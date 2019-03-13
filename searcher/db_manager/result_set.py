from sqlalchemy import or_

from searcher.db_manager.models import Exploit, Shellcode
from searcher.db_manager.session_manager import start_session


def queryset2list(queryset):
    list = []
    for instance in queryset:
        list.append(instance)
    return list


def print_instances(result_set):
    for instance in result_set:
        print(instance.description)


def void_result_set():
    list = []
    return list


def result_set_len(result_set):
    try:
        return len(result_set)
    except TypeError:
        return 0


def join_result_sets(result_set_1, result_set_2, db_table):
    list_id_1 = []
    list_id_2 = []
    for instance in result_set_1:
        list_id_1.append(instance.id)
    for instance in result_set_2:
        list_id_2.append(instance.id)
    union_list_id = set(list_id_1) | set(list_id_2)
    print(union_list_id)
    print(union_list_id.__len__())

    session = start_session()
    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(or_(Exploit.id == instance_id for instance_id in union_list_id))
    else:
        queryset = session.query(Shellcode).filter(or_(Shellcode.id == instance_id for instance_id in union_list_id))

    session.close()
    return queryset2list(queryset)
