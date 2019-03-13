import sys
from searcher.engine.search_engine import search_vulnerabilities_in_db
from searcher.db_manager.result_set import print_result_set, result_set_len
from tools.colors import O, W
from searcher.db_manager.session_manager import start_session
from searcher.db_manager.models import Exploit, Shellcode
import os


def main(argv):
    if argv.__len__() == 0:
        print('usage: python houndsploit.py "[text to search]"')
        exit(0)

    if argv[0] == '-oe' and not argv[1] is None:
        session = start_session()
        queryset = session.query(Exploit).filter(Exploit.id == argv[1])
        session.close()
        try:
            os.system('nano ' + './searcher/vulnerabilities/' + queryset[0].file)
        except IndexError:
            print('ERROR: Exploit not found!')
        return exit(0)

    if argv[0] == '-os' and not argv[1] is None:
        session = start_session()
        queryset = session.query(Shellcode).filter(Shellcode.id == argv[1])
        session.close()
        try:
            os.system('nano ' + './searcher/vulnerabilities/' + queryset[0].file)
        except IndexError:
            print('ERROR: Shellcode not found!')
        return exit(0)

    searched_text = argv[0]
    exploits_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_exploit')
    shellcodes_result_set = search_vulnerabilities_in_db(searched_text, 'searcher_shellcode')
    print(str(result_set_len(exploits_result_set)) + ' exploits and ' + str(result_set_len(shellcodes_result_set)) + ' shellcodes found.\n')
    if result_set_len(exploits_result_set) > 0:
        print(O + 'EXPLOITS:' + W)
        print_result_set(exploits_result_set)
    if result_set_len(shellcodes_result_set) > 0:
        print('\n' + O + 'SHELLCODES:' + W)
        print_result_set(shellcodes_result_set)


if __name__ == "__main__":
    main(sys.argv[1:])
