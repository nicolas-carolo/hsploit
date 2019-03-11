from pkg_resources import parse_version
from searcher.engine.version_comparator import get_num_version_with_comparator, get_num_version,\
    is_in_version_range_with_x, is_equal_with_x, is_in_version_range, is_lte_with_comparator_x
from searcher.engine.string import str_contains_num_version_range_with_x, str_contains_num_version_range
from searcher.db_manager.result_set import exclude
from searcher.db_manager.result_set import print_instances


def filter_exploits_without_comparator(exploit, num_version, software_name, result_set):
    """
    Remove a exploit by the queryset if it has a number of version that does not match the value passed by the user.
    This method is used only for exploits that have not '<' char in the description.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                    the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the exploit matches the number of version searched by the user,
                the original queryset without the exploit if it does not.
    """
    if not exploit.description.__contains__('.x'):
        # exclude the exploit from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) != parse_version(get_num_version(software_name, exploit.description)):
                result_set = exclude(result_set, exploit.description)
        except TypeError:
            result_set = exclude(result_set, exploit.description)
    else:
        # exclude the exploit from results table if the number of version is not equal and not contains 'x'
        try:
            if not is_equal_with_x(num_version, get_num_version(software_name, exploit.description)):
                result_set = exclude(result_set, exploit.description)
        except TypeError:
            result_set = exclude(result_set, exploit.description)
    return result_set


def filter_exploits_with_comparator(exploit, num_version, software_name, result_set):
    """
    Remove a exploit by the queryset if it has a number of version that does not match the value passed by the user.
    This method is used only for exploits containing '<' char in the description.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                    the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the exploit matches the number of version searched by the user,
                the original queryset without the exploit if it does not.
    """
    if not exploit.description.__contains__('.x'):
        result_set = filter_exploits_with_comparator_and_without_x(exploit, num_version, software_name, result_set)
    else:
        result_set = filter_exploits_with_comparator_and_x(exploit, num_version, software_name, result_set)
    return result_set


def filter_shellcodes_without_comparator(shellcode, num_version, software_name, result_set):
    """
    Remove a shellcode by the queryset if it has a number of version that does not match the value passed by the
    user.
    This method is used only for shellcodes that have not '<' char in the description.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the shellcode matches the number of version searched by the user,
                the original queryset without the shellcode if it does not.
    """
    if not shellcode.description.__contains__('.x'):
        # exclude the shellcode from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) != parse_version(get_num_version(software_name, shellcode.description)):
                result_set = exclude(result_set, shellcode.description)
        except TypeError:
            result_set = exclude(result_set, shellcode.description)
    else:
        # exclude the shellcode from results table if the number of version is not equal and not contains 'x'
        try:
            if not is_equal_with_x(num_version, get_num_version(software_name, shellcode.description)):
                result_set = exclude(result_set, shellcode.description)
        except TypeError:
            result_set = exclude(result_set, shellcode.description)
    return result_set


def filter_shellcodes_with_comparator(shellcode, num_version, software_name, result_set):
    """
    Remove a shellcode by the queryset if it has a number of version that does not match the value passed by the
    user.
    This method is used only for shellcodes containing '<' char in the description.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the shellcode matches the number of version searched by the user,
                the original queryset without the shellcode if it does not.
    """
    if not shellcode.description.__contains__('.x'):
        result_set = filter_shellcodes_with_comparator_and_without_x(shellcode, num_version, software_name, result_set)
    else:
        result_set = filter_exploits_with_comparator_and_x(shellcode, num_version, software_name, result_set)
    return result_set


def filter_exploits_with_comparator_and_without_x(exploit, num_version, software_name, result_set):
    """
    Remove a exploit by the queryset if it has a number of version that does not match the value passed by the
    user.
    This method is used only for exploits containing '<' char in the description and that does not contain
    'x' char in the number of version.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the exploit matches the number of version searched by the user,
                the original queryset without the exploit if it does not.
    """
    if str_contains_num_version_range(str(exploit.description)):
        if not is_in_version_range(num_version, software_name, exploit.description):
            result_set = exclude(result_set, exploit.description)
    else:
        try:
            if parse_version(num_version) > parse_version(
                    get_num_version_with_comparator(software_name, exploit.description)):
                result_set = exclude(result_set, exploit.description)
        except TypeError:
            result_set = exclude(result_set, exploit.description)
    return result_set


def filter_exploits_with_comparator_and_x(exploit, num_version, software_name, result_set):
    """
    Remove a exploit by the queryset if it has a number of version that does not match the value passed by the
    user.
    This method is used only for exploits containing '<' char in the description and that contain
    'x' char in the number of version.
    :param exploit: the exploit we have to check if it has a number of version that matches the value passed by
                    the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the exploit matches the number of version searched by the user,
                the original queryset without the exploit if it does not.
    """
    if str_contains_num_version_range_with_x(str(exploit.description)):
        if not is_in_version_range_with_x(num_version, software_name, exploit.description):
            result_set = exclude(result_set, exploit.description)
    else:
        try:
            if not is_lte_with_comparator_x(num_version, software_name, exploit.description):
                result_set = exclude(result_set, exploit.description)
        except TypeError:
            result_set = exclude(result_set, exploit.description)
    return result_set


def filter_shellcodes_with_comparator_and_without_x(shellcode, num_version, software_name, result_set):
    """
    Remove a shellcode by the queryset if it has a number of version that does not match the value passed by the
    user.
    This method is used only for shellcodes containing '<' char in the description and that does not contain
    'x' char in the number of version.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the shellcode matches the number of version searched by the user,
                the original queryset without the shellcode if it does not.
    """
    if str_contains_num_version_range(str(shellcode.description)):
        if not is_in_version_range(num_version, software_name, shellcode.description):
            result_set = exclude(result_set, shellcode.description)
    else:
        try:
            if parse_version(num_version) > parse_version(
                    get_num_version_with_comparator(software_name, shellcode.description)):
                result_set = exclude(result_set, shellcode.description)
        except TypeError:
            result_set = exclude(result_set, shellcode.description)
    return result_set


def filter_shellcodes_with_comparator_and_x(shellcode, num_version, software_name, result_set):
    """
    Remove a shellcode by the queryset if it has a number of version that does not match the value passed by the
    user.
    This method is used only for shellcodes containing '<' char in the description and that contain
    'x' char in the number of version.
    :param shellcode: the shellcode we have to check if it has a number of version that matches the value passed by
                        the user.
    :param num_version: the number of version searched by the user.
    :param software_name: the name of the software searched by the user.
    :param queryset: the queryset we have to filter.
    :return: the original queryset if the shellcode matches the number of version searched by the user,
                the original queryset without the shellcode if it does not.
    """
    if str_contains_num_version_range_with_x(str(shellcode.description)):
        if not is_in_version_range_with_x(num_version, software_name, shellcode.description):
            result_set = exclude(result_set, shellcode.description)
    else:
        try:
            if not is_lte_with_comparator_x(num_version, software_name, shellcode.description):
                result_set = exclude(result_set, shellcode.description)
        except TypeError:
            result_set = exclude(result_set, shellcode.description)
    return result_set
