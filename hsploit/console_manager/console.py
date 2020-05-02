from hsploit.searcher.db_manager.session_manager import start_session
from hsploit.searcher.db_manager.models import Exploit, Shellcode
import os, sys
from tabulate import tabulate
from hsploit.console_manager.colors import W, O, R, G
from shutil import copyfile
from hsploit.searcher.engine.string import get_vulnerability_extension
from hsploit.searcher.engine.updates import get_latest_db_update_date, install_updates
from hsploit.searcher.engine.suggestions import substitute_with_suggestions, propose_suggestions, get_suggestions_list, new_suggestion,\
    remove_suggestion, get_suggestion, DEFAULT_SUGGESTIONS
from hsploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description
from hsploit.searcher.engine.search_engine import search_vulnerabilities_in_db, search_vulnerabilities_advanced, get_vulnerability_filters
from hsploit.searcher.db_manager.result_set import print_result_set, result_set_len, print_result_set_no_table
import datetime


# Software information constants
SW_VERSION = '2.0.0'
RELEASE_DATE = '2020-04-26'
DEVELOPER = 'Nicolas Carolo'
LATEST_DB_UPDATE = get_latest_db_update_date()


def print_guide():
    print_ascii_art()
    print(O + 'USAGE:' + W)
    print(tabulate([[G + 'Perform a search' + W, 'hsploit -s "[search text]"'],
                    [G + 'Perform a search (without keywords highlighting)' + W,
                     'hsploit -s --nokeywords "[search text]"'],
                    [G + 'Perform a search (no table for results)' + W, 'hsploit -s --notable "[search text]"'],
                    [G + 'Show info about the exploit' + W, 'hsploit -ie [exploit\'s id]'],
                    [G + 'Show info about the shellcode' + W, 'hsploit -is [shellcode\'s id]'],
                    [G + 'Open the exploit\'s source code with vim' + W, 'hsploit -oe [exploit\'s id]'],
                    [G + 'Open the shellcode\'s source code with vim' + W,
                    'hsploit -os [shellcode\'s id]'],
                    [G + 'Copy the exploit\'s file into a chosen file or directory' + W,
                    'hsploit -cpe [exploit\'s id] [file or directory]'],
                    [G + 'Copy the shellcode\'s file into a chosen file or directory' + W,
                    'hsploit -cps [shellcode\'s id] [file or directory]'],
                    [G + 'List suggestions' + W, 'hsploit -ls'],
                    [G + 'Add or edit a suggestion' + W, 'hsploit -as [keyword(s)]'],
                    [G + 'Remove a suggestion' + W, 'hsploit -rs [keyword(s)]'],
                    [G + 'Show software information' + W, 'hsploit -v'],
                    [G + 'Check for software and database updates' + W, 'hsploit -u'],
                    [G + 'Show help' + W, 'hsploit -help']],
                   [R + 'ACTION' + W, R + 'COMMAND LINE' + W], tablefmt='grid'))
    exit(0)


def print_software_information():
    print_ascii_art()
    print(tabulate([[O + 'Version:' + W, SW_VERSION],
                    [O + 'Release date:' + W, RELEASE_DATE],
                    [O + 'Developer:' + W, DEVELOPER],
                    [O + 'Latest Database update:' + W, LATEST_DB_UPDATE]], tablefmt='grid'))
    exit(0)


def perform_search(searched_text, output_type):
    searched_text = substitute_with_suggestions(searched_text)
    suggested_search_text = propose_suggestions(searched_text)
    key_words_list = (str(searched_text).upper()).split()
    if output_type == "standard":
        exploits_result_set = highlight_keywords_in_description(key_words_list, search_vulnerabilities_in_db(searched_text, 'searcher_exploit'))
        shellcodes_result_set = highlight_keywords_in_description(key_words_list, search_vulnerabilities_in_db(searched_text, 'searcher_shellcode'))
    else:
        exploits_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
        shellcodes_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_shellcode')
    print('\n' + str(result_set_len(exploits_result_set)) + ' exploits and '
        + str(result_set_len(shellcodes_result_set)) + ' shellcodes found.\n')
    if output_type == "standard" or output_type == "nokeywords":
        if result_set_len(exploits_result_set) > 0:
            print(O + 'EXPLOITS:' + W)
            print_result_set(exploits_result_set)
        if result_set_len(shellcodes_result_set) > 0:
            print('\n' + O + 'SHELLCODES:' + W)
            print_result_set(shellcodes_result_set)
        if suggested_search_text != "":
            perform_suggested_search(suggested_search_text, output_type)
        else:
            exit(0)
    if output_type == "notable":
        if result_set_len(exploits_result_set) > 0:
            print(O + 'EXPLOITS:' + W)
            print_result_set_no_table(exploits_result_set)
        if result_set_len(shellcodes_result_set) > 0:
            print('\n' + O + 'SHELLCODES:' + W)
            print_result_set_no_table(shellcodes_result_set)
        if suggested_search_text != "":
            perform_suggested_search(suggested_search_text, output_type)
        else:
            exit(0)


def perform_advanced_search(searched_text, output_type, operator_filter, type_filter, platform_filter, author_filter,
                                    port_filter, date_from_filter, date_to_filter):
    vulnerability_types_list, vulnerability_platforms_list = get_vulnerability_filters()
    if operator_filter == "":
        while not operator_filter in ['AND', 'OR']:
            operator_filter = input("Search operator [AND/OR]: ")
            operator_filter = str(operator_filter).upper()
        author_filter = input("Author: ")
        author_filter = str(author_filter).lower()
        vulnerability_types_list.insert(0, "all")
        while not type_filter in vulnerability_types_list:
            type_filter = input("Type (write '-list' for listing all available types): ")
            type_filter = str(type_filter).lower()
            if type_filter == "":
                type_filter = "all"
            if type_filter == '-list':
                for item in vulnerability_types_list:
                    print(G + item + W)
        vulnerability_platforms_list.insert(0, "all")
        while not platform_filter in vulnerability_platforms_list:
            platform_filter = input("Platform (write '-list' for listing all available platforms): ")
            platform_filter = str(platform_filter).lower()
            if platform_filter == "":
                platform_filter = "all"
            if platform_filter == '-list':
                for item in vulnerability_platforms_list:
                    print(G + item + W)
        ports_list = [str(x) for x in range(0, 65536)]
        ports_list.insert(0, "")
        while not port_filter in ports_list:
            port_filter = input("Port (0 <= port <= 65535): ")
        date_from_filter, date_to_filter = get_input_date()
        while not (datetime.datetime.now() >= datetime.datetime.strptime(date_to_filter, '%Y-%m-%d') >= datetime.datetime.strptime(date_from_filter, '%Y-%m-%d')) :
            print(R + "Error:" + W + " please insert a valid date interval")
            date_from_filter, date_to_filter = get_input_date()

    searched_text = substitute_with_suggestions(searched_text)
    suggested_search_text = propose_suggestions(searched_text)
    key_words_list = (str(searched_text).upper()).split()
    exploits_list = search_vulnerabilities_advanced(searched_text, 'searcher_exploit', operator_filter, type_filter,
                                                        platform_filter, author_filter, port_filter, date_from_filter,
                                                        date_to_filter)
    if output_type == "standard":
        exploits_result_set = highlight_keywords_in_description(key_words_list, exploits_list)
    else:
        exploits_result_set = exploits_list
    shellcodes_list = search_vulnerabilities_advanced(searched_text, 'searcher_shellcode', operator_filter,
                                                          type_filter, platform_filter, author_filter, port_filter,
                                                          date_from_filter, date_to_filter)
    if output_type == "standard":
        shellcodes_result_set = highlight_keywords_in_description(key_words_list, shellcodes_list)
    else:
        shellcodes_result_set = shellcodes_list
    print('\n' + str(result_set_len(exploits_result_set)) + ' exploits and '
        + str(result_set_len(shellcodes_result_set)) + ' shellcodes found.\n')
    if output_type == "standard" or output_type == "nokeywords":
        if result_set_len(exploits_result_set) > 0:
            print(O + 'EXPLOITS:' + W)
            print_result_set(exploits_result_set)
        if result_set_len(shellcodes_result_set) > 0:
            print('\n' + O + 'SHELLCODES:' + W)
            print_result_set(shellcodes_result_set)
        if suggested_search_text != "":
            perform_advanced_suggested_search(suggested_search_text, output_type, operator_filter, type_filter,
                                    platform_filter, author_filter, port_filter, date_from_filter, date_to_filter)
        else:
            exit(0)
    if output_type == "notable":
        if result_set_len(exploits_result_set) > 0:
            print(O + 'EXPLOITS:' + W)
            print_result_set_no_table(exploits_result_set)
        if result_set_len(shellcodes_result_set) > 0:
            print('\n' + O + 'SHELLCODES:' + W)
            print_result_set_no_table(shellcodes_result_set)
        if suggested_search_text != "":
            perform_advanced_suggested_search(suggested_search_text, output_type, operator_filter, type_filter,
                                    platform_filter, author_filter, port_filter, date_from_filter, date_to_filter)
        else:
            exit(0)


def get_input_date():
    while True:
        try:
            date_from_filter = input("Date from (yyyy-mm-dd): ")
            datetime.datetime.strptime(date_from_filter, '%Y-%m-%d')
            break
        except ValueError:
            if date_from_filter == "":
                return "1900-01-01", datetime.datetime.now().strftime("%Y-%m-%d")
    while True:
        try:
            date_to_filter = input("Date to (yyyy-mm-dd): ")
            datetime.datetime.strptime(date_to_filter, '%Y-%m-%d')
            break
        except ValueError:
            if date_to_filter == "":
                date_to_filter = datetime.datetime.now().strftime("%Y-%m-%d")
                break
    if date_from_filter == "" and date_to_filter == "":
        return "1900-01-01", datetime.datetime.now().strftime("%Y-%m-%d")
    else:
        return date_from_filter, date_to_filter


def perform_suggested_search(suggested_search, output_type):
    answer = ""
    while not answer in ['y', 'n', 'yes', 'no']:
        answer = input("\nDo you wish to search also for '" + suggested_search + "'?: ")
        answer = str(answer).lower()
    if answer[0:1] == 'n':
        exit(0)
    else:
        perform_search(suggested_search, output_type)


def perform_advanced_suggested_search(suggested_search, output_type, operator_filter, type_filter, platform_filter, author_filter,
                                    port_filter, date_from_filter, date_to_filter):
    answer = ""
    while not answer in ['y', 'n', 'yes', 'no']:
        answer = input("\nDo you wish to search also for '" + suggested_search + "'?: ")
        answer = str(answer).lower()
    if answer[0:1] == 'n':
        exit(0)
    else:
        perform_advanced_search(suggested_search, output_type, operator_filter, type_filter, platform_filter, author_filter,
                                    port_filter, date_from_filter, date_to_filter)


def open_exploit(id):
    """
    Open the exploit identified by the id.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.expanduser("~") + "/HoundSploit/exploitdb/"
        os.system('vim ' + vulnerabilities_path + queryset[0].file)
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)


def open_shellcode(id):
    """
    Open the shellcode identified by the id.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.expanduser("~") + "/HoundSploit/exploitdb/"
        os.system('vim ' + vulnerabilities_path + queryset[0].file)
    except IndexError:
        print('ERROR: Shellcode not found!')
    return exit(0)


def show_exploit_info(id):
    """
    Show the information about the exploit identified by the id.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        exploit = queryset[0]
        if exploit.port:
            print(tabulate([[O + 'DESCRIPTION:' + W, exploit.description], [O + 'AUTHOR:' + W, exploit.author],
                            [O + 'FILE:' + W, exploit.file], [O + 'DATE:' + W, exploit.date],
                            [O + 'TYPE:' + W, exploit.type], [O + 'PLATFORM:' + W, exploit.platform],
                            [O + 'PORT:' + W, exploit.port]], tablefmt='grid'))
        else:
            print(tabulate([[O + 'DESCRIPTION:' + W, exploit.description], [O + 'AUTHOR:' + W, exploit.author],
                            [O + 'FILE:' + W, exploit.file], [O + 'DATE:' + W, exploit.date],
                            [O + 'TYPE:' + W, exploit.type], [O + 'PLATFORM:' + W, exploit.platform]], tablefmt='grid'))
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)


def show_shellcode_info(id):
    """
    Show the information about the shellcode identified by the id.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        shellcode = queryset[0]
        print(tabulate([[O + 'DESCRIPTION:' + W, shellcode.description], [O + 'AUTHOR:' + W, shellcode.author],
                        [O + 'FILE:' + W, shellcode.file], [O + 'DATE:' + W, shellcode.date],
                        [O + 'TYPE:' + W, shellcode.type], [O + 'PLATFORM:' + W, shellcode.platform]], tablefmt='grid'))
    except IndexError:
        print('ERROR: Shellcode not found!')
    return exit(0)


def print_ascii_art():
    print("" + O)
    print("  .__                   .__         .__  __")   
    print("  |  |__   ____________ |  |   ____ |__|/  |_              __    ")
    print("  |  |  \ /  ___/\____ \|  |  /  _ \|  \   __\\ (\,--------'()'--o")
    print("  |   Y  \\___ \ |  |_> >  |_(  <_> )  ||  |    (_    ___    /~\" ")
    print("  |___|  /____  >|   __/|____/\____/|__||__|     (_)_)  (_)_)    ")
    print("       \/     \/ |__|                         ")
    print(W + "")


def check_for_updates():
    install_updates()
    exit(0)


def copy_exploit(id, dst):
    """
    Copy the exploit identified by the id into the destination specified by the user.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.expanduser("~") + "/HoundSploit/exploitdb/"
        src = vulnerabilities_path + queryset[0].file
        try:
            copyfile(src, dst)
        except IsADirectoryError:
            if src[-1:] == '/':
                dst = dst + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            else:
                dst = dst + '/' + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            copyfile(src, dst)
    except IndexError:
        print(R + "ERROR:" + W + " Exploit not found!")
    except FileNotFoundError:
        print(R + "ERROR:" + W + " Please insert a valid destination path")
    return exit(0)


def copy_shellcode(id, dst):
    """
    Copy the shellcode identified by the id into the destination specified by the user.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        vulnerabilities_path = os.path.expanduser("~") + "/HoundSploit/exploitdb/"
        src = vulnerabilities_path + queryset[0].file
        try:
            copyfile(src, dst)
        except IsADirectoryError:
            if src[-1:] == '/':
                dst = dst + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            else:
                dst = dst + '/' + queryset[0].id + get_vulnerability_extension(queryset[0].file)
            copyfile(src, dst)
    except IndexError:
        print(R + "ERROR:" + W + " Shellcode not found!")
    except FileNotFoundError:
        print(R + "ERROR:" + W + " Please insert a valid destination path")
    return exit(0)


def print_suggestions_list():
    print()
    print(tabulate([[instance.searched, instance.suggestion, instance.autoreplacement] for instance in get_suggestions_list()],
                   [O + 'SEARCHED WORDS' + W, O + 'SUGGESTION' + W, O + 'AUTOREPLACEMENT' + W], tablefmt='grid'))
    print()
    exit(0)


def add_suggestion(searched):
    searched = str(searched).lower()
    suggestion = ""
    autoreplacement = ""
    answer = ""
    if searched in DEFAULT_SUGGESTIONS:
        print(R +"ERROR:" + W + " default suggestions cannot be modified.")
        exit(1)
    while suggestion == "":
        suggestion = input("Suggestion: ")
        suggestion = str(suggestion).lower()
    while not autoreplacement in ['y', 'n', 'yes', 'no']:
        autoreplacement = input("Autoreplacement [Y/N]: ")
        autoreplacement = str(autoreplacement).lower()
    if autoreplacement[0:1] == "y":
        autoreplacement = "true"
    else:
        autoreplacement = "false"
    print()
    print(tabulate([[G + searched + W, G + suggestion + W, G + autoreplacement + W]],
                   [O + 'SEARCHED WORDS' + W, O + 'SUGGESTIONS' + W, O + 'AUTOREPLACEMENT' + W], tablefmt='grid'))
    print()
    while not answer in ['y', 'n', 'yes', 'no']:
        answer = input("\nDo you wish to save the new suggestion? [Y/N]: ")
        answer = str(answer).lower()
    if answer[0:1] == "y":
        new_suggestion(searched, suggestion, autoreplacement)
        print("New suggestion added!\n")
    else:
        print("New suggestion cancelled!\n")
    exit(0)


def delete_suggestion(searched):
    answer = ""
    searched = str(searched).lower()
    if searched in DEFAULT_SUGGESTIONS:
        print(R +"ERROR:" + W + " default suggestions cannot be remove.")
        exit(1)
    suggestion_item = get_suggestion(searched)
    if suggestion_item is not None:
        print()
        print(tabulate([[R + suggestion_item.searched + W, R + suggestion_item.suggestion + W, R + suggestion_item.autoreplacement + W]],
            [O + 'SEARCHED WORDS' + W, O + 'SUGGESTIONS' + W, O + 'AUTOREPLACEMENT' + W], tablefmt='grid'))
        while not answer in ['y', 'n', 'yes', 'no']:
            answer = input("\nDo you really want to remove this suggestion? [Y/N]: ")
            answer = str(answer).lower()
        if answer[0:1] == "y":
            remove_suggestion(searched)
            print("Suggestion removed!")
        else:
            print()
        exit(0)
    else:
        print(R +"ERROR:" + W + " suggestion not found.")
        exit(1)