import os


def main():
    if not os.path.isfile('houndsploit.py'):
        print("Change the current working directory to the directory of \'houndsploit.py\'"
              " for executing \'setup.py\'.")
        exit(0)

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

    from searcher.engine.updates import install_exploitdb_update
    install_exploitdb_update()


if __name__ == "__main__":
    main()
