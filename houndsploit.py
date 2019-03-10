import sys
from searcher.engine.search_engine import search_vulnerabilities_for_description


def main(argv):
    if argv.__len__() > 0:
        search_vulnerabilities_for_description(argv, 'searcher_exploit')
    else:
        print('show guide!')


if __name__ == "__main__":
    main(sys.argv[1:])
