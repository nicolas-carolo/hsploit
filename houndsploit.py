import sys
import os
from searcher.engine.search_engine import search_vulnerabilities_in_db
from searcher.db_manager.result_set import print_result_set, result_set_len
from console_manager.colors import O, W, R
from console_manager.console import print_guide, open_exploit, open_shellcode, show_exploit_info, show_shellcode_info,\
    print_software_information, check_for_updates, check_for_exploitdb_updates


def main(argv):
    if not os.path.isfile('houndsploit.py'):
        print("Change the current working directory to the directory of \'houndsploit.py\'"
              " for executing HoundSploit.")
        exit(0)

    if not os.path.isfile('hound_db.sqlite3'):
        print("Run \'setup.py\' before executing \'houndsploit.py\'.")
        exit(0)

    if argv.__len__() == 0 or argv[0] == '-help':
        print_guide()

    if argv[0] == '-u':
        check_for_updates()

    if argv[0] == '-udb':
        check_for_exploitdb_updates()

    if argv[0] == '-v':
        print_software_information()

    if argv[0] == '-oe' and not argv[1] is None:
        open_exploit(argv[1])

    if argv[0] == '-os' and not argv[1] is None:
        open_shellcode(argv[1])

    if argv[0] == '-ie' and not argv[1] is None:
        show_exploit_info(argv[1])

    if argv[0] == '-is' and not argv[1] is None:
        show_shellcode_info(argv[1])

    if len(argv) == 1:
        searched_text = argv[0]
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


if __name__ == "__main__":
    main(sys.argv[1:])
