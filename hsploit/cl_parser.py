# -*- encoding: utf-8 -*-
# ADGraphGenerator v1.0.0
# An advanced command-line search engine for Exploit-DB
# Copyright © 2021, Nicolas Carolo.
# See /LICENSE for licensing information.

"""
Command Line Parsing Module for hsploit
:Copyright: © 2020, Nicolas Carolo.
:License: BSD (see /LICENSE).
"""

__all__ = ()

import argparse


def parse_args(args):
    """
    This function parses the arguments which have been passed from the command
    line, these can be easily retrieved for example by using "sys.argv[1:]".
    It returns a parser object as with argparse.
    Arguments:
    args -- the list of arguments passed from the command line as the sys.argv
            format
    Returns: a parser with the provided arguments, which can be used in a
            simpler format
    """
    parser = argparse.ArgumentParser(prog='hsploit',
                                     description='An advanced command-line search engine for Exploit-DB',
                                     add_help=False)

    requiredNamed = parser.add_argument_group('required arguments')
    requiredNamed.add_argument(
        "-s", "--search",
        help="The searched text",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-sad", "--advancedsearch",
        help="The searched text",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-of", "--outputfile",
        help="The output file",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-oe", "--openexploit",
        help="Open an exploit",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-os", "--openshellcode",
        help="Open a shellcode",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-ie", "--infoexploit",
        help="Info about an exploit",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-is", "--infoshellcode",
        help="Info about a shellcode",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-as", "--addsuggestion",
        help="Add a suggestion",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-rs", "--removesuggestion",
        help="Remove a suggestion",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-cpe", "--copyexploit",
        help="Copy an exploit to a file",
        type=str,
        required=False
    )
    requiredNamed.add_argument(
        "-cps", "--copyshellcode",
        help="Copy a shellcode to a file",
        type=str,
        required=False
    )
    parser.add_argument(
       "-nk", "--nokeywords",
        help="No keywords highlighting",
        action="store_true",
        required=False
    )
    parser.add_argument(
       "-nt", "--notable",
        help="Search results not shown into a table",
        action="store_true",
        required=False
    )
    parser.add_argument(
       "-u", "--update",
        help="Check for updates",
        action="store_true",
        required=False
    )
    parser.add_argument(
       "-v", "--version",
        help="About",
        action="store_true",
        required=False
    )
    parser.add_argument(
       "-h", "--help",
        help="Help",
        action="store_true",
        required=False
    )
    parser.add_argument(
       "-ls", "--listsuggestions",
        help="List suggestions",
        action="store_true",
        required=False
    )
    parser.add_argument(
       "-lb", "--listbookmarks",
        help="List bookmarks",
        action="store_true",
        required=False
    )


    return parser.parse_args(args)