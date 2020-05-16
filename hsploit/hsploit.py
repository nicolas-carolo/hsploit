"""Main module."""
__all__ = ()

import sys
import os
from os import path
from hsploit.console_manager.colors import O, W, R
from hsploit.console_manager.console import print_guide, open_exploit, open_shellcode, show_exploit_info,\
    show_shellcode_info,print_software_information, copy_exploit, copy_shellcode, check_for_updates, perform_search,\
    print_suggestions_list, add_suggestion, delete_suggestion, perform_advanced_search
from hsploit.searcher.engine.csv2sqlite import create_db
from hsploit.searcher.engine.updates import install_updates, migrate_to_new_installation


def main(args=None):
    """Main routine of hsploit."""
    init_path = os.path.expanduser("~") + "/.HoundSploit"
    if not path.exists(init_path):
        print("OK")
        migrate_to_new_installation()
        print_guide()
    if not os.path.isfile(init_path + "/hound_db.sqlite3"):
        install_updates()
        create_db()

    if args is None:
        args = sys.argv[1:]

    if args.__len__() == 0 or args[0] == '-help' or str(args[0]).isspace() or str(args[0]) == "":
        print_guide()

    if args[0] == '-u':
        check_for_updates()

    if args[0] == '-v':
        print_software_information()
    
    if args[0] == '-ls':
        print_suggestions_list()

    if args[0] == '-oe' and not args[1] is None:
        open_exploit(args[1])

    if args[0] == '-os' and not args[1] is None:
        open_shellcode(args[1])

    if args[0] == '-ie' and not args[1] is None:
        show_exploit_info(args[1])

    if args[0] == '-is' and not args[1] is None:
        show_shellcode_info(args[1])

    if args[0] == '-as' and not args[1] is None:
        try:
            add_suggestion(args[1])
        except KeyboardInterrupt:
            keyboard_exit()

    if args[0] == '-rs' and not args[1] is None:
        try:
            delete_suggestion(args[1])
        except KeyboardInterrupt:
            keyboard_exit()
    
    if (args[0] == '-cps' or args[0] == '-cpe') and len(args) < 3:
        print(R + 'ERROR: ' + W + "\'-cps\' and \'-cpe\' options require three arguments")
        exit(0)
    else:
        if args[0] == '-cpe' and not args[1] is None and not args[2] is None:
            id = args[1]
            dst = args[2]
            copy_exploit(id, dst)

        if args[0] == '-cps' and not args[1] is None and not args[2] is None:
            id = args[1]
            dst = args[2]
            copy_shellcode(id, dst)       
    

    try:
        if len(args) == 2 and args[0] == '-s':
            perform_search(args[1], "standard", "")
        elif len(args) == 3 and args[0] == '-s' and args[1] == '--nokeywords' and not (str(args[2]).isspace() or str(args[2]) == ""):
            perform_search(args[2], "nokeywords", "")
        elif len(args) == 3 and args[0] == '-s' and args[1] == '--notable' and not (str(args[2]).isspace() or str(args[2]) == ""):
            perform_search(args[2], "notable", "")
        elif len(args) == 4 and args[0] == '-s' and args[1] == '--file' and not (str(args[2]).isspace() or str(args[2]) == "") and not (str(args[3]).isspace() or str(args[3]) == ""):
            perform_search(args[3], "file", args[2])
    except KeyboardInterrupt:
            keyboard_exit()

    
    try:
        if len(args) == 2 and args[0] == '-sad':
            perform_advanced_search(args[1], "standard", "", "", "", "", "", "", "", "")
        elif len(args) == 3 and args[0] == '-sad' and args[1] == '--nokeywords' and not (str(args[2]).isspace() or str(args[2]) == ""):
            perform_advanced_search(args[2], "nokeywords", "", "", "", "", "", "", "", "")
        elif len(args) == 3 and args[0] == '-sad' and args[1] == '--notable' and not (str(args[2]).isspace() or str(args[2]) == ""):
            perform_advanced_search(args[2], "notable", "", "", "", "", "", "", "", "")
        elif len(args) == 4 and args[0] == '-sad' and args[1] == '--file' and not (str(args[2]).isspace() or str(args[2]) == "") and not (str(args[3]).isspace() or str(args[3]) == ""):
            perform_advanced_search(args[3], "file", args[2], "", "", "", "", "", "", "")
    except KeyboardInterrupt:
            keyboard_exit()

    print_guide()


def keyboard_exit():
    print()
    exit(0)