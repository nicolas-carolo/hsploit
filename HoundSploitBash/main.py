# -*- encoding: utf-8 -*-
# HoundSploitBash v1.4.0
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
from HoundSploitBash.cl_parser import parse_args

import os
from HoundSploitBash.searcher.engine.search_engine import search_vulnerabilities_in_db
from HoundSploitBash.searcher.db_manager.result_set import print_result_set, result_set_len
from HoundSploitBash.console_manager.colors import O, W, R
from HoundSploitBash.console_manager.console import print_guide, open_exploit, open_shellcode, show_exploit_info, show_shellcode_info,\
    print_software_information, check_for_updates, check_for_exploitdb_updates, install_exploitdb_update


def main(args=None):
    """Main routine of HoundSploitBash."""
    init_path = os.path.split(sys.executable)[0]
    if not os.path.isfile(init_path + "/hound_db.sqlite3"):
        print(init_path + "/hound_db.sqlite3")
        install_exploitdb_update(init_path)

    if args is None:
        args = sys.argv[1:]

    if args.__len__() == 0 or args[0] == '-help' or str(args[0]).isspace():
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

    if len(args) == 1:
        searched_text = args[0]
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
    else:
        print(R + 'ERROR: ' + W + ' Bad input!')
        print_guide()
