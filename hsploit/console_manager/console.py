from hsploit.searcher.db_manager.session_manager import start_session
from hsploit.searcher.db_manager.models import Exploit, Shellcode
import os, sys
from tabulate import tabulate
from hsploit.console_manager.colors import W, O, R, G
from shutil import copyfile
from hsploit.searcher.engine.string import get_vulnerability_extension
from hsploit.searcher.engine.updates import get_latest_db_update_date, install_updates


# Software information constants
SW_VERSION = '1.8.5'
RELEASE_DATE = '2020-04-22'
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
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/HoundSploit/vulnerabilities/"
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
        print('ERROR: Exploit not found!')
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
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/HoundSploit/vulnerabilities/"
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
        print('ERROR: Exploit not found!')
    return exit(0)