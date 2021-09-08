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


BOOLEAN_ARGS = ['nokeywords', 'notable', 'update', 'version', 'listsuggestions', 'help', 'outputfile']


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

    input_control(args_parsed)


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
            check_boolean_input('nokeywords', args_dict)
            perform_search(searched_text, "nokeywords", "")
        if args_dict['notable']:
            check_boolean_input('notable', args_dict)
            perform_search(searched_text, "notable", "")
        if args_dict['outputfile'] is not None:
            check_boolean_input('outputfile', args_dict)
            perform_search(searched_text, "file", args_dict['outputfile'])
        else:
            perform_search(searched_text, "standard", "")

    elif args_dict['search'] is None and args_dict['advancedsearch'] is not None:
        searched_text = args_dict['advancedsearch']
        print(searched_text)
        if args_dict['nokeywords']:
            check_boolean_input('nokeywords', args_dict)
            perform_advanced_search(searched_text, "nokeywords", "", "", "", "", "", "", "", "")
        if args_dict['notable']:
            check_boolean_input('notable', args_dict)
            perform_advanced_search(searched_text, "notable", "", "", "", "", "", "", "", "")
        if args_dict['outputfile'] is not None:
            check_boolean_input('outputfile', args_dict)
            perform_advanced_search(searched_text, "file", args_dict['outputfile'], "", "", "", "", "", "", "")
        else:
            perform_advanced_search(searched_text, "standard", "", "", "", "", "", "", "", "")
    else:
        print_guide()

def keyboard_exit():
    print()
    exit(0)