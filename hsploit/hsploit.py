"""Main module."""
__all__ = ()

import sys
import os
from os import path
from hsploit.cl_parser import parse_args
from hsploit.console_manager.colors import O, W, R
from hsploit.console_manager.console import print_guide, open_exploit, open_shellcode, show_exploit_info,\
    show_shellcode_info,print_software_information, copy_exploit, copy_shellcode, check_for_updates, perform_search,\
    print_suggestions_list, add_suggestion, delete_suggestion, perform_advanced_search
from hsploit.searcher.engine.csv2sqlite import create_db
from hsploit.searcher.engine.updates import install_updates, migrate_to_new_installation


BOOLEAN_ARGS = ['nokeywords', 'notable', 'update', 'version', 'listsuggestions', 'help']


def main(args=None):
    """Main routine of hsploit."""
    init_path = os.path.expanduser("~") + "/.HoundSploit"
    if not path.exists(init_path):
        migrate_to_new_installation()
        print_guide()
    if not os.path.isfile(init_path + "/hound_db.sqlite3"):
        install_updates()
        create_db()

    
    args_parsed = parse_args(sys.argv[1:])

    base_searched_text = args_parsed.search
    advanced_searched_text = args_parsed.advancedsearch
    no_keywords = args_parsed.nokeywords
    no_table = args_parsed.notable
    output_file = args_parsed.outputfile
    update = args_parsed.update

    input_control(args_parsed)

    """
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
    """


def input_control(args_parsed):
    args_dict = {}
    for arg in vars(args_parsed):
        args_dict[arg] = getattr(args_parsed, arg)
    print(args_dict)
    check_first_command(args_dict)


def check_first_command(args_dict):
    if args_dict['search'] is not None or args_dict['advancedsearch'] is not None:
        check_search_command(args_dict)
    elif args_dict['update']:
        check_boolean_input('update', args_dict)
        check_for_updates()
    elif args_dict['version']:
        check_boolean_input('version', args_dict)
        print_software_information()
    elif args_dict['listsuggestions']:
        check_boolean_input('listsuggestions', args_dict)
        print_suggestions_list()
    elif args_dict['openexploit']:
        open_exploit(args_dict['openexploit'])
    elif args_dict['openshellcode']:
        open_shellcode(args_dict['openshellcode'])
    elif args_dict['infoexploit']:
        show_exploit_info(args_dict['infoexploit'])
    elif args_dict['infoshellcode']:
        show_shellcode_info(args_dict['infoshellcode'])
    elif args_dict['addsuggestion']:
        add_suggestion(args_dict['addsuggestion'])
    elif args_dict['removesuggestion']:
        delete_suggestion(args_dict['removesuggestion'])
    elif args_dict['copyexploit']:
        check_copy_command('cpe', args_dict)
    elif args_dict['copyshellcode']:
        check_copy_command('cps', args_dict)
    else:
        print_guide()


def check_boolean_input(cmd, args_dict):
    false_boolean_args = BOOLEAN_ARGS
    false_boolean_args.remove(cmd)
    for key in false_boolean_args:
        if args_dict[key]:
            print_guide()


def check_copy_command(cmd, args_dict):
    if args_dict['outputfile'] is None:
        print_guide()
    else:
        if cmd == 'cpe':
            copy_exploit(args_dict['copyexploit'], args_dict['outputfile'])
        elif cmd == 'cps':
            copy_shellcode(args_dict['copyshellcode'], args_dict['outputfile'])
        else:
            print_guide()


def check_search_command(args_dict):
    if args_dict['search'] is not None and args_dict['advancedsearch'] is None:
        searched_text = args_dict['search']
        if args_dict['nokeywords']:
            perform_search(searched_text, "nokeywords", "")
        if args_dict['notable']:
            perform_search(searched_text, "notable", "")
        if args_dict['outputfile'] is not None:
            perform_search(searched_text, "file", args_dict['outputfile'])
        else:
            perform_search(searched_text, "standard", "")

    elif args_dict['search'] is None and args_dict['advancedsearch'] is not None:
        searched_text = args_dict['advancedsearch']
        print(searched_text)
        if args_dict['nokeywords']:
            perform_advanced_search(searched_text, "nokeywords", "", "", "", "", "", "", "", "")
        if args_dict['notable']:
            perform_advanced_search(searched_text, "notable", "", "", "", "", "", "", "", "")
        if args_dict['outputfile'] is not None:
            perform_advanced_search(searched_text, "file", args_dict['outputfile'], "", "", "", "", "", "", "")
        else:
            perform_advanced_search(searched_text, "standard", "", "", "", "", "", "", "", "")

def keyboard_exit():
    print()
    exit(0)