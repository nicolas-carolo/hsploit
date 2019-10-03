import re
from HoundSploitBash.console_manager.colors import W, R


def highlight_keywords_in_description(keywords_list, vulnerabilities_list):
    """
    Highlight searched keywords in the 'description' field.
    :param keywords_list: the list of keywords typed by the user in the search field.
    :param vulnerabilities_list: the list containing all the search results.
    :return: a queryset containing all search results formatted with HTML code for highlighting searched keywords.
    """
    for vulnerability in vulnerabilities_list:
        for keyword in keywords_list:
            if keyword != '<':
                description = str(vulnerability.description).upper()
                if description.__contains__(keyword):
                    regex = re.compile(re.escape(keyword), re.IGNORECASE)
                    vulnerability.description = regex.sub(R + keyword + W, vulnerability.description)
    return vulnerabilities_list
