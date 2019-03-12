from searcher.db_manager.result_set import exclude

from sqlalchemy import and_
from searcher.db_manager.models import Exploit
from searcher.db_manager.session_manager import start_session
from searcher.db_manager.result_set import queryset2list


def main():
    session = start_session()
    queryset = session.query(Exploit).filter(and_(Exploit.description.like('%cisco%')))
    result_set = queryset2list(queryset)
    session.close()

    print('\n' + str(list(result_set).__len__()))

    result_set = exclude(result_set, 'Cisco IOS - IPv4 Packets Denial of Service')

    print('\n' + str(list(result_set).__len__()))

    result_set = exclude(result_set, 'Cisco - Cisco Global er Tool')

    print('\n' + str(list(result_set).__len__()))


if __name__ == "__main__":
    main()