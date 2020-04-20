import re
from hsploit.console_manager.colors import W, R

W_sub = '__WHITE__'   # white (normal)
R_sub = '__RED__'  # red


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
                    vulnerability.description = regex.sub(R_sub + keyword + W_sub, vulnerability.description)
    for vulnerability in vulnerabilities_list:
        vulnerability.description = str(vulnerability.description).replace("__RED__", R)
        vulnerability.description = str(vulnerability.description).replace("__WHITE__", W)

    return vulnerabilities_list
