from searcher.db_manager.session_manager import start_session
from searcher.db_manager.models import Exploit, Shellcode
import os, sys
from tabulate import tabulate
from console_manager.colors import W, O, R, G
from searcher.engine.updates import is_update_available, download_update


# Software information constants
SW_VERSION = '1.2.0 (Bash Version)'
RELEASE_DATE = 'March 21, 2019'
DEVELOPER = 'Nicolas Carolo'
LAST_DB_UPDATE = 'March 15, 2019'


def print_guide():
    print_ascii_art('Hound\nSploit')
    print(O + 'USAGE:' + W)
    print(tabulate([[G + 'Perform a search' + W, 'python houndsploit.py "[search text]"'],
                    [G + 'Show info about the exploit' + W, 'python houndsploit.py -ie [exploit\'s id]'],
                    [G + 'Show info about the shellcode' + W, 'python houndsploit.py -is [shellcode\'s id]'],
                    [G + 'Open the exploit\'s source code with nano' + W, 'python houndsploit.py -oe [exploit\'s id]'],
                    [G + 'Open the shellcode\'s source code with nano' + W,
                     'python houndsploit.py -os [shellcode\'s id]'],
                    [G + 'Show software information' + W, 'python houndsploit.py -v'],
                    [G + 'Check for software updates' + W, 'python houndsploit.py -u'],
                    [G + 'Show help' + W, 'python houndsploit.py -help']],
                   [R + 'ACTION' + W, R + 'COMMAND LINE' + W], tablefmt='grid'))
    exit(0)


def print_software_information():
    print_ascii_art('Hound\nSploit')
    print(tabulate([[O + 'Version:' + W, SW_VERSION],
                    [O + 'Release date:' + W, RELEASE_DATE],
                    [O + 'Developer:' + W, DEVELOPER],
                    [O + 'Last Database update:' + W, LAST_DB_UPDATE]], tablefmt='grid'))
    exit(0)


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


def print_ascii_art(text_to_print):
    from colorama import init
    init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected
    from termcolor import cprint
    from pyfiglet import figlet_format

    cprint(figlet_format(text_to_print, font='starwars'),
           'yellow', attrs=['bold'])


def check_for_updates():
    if is_update_available():
        print('A new software update is available!')
        choice = input('Do you want to download it? (Y/N): ')
        if choice.upper() == 'Y' or choice.upper() == 'YES':
            download_update()
        elif choice.upper() == 'N' or choice.upper() == 'NO':
            exit(0)
        else:
            print('ERROR: Bad input! Choose yes (Y) or no (N)')
            check_for_updates()
    else:
        print('The software is up-to-date!')
    exit(0)
