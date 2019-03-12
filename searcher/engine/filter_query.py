from pkg_resources import parse_version
from searcher.engine.version_comparator import get_num_version_with_comparator, get_num_version,\
    is_in_version_range_with_x, is_equal_with_x, is_in_version_range, is_lte_with_comparator_x
from searcher.engine.string import str_contains_num_version_range_with_x, str_contains_num_version_range
from searcher.db_manager.result_set import exclude


def filter_exploits_without_comparator(exploit, num_version, software_name, final_result_set):
    if not exploit.description.__contains__('.x'):
        # exclude the exploit from results table if the number of version is not equal and contains 'x'
        try:
            if parse_version(num_version) == parse_version(get_num_version(software_name, exploit.description)):
                final_result_set.append(exploit)
        except TypeError:
            pass
    else:
        # exclude the exploit from results table if the number of version is not equal and not contains 'x'
        try:
            if is_equal_with_x(num_version, get_num_version(software_name, exploit.description)):
                final_result_set.append(exploit)
        except TypeError:
            pass
    return final_result_set
