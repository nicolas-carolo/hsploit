from HoundSploitBash.searcher.db_manager.session_manager import start_session
from HoundSploitBash.searcher.db_manager.models import Exploit, Shellcode
import os, sys
from tabulate import tabulate
from HoundSploitBash.console_manager.colors import W, O, R, G
from HoundSploitBash.searcher.engine.updates import is_db_update_available, is_hs_update_available, download_update, install_exploitdb_update,\
    get_latest_db_update_date


# Software information constants
SW_VERSION = '1.4.0 (Bash Version)'
RELEASE_DATE = '2019-09-28'
DEVELOPER = 'Nicolas Carolo'
LATEST_DB_UPDATE = get_latest_db_update_date()
LATEST_HS_COMMIT = "1.4.0: README.md and check on blank input"


def print_guide():
    print_ascii_art('Hound\nSploit')
    print(O + 'USAGE:' + W)
    print(tabulate([[G + 'Perform a search' + W, 'HoundSploitBash "[search text]"'],
                    [G + 'Show info about the exploit' + W, 'HoundSploitBash -ie [exploit\'s id]'],
                    [G + 'Show info about the shellcode' + W, 'HoundSploitBash -is [shellcode\'s id]'],
                    [G + 'Open the exploit\'s source code with nano' + W, 'HoundSploitBash -oe [exploit\'s id]'],
                    [G + 'Open the shellcode\'s source code with nano' + W,
                     'HoundSploitBash -os [shellcode\'s id]'],
                    [G + 'Show software information' + W, 'HoundSploitBash -v'],
                    [G + 'Check for software updates' + W, 'HoundSploitBash -u'],
                    [G + 'Check for database updates' + W, 'HoundSploitBash -udb'],
                    [G + 'Show help' + W, 'HoundSploitBash -help']],
                   [R + 'ACTION' + W, R + 'COMMAND LINE' + W], tablefmt='grid'))
    exit(0)


def print_software_information():
    print_ascii_art('Hound\nSploit')
    print(tabulate([[O + 'Version:' + W, SW_VERSION],
                    [O + 'Release date:' + W, RELEASE_DATE],
                    [O + 'Developer:' + W, DEVELOPER],
                    [O + 'Latest Database update:' + W, LATEST_DB_UPDATE]], tablefmt='grid'))
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
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/vulnerabilities/"
        os.system('nano ' + vulnerabilities_path + queryset[0].file)
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
        vulnerabilities_path = os.path.split(sys.executable)[0] + "/vulnerabilities/"
        os.system('nano ' + vulnerabilities_path + queryset[0].file)
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
    if is_hs_update_available(LATEST_HS_COMMIT):
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


def check_for_exploitdb_updates():
    latest_db_update_path = os.path.split(sys.executable)[0] + "/etc/latest_exploitdb_commit.txt"
    if is_db_update_available(latest_db_update_path):
        print('A new database update is available!')
        choice = input('Do you want to download and install it? (Y/N): ')
        if choice.upper() == 'Y' or choice.upper() == 'YES':
            install_exploitdb_update()
        elif choice.upper() == 'N' or choice.upper() == 'NO':
            exit(0)
        else:
            print('ERROR: Bad input! Choose yes (Y) or no (N)')
            check_for_updates()
    else:
        print('The database is up-to-date!')
    exit(0)
