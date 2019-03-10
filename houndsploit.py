import sys
from searcher.engine.search_engine import search_vulnerabilities_for_description


def main(argv):
    print(argv)
    search_vulnerabilities_for_description(argv, 'searcher_exploit')


if __name__ == "__main__":
    main(sys.argv[1:])
