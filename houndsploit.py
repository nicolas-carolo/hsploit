import sys
from searcher.engine.search_engine import search_vulnerabilities_in_db


def main(argv):
    if argv.__len__() == 0:
        print('show guide!')
        exit(0)

    print('Exploits:')
    queryset = search_vulnerabilities_in_db(argv, 'searcher_exploit')
    print_exploits(queryset)
    print('\nShellcodes:')
    queryset = search_vulnerabilities_in_db(argv, 'searcher_shellcode')
    print_shellcodes(queryset)


def print_exploits(queryset):
    for exploit in queryset:
        print(exploit.description)


def print_shellcodes(queryset):
    for shellcode in queryset:
        print(shellcode.description)


if __name__ == "__main__":
    main(sys.argv[1:])
