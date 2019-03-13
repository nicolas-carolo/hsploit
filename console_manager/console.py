from searcher.db_manager.session_manager import start_session
from searcher.db_manager.models import Exploit, Shellcode
import os
from tabulate import tabulate
from console_manager.colors import W, O


def open_exploit(id):
    """
    Open the exploit identified by the id.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        os.system('nano ' + './searcher/vulnerabilities/' + queryset[0].file)
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)


def open_shellcode(id):
    """
    Open the shellcode identified by the id.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        os.system('nano ' + './searcher/vulnerabilities/' + queryset[0].file)
    except IndexError:
        print('ERROR: Shellcode not found!')
    return exit(0)


def show_exploit_info(id):
    """
    Show the information about the exploit identified by the id.
    :param id: the exploit's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Exploit).filter(Exploit.id == id)
    session.close()
    try:
        exploit = queryset[0]
        if exploit.port:
            print(tabulate([[O + 'DESCRIPTION:' + W, exploit.description], [O + 'AUTHOR:' + W, exploit.author],
                            [O + 'FILE:' + W, exploit.file], [O + 'DATE:' + W, exploit.date],
                            [O + 'TYPE:' + W, exploit.type], [O + 'PLATFORM:' + W, exploit.platform],
                            [O + 'PORT:' + W, exploit.port]], tablefmt='grid'))
        else:
            print(tabulate([[O + 'DESCRIPTION:' + W, exploit.description], [O + 'AUTHOR:' + W, exploit.author],
                            [O + 'FILE:' + W, exploit.file], [O + 'DATE:' + W, exploit.date],
                            [O + 'TYPE:' + W, exploit.type], [O + 'PLATFORM:' + W, exploit.platform]], tablefmt='grid'))
    except IndexError:
        print('ERROR: Exploit not found!')
    return exit(0)


def show_shellcode_info(id):
    """
    Show the information about the shellcode identified by the id.
    :param id: the shellcode's id.
    :return: exit the program.
    """
    session = start_session()
    queryset = session.query(Shellcode).filter(Shellcode.id == id)
    session.close()
    try:
        shellcode = queryset[0]
        print(tabulate([[O + 'DESCRIPTION:' + W, shellcode.description], [O + 'AUTHOR:' + W, shellcode.author],
                        [O + 'FILE:' + W, shellcode.file], [O + 'DATE:' + W, shellcode.date],
                        [O + 'TYPE:' + W, shellcode.type], [O + 'PLATFORM:' + W, shellcode.platform]], tablefmt='grid'))
    except IndexError:
        print('ERROR: Shellcode not found!')
    return exit(0)
