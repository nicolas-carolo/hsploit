"""Main module."""
__all__ = ()

import sys
import os
from hsploit.searcher.engine.search_engine import search_vulnerabilities_in_db
from hsploit.searcher.db_manager.result_set import print_result_set, result_set_len, print_result_set_no_table
from hsploit.console_manager.colors import O, W, R
from hsploit.console_manager.console import print_guide, open_exploit, open_shellcode, show_exploit_info,\
    show_shellcode_info,print_software_information, copy_exploit, copy_shellcode, check_for_updates
from hsploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description
from hsploit.searcher.engine.csv2sqlite import create_db
from hsploit.searcher.engine.updates import install_updates


def main(args=None):
    """Main routine of hsploit."""
    init_path = os.path.expanduser("~") + "/HoundSploit"
    if not os.path.isfile(init_path + "/hound_db.sqlite3"):
        install_updates()
        create_db()

    if args is None:
        args = sys.argv[1:]

    if args.__len__() == 0 or args[0] == '-help' or str(args[0]).isspace() or str(args[0]) == "":
        print_guide()

    if args[0] == '-u':
        check_for_updates()

    if args[0] == '-v':
        print_software_information()

    if args[0] == '-oe' and not args[1] is None:
        open_exploit(args[1])

    if args[0] == '-os' and not args[1] is None:
        open_shellcode(args[1])

    if args[0] == '-ie' and not args[1] is None:
        show_exploit_info(args[1])

    if args[0] == '-is' and not args[1] is None:
        show_shellcode_info(args[1])
    
    if (args[0] == '-cps' or args[0] == '-cpe') and len(args) < 3:
        print(R + 'ERROR: ' + W + "\'-cps\' and \'-cpe\' options require three arguments")
        exit(0)
    else:
        if args[0] == '-cpe' and not args[1] is None and not args[2] is None:
            id = args[1]
            dst = args[2]
            copy_exploit(id, dst)

        if args[0] == '-cps' and not args[1] is None and not args[2] is None:
            id = args[1]
            dst = args[2]
            copy_shellcode(id, dst)       
    

    if len(args) == 2 and args[0] == '-s':
        searched_text = args[1]
        key_words_list = (str(searched_text).upper()).split()
        exploits_result_set = highlight_keywords_in_description(key_words_list, search_vulnerabilities_in_db(searched_text, 'searcher_exploit'))
        shellcodes_result_set = highlight_keywords_in_description(key_words_list, search_vulnerabilities_in_db(searched_text, 'searcher_shellcode'))
        print('\n' + str(result_set_len(exploits_result_set)) + ' exploits and '
              + str(result_set_len(shellcodes_result_set)) + ' shellcodes found.\n')
        if result_set_len(exploits_result_set) > 0:
            print(O + 'EXPLOITS:' + W)
            print_result_set(exploits_result_set)
        if result_set_len(shellcodes_result_set) > 0:
            print('\n' + O + 'SHELLCODES:' + W)
            print_result_set(shellcodes_result_set)
    elif len(args) == 3 and args[0] == '-s' and args[1] == '--nokeywords' and not (str(args[2]).isspace() or str(args[2]) == ""):
        searched_text = args[2]
        exploits_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
        shellcodes_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_shellcode')
        print('\n' + str(result_set_len(exploits_result_set)) + ' exploits and '
              + str(result_set_len(shellcodes_result_set)) + ' shellcodes found.\n')
        if result_set_len(exploits_result_set) > 0:
            print(O + 'EXPLOITS:' + W)
            print_result_set(exploits_result_set)
        if result_set_len(shellcodes_result_set) > 0:
            print('\n' + O + 'SHELLCODES:' + W)
            print_result_set(shellcodes_result_set)
    elif len(args) == 3 and args[0] == '-s' and args[1] == '--notable' and not (str(args[2]).isspace() or str(args[2]) == ""):
        searched_text = args[2]
        exploits_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
        shellcodes_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_shellcode')
        print('\n' + str(result_set_len(exploits_result_set)) + ' exploits and '
              + str(result_set_len(shellcodes_result_set)) + ' shellcodes found.\n')
        if result_set_len(exploits_result_set) > 0:
            print('EXPLOITS:')
            print_result_set_no_table(exploits_result_set)
        if result_set_len(shellcodes_result_set) > 0:
            print('\n' + 'SHELLCODES:')
            print_result_set_no_table(shellcodes_result_set)
    else:
        print_guide()