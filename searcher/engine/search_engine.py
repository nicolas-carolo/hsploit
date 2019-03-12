from searcher.engine.string import str_is_num_version
from searcher.engine.filter_query import filter_exploits_without_comparator, filter_exploits_with_comparator,\
    filter_shellcodes_without_comparator, filter_shellcodes_with_comparator

from sqlalchemy import and_, or_
from searcher.db_manager.models import Exploit, Shellcode
from searcher.db_manager.session_manager import start_session
from searcher.db_manager.result_set import queryset2list, void_result_set

N_MAX_RESULTS_NUMB_VERSION = 20000


def search_vulnerabilities_in_db(word_list, db_table):
    searched_text = word_list[0]
    for word in word_list[1:]:
        searched_text = searched_text + ' ' + word

    if str(searched_text).isnumeric():
        return search_vulnerabilities_numerical(word_list[0], db_table)
    elif str_is_num_version(str(searched_text)) and str(searched_text).__contains__(' ') and not str(
            searched_text).__contains__('<'):
        result_set = search_vulnerabilities_version(word_list, db_table)
        # TODO union with standard research (test)
        standard_result_set = search_vulnerabilities_for_text_input(word_list, db_table)

        in_first = set(result_set)
        in_second = set(standard_result_set)

        in_second_but_not_in_first = in_second - in_first

        result = result_set + list(in_second_but_not_in_first)

        return result
    else:
        result_set = search_vulnerabilities_for_description(word_list, db_table)
        if len(result_set) > 0:
            return result_set
        else:
            result_set = search_vulnerabilities_for_file(word_list, db_table)
            if len(result_set) > 0:
                return result_set
            else:
                return search_vulnerabilities_for_author(word_list, db_table)


def search_vulnerabilities_numerical(searched_text, db_table):
    """
    Perform a search based on vulnerabilities' description, file, id, and port (only if it is an exploit) for an only
    numerical search input.
    :param searched_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset with search results.
    """
    session = start_session()
    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(or_(Exploit.description.like('%' + searched_text + '%'),
                                                     Exploit.id == int(searched_text),
                                                     Exploit.file.like('%' + searched_text + '%'),
                                                     Exploit.port == int(searched_text)
                                                     ))
    else:
        queryset = session.query(Shellcode).filter(or_(Shellcode.description.like('%' + searched_text + '%'),
                                                       Shellcode.id == int(searched_text),
                                                       Shellcode.file.like('%' + searched_text + '%')
                                                       ))
    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_description(word_list, db_table):
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.description.like('%' + word + '%') for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.description.like('%' + word + '%') for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_file(word_list, db_table):
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.file.like('%' + word + '%') for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.file.like('%' + word + '%') for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_for_author(word_list, db_table):
    session = start_session()

    if db_table == 'searcher_exploit':
        queryset = session.query(Exploit).filter(and_(Exploit.author.like('%' + word + '%') for word in word_list))
    else:
        queryset = session.query(Shellcode).filter(
            and_(Shellcode.author.like('%' + word + '%') for word in word_list))

    session.close()
    return queryset2list(queryset)


def search_vulnerabilities_version(word_list, db_table):
    software_name = word_list[0]
    for word in word_list[1:]:
        if not str_is_num_version(word):
            software_name = software_name + ' ' + word
        else:
            num_version = word
    if db_table == 'searcher_exploit':
        return search_exploits_version(software_name, num_version)
    else:
        return search_shellcodes_version(software_name, num_version)


def search_exploits_version(software_name, num_version):
    """
    Perform a search based on exploits' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_exploit' DB table.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(and_(Exploit.description.like('%' + software_name + '%')))
    query_result_set = queryset2list(queryset)
    session.close()
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        return void_result_set()
    final_result_set = []
    for exploit in query_result_set:
        # if exploit not contains '<'
        if not str(exploit.description).__contains__('<'):
            final_result_set = filter_exploits_without_comparator(exploit, num_version, software_name, final_result_set)
        # if exploit contains '<'
        else:
            final_result_set = filter_exploits_with_comparator(exploit, num_version, software_name, final_result_set)
    return final_result_set


def search_shellcodes_version(software_name, num_version):
    """
    Perform a search based on exploits' description for an input search that contains a number of version.
    This function is called by 'search_vulnerabilities_version' method.
    :param software_name: the name of the software that the user is searching for.
    :param num_version: the specific number of version the user is searching for.
    :return: a queryset with search result found in 'searcher_exploit' DB table.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(and_(Shellcode.description.like('%' + software_name + '%')))
    query_result_set = queryset2list(queryset)
    session.close()
    # limit the time spent for searching useless results.
    if queryset.count() > N_MAX_RESULTS_NUMB_VERSION:
        # return Exploit.objects.none()
        return void_result_set()
    final_result_set = []
    for shellcode in query_result_set:
        # if exploit not contains '<'
        if not str(shellcode.description).__contains__('<'):
            final_result_set = filter_shellcodes_without_comparator(shellcode, num_version, software_name, final_result_set)
        # if exploit contains '<'
        else:
            final_result_set = filter_shellcodes_with_comparator(shellcode, num_version, software_name, final_result_set)
    return final_result_set


# def search_vulnerabilities_advanced(search_text, db_table, operator_filter, type_filter, platform_filter, author_filter,
#                                     port_filter, start_date_filter, end_date_filter):
#     """
#     Perform a search based on filter selected by the user for an input search.
#     :param search_text: the search input.
#     :param db_table: the DB table in which we want to perform the search.
#     :param operator_filter: OR operator matches all search results that contain at least one search keyword,
#                             AND operator matches only search results that contain all the search keywords.
#     :param type_filter: the filter on the vulnerabilities' type.
#     :param platform_filter: the filter on the vulnerabilities' platform.
#     :param author_filter: the filter on the vulnerabilities' author.
#     :param port_filter: the filter on the exploits' port.
#     :param start_date_filter: the filter on the vulnerabilities' date (from).
#     :param end_date_filter: the filter on the vulnerabilities' date (to).
#     :return: a queryset containing all the search results.
#     """
#     words_list = str(search_text).upper().split()
#     if operator_filter == 'AND' and search_text != '':
#         queryset = search_vulnerabilities_for_description_advanced(search_text, db_table)
#     elif operator_filter == 'OR':
#         try:
#             query = reduce(operator.or_, (Q(description__icontains=word) for word in words_list))
#             if db_table == 'searcher_exploit':
#                 queryset = Exploit.objects.filter(query)
#             else:
#                 queryset = Shellcode.objects.filter(query)
#         except TypeError:
#             if db_table == 'searcher_exploit':
#                 queryset = Exploit.objects.all()
#             else:
#                 queryset = Shellcode.objects.all()
#     else:
#         if db_table == 'searcher_exploit':
#             queryset = Exploit.objects.all()
#         else:
#             queryset = Shellcode.objects.all()
#     if type_filter != 'All':
#         queryset = queryset.filter(type__exact=type_filter)
#     if platform_filter != 'All':
#         queryset = queryset.filter(platform__exact=platform_filter)
#     if author_filter != '':
#         queryset = queryset.filter(author__icontains=author_filter)
#     try:
#         queryset = queryset.filter(date__gte=start_date_filter)
#         queryset = queryset.filter(date__lte=end_date_filter)
#     except ValueError:
#         pass
#     if port_filter is not None and db_table == 'searcher_exploit':
#         queryset = queryset.filter(port__exact=port_filter)
#     elif port_filter is not None and db_table == 'searcher_shellcode':
#         queryset = Shellcode.objects.none()
#
#     queryset_std = search_vulnerabilities_for_text_input_advanced(search_text, db_table, type_filter, platform_filter,
#                                                                   author_filter, port_filter, start_date_filter,
#                                                                   end_date_filter)
#     queryset = queryset.union(queryset_std)
#
#     return highlight_keywords_in_description(words_list, queryset)
#
#
# def search_vulnerabilities_for_description_advanced(search_text, db_table):
#     """
#     If the search input contains a number of version, it calls 'search_vulnerabilities_version' method,
#     else it calls 'search_vulnerabilities_for_description'.
#     :param search_text: the search input.
#     :param db_table: the DB table in which we want to perform the search.
#     :return: a queryset containing all the search results that can be filtered with the filters selected by the user.
#     """
#     if str_is_num_version(str(search_text)) and str(search_text).__contains__(' ') \
#             and not str(search_text).__contains__('<'):
#         queryset = search_vulnerabilities_version(search_text, db_table)
#     else:
#         queryset = search_vulnerabilities_for_description(search_text, db_table)
#     return queryset


def search_vulnerabilities_for_text_input(word_list, db_table):
    """
    Perform a search in description based on characters contained by this attribute.
    This queryset can be joined with the search results based on the number of version.
    :param search_text: the search input.
    :param db_table: the DB table in which we want to perform the search.
    :return: a queryset containing the search results found with a search based on the characters contained by
                the attribute 'description'
    """
    word_list_num = []
    for word in word_list:
        if word.isnumeric():
            word_list.remove(word)
            word_list_num.append(' ' + word)
            word_list_num.append('/' + word)
        if word.__contains__('.'):
            word_list.remove(word)
            word_list_num.append(' ' + word)
            word_list_num.append('/' + word)
    try:
        session = start_session()
        if db_table == 'searcher_exploit':
            queryset = session.query(Exploit).filter(
                and_(Exploit.description.like('%' + word + '%') for word in word_list))
        else:
            queryset = session.query(Shellcode).filter(
                and_(Shellcode.description.like('%' + word + '%') for word in word_list))
        session.close()
        query_result_set = queryset2list(queryset)
    except TypeError:
        query_result_set = void_result_set()
    final_result_set = []
    try:
        for instance in query_result_set:
            for word in word_list_num:
                if str(instance.description).__contains__(word):
                    final_result_set.append(instance)
    except TypeError:
        pass
    return final_result_set


# def search_vulnerabilities_for_text_input_advanced(search_text, db_table, type_filter, platform_filter, author_filter,
#                                                    port_filter, start_date_filter, end_date_filter):
#     """
#     Perform a search based on characters contained by this attribute.
#     :param search_text: the search input.
#     :param db_table: the DB table in which we want to perform the search.
#     :param type_filter: the filter on the vulnerabilities' type.
#     :param platform_filter: the filter on the vulnerabilities' platform.
#     :param author_filter: the filter on the vulnerabilities' author.
#     :param port_filter: the filter on the exploits' port.
#     :param start_date_filter: the filter on the vulnerabilities' date (from).
#     :param end_date_filter: the filter on the vulnerabilities' date (to).
#     :return: a queryset containing all the search results.
#     """
#     queryset = search_vulnerabilities_for_text_input(search_text, db_table)
#     if type_filter != 'All':
#         queryset = queryset.filter(type__exact=type_filter)
#     if platform_filter != 'All':
#         queryset = queryset.filter(platform__exact=platform_filter)
#     if author_filter != '':
#         queryset = queryset.filter(author__icontains=author_filter)
#     try:
#         queryset = queryset.filter(date__gte=start_date_filter)
#         queryset = queryset.filter(date__lte=end_date_filter)
#     except ValueError:
#         pass
#     except ValidationError:
#         pass
#     if port_filter is not None and db_table == 'searcher_exploit':
#         queryset = queryset.filter(port__exact=port_filter)
#     elif port_filter is not None and db_table == 'searcher_shellcode':
#         queryset = Shellcode.objects.none()
#     return queryset
