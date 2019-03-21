from sqlalchemy.exc import InternalError, OperationalError
from searcher.db_manager.session_manager import start_session
from searcher.db_manager.models import Exploit, Shellcode
import os


def main():
    try:
        session = start_session()
        session.query(Exploit).count()
        session.query(Shellcode).count()
        print('Setup completed! Now you can run HoundSploit using the following command:')
        print('\t$ python houndsploit.py')
        exit(0)
    except InternalError:
        print('ERROR: The setup failed!')
        setup_error()
    except OperationalError:
        print('ERROR: The setup failed!')
        setup_error()


def setup_error():
    choice = input('Do you want to run setup again? (Y/N): ')
    if choice.upper() == 'Y' or choice.upper() == 'YES':
        os.system('python setup.py')
    elif choice.upper() == 'N' or choice.upper() == 'NO':
        exit(0)
    else:
        print('ERROR: Bad input! Choose yes (Y) or no (N)')
        setup_error()


if __name__ == "__main__":
    main()
