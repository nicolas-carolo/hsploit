import re
from hsploit.searcher.db_manager.models import Bookmark, Exploit, Shellcode
from hsploit.searcher.db_manager.session_manager import start_session
from hsploit.searcher.db_manager.result_set import queryset2list


def check_file_existence(filename):
    try:
        f = open(filename)
        f.close()
        return True
    except IOError:
        return False

def get_vulnerability_extension(vulnerability_file):
    """
    Get the extension of the vulnerability passed as parameter.
    :param vulnerability_file: the vulnerability we want to get its extension.
    :return: the extension of the vulnerability passed as parameter.
    """
    regex = re.search(r'\.(?P<extension>\w+)', vulnerability_file)
    extension = '.' + regex.group('extension')
    return extension


def check_vulnerability_existence(vulnerability_id, vulnerability_class):
    session = start_session()
    if vulnerability_class == "exploit":
        queryset = session.query(Exploit).filter(Exploit.id == vulnerability_id)
    else:
        queryset = session.query(Shellcode).filter(Shellcode.id == vulnerability_id)
    results_list = queryset2list(queryset)
    if len(results_list) == 0:
        session.close()
        return False
    else:
        session.close()
        return True