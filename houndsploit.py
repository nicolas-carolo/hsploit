import sys
from searcher.engine.search_engine import search_vulnerabilities_in_db
from searcher.db_manager.result_set import print_instances


def main(argv):
    if argv.__len__() == 0:
        print('show guide!')
        exit(0)

    exploits_result_set = search_vulnerabilities_in_db(argv, 'searcher_exploit')
    # shellcodes_result_set = search_vulnerabilities_in_db(argv, 'searcher_shellcode')
    # print(str(exploits_result_set.list.__len__()) + ' exploits and ' + str(shellcodes_result_set.list.__len__()) +
    #       ' shellcodes found')
    print(exploits_result_set.__len__())
    print('Exploits:')
    # print_exploits(queryset)
    print_instances(exploits_result_set)
    # print('\nShellcodes:')
    # print_shellcodes(queryset)
    # print_instances(shellcodes_result_set)

# def print_exploits(queryset):
#     for exploit in queryset:
#         print(exploit.description)
#
#
# def print_shellcodes(queryset):
#     for shellcode in queryset:
#         print(shellcode.description)


if __name__ == "__main__":
    main(sys.argv[1:])
