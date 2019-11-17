import re


def str_contains_numbers(str):
    """
    Check if a string contains at least one number.
    :param str: the string to check.
    :return: true if the string contains at least one number, false else.
    """
    return bool(re.search(r'\d', str))


def str_is_num_version(str):
    """
    Check if a string contains a number of version.
    :param str: the string to check.
    :return: true if the string contains a number of version, false else.
    """
    return bool(re.search(r'\d+((\.\d+)+)?', str))


def str_contains_num_version_range(str):
    """
    Check if a string contains a range of number version.
    :param str: the string to check.
    :return: true if the string contains a a range of number version, false else.
    """
    return bool(re.search(r'\d+((\.\d+)+)? < \d+((\.\d+)+)?', str))


def str_contains_num_version_range_with_x(str):
    """
    Check if a string contains a range of number version with x.
    :param str: the string to check.
    :return: true if the string contains a a range of number version with x, false else.
    """
    return bool(re.search(r'\d+((\.\d+)+)?(\.x)? < \d+((\.\d+)+)?(\.x)?', str))


def get_vulnerability_extension(vulnerability_file):
    """
    Get the extension of the vulnerability passed as parameter.
    :param vulnerability_file: the vulnerability we want to get its extension.
    :return: the extension of the vulnerability passed as parameter.
    """
    regex = re.search(r'\.(?P<extension>\w+)', vulnerability_file)
    extension = '.' + regex.group('extension')
    return extension
