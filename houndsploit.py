import sys
from searcher.engine.search_engine import search_vulnerabilities_in_db
from searcher.db_manager.result_set import print_instances, result_set_len


def main(argv):
    if argv.__len__() == 0:
        print('show guide!')
        exit(0)

    exploits_result_set = search_vulnerabilities_in_db(argv, 'searcher_exploit')
    shellcodes_result_set = search_vulnerabilities_in_db(argv, 'searcher_shellcode')
    print(str(result_set_len(exploits_result_set)) + ' exploits and ' + str(result_set_len(shellcodes_result_set)) + ' shellcodes found.\n')
    print('Exploits:')
    print_instances(exploits_result_set)
    print('\nShellcodes:')
    print_instances(shellcodes_result_set)


if __name__ == "__main__":
    main(sys.argv[1:])
