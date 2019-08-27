import os


def main():
    os.system('pip install --upgrade pip')

    try:
        import sqlalchemy
    except ImportError:
        os.system('pip install sqlalchemy')

    try:
        import colorama
    except ImportError:
        os.system('pip install colorama')

    try:
        import pyfiglet
    except ImportError:
        os.system('pip install pyfiglet')

    try:
        import tabulate
    except ImportError:
        os.system('pip install tabulate')

    try:
        import termcolor
    except ImportError:
        os.system('pip install termcolor')

    try:
        import requests
    except ImportError:
        os.system('pip install requests')


if __name__ == "__main__":
    main()
