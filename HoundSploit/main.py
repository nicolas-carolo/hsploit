# -*- encoding: utf-8 -*-
# hsploit v1.7.0
# An advanced command-line search engine for Exploit-DB
# Copyright © 2019, Nicolas Carolo.
# See /LICENSE for licensing information.

"""
INSERT MODULE DESCRIPTION HERE.

:Copyright: © 2019, Nicolas Carolo.
:License: BSD (see /LICENSE).
"""

__all__ = ()

import sys
import os
from HoundSploit.searcher.engine.search_engine import search_vulnerabilities_in_db
from HoundSploit.searcher.db_manager.result_set import print_result_set, result_set_len, print_result_set_no_table
from HoundSploit.console_manager.colors import O, W, R
from HoundSploit.console_manager.console import print_guide, open_exploit, open_shellcode, show_exploit_info,\
    show_shellcode_info,print_software_information, check_for_updates, check_for_exploitdb_updates,\
    install_exploitdb_update, copy_exploit, copy_shellcode
from HoundSploit.searcher.engine.keywords_highlighter import highlight_keywords_in_description


def main(args=None):
    """Main routine of hsploit."""
    init_path = os.path.split(sys.executable)[0]
    if not os.path.isfile(init_path + "/hound_db.sqlite3"):
        print(init_path + "/hound_db.sqlite3")
        install_exploitdb_update(init_path)

    if args is None:
        args = sys.argv[1:]

    if args.__len__() == 0 or args[0] == '-help' or str(args[0]).isspace() or str(args[0]) == "":
        print_guide()

    if args[0] == '-u':
        check_for_updates()

    if args[0] == '-udb':
        check_for_exploitdb_updates()

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
        print(len(args))
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
    

    if len(args) == 1:
        searched_text = args[0]
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
    elif len(args) == 2 and args[0] == '--nokeywords' and not (str(args[1]).isspace() or str(args[1]) == ""):
        searched_text = args[1]
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
    elif len(args) == 2 and args[0] == '--notable' and not (str(args[1]).isspace() or str(args[1]) == ""):
        searched_text = args[1]
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
        print(R + 'ERROR: ' + W + ' Bad input!')
        print_guide()
