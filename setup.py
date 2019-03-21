import os
import platform


def main():
    os.system('pip install --upgrade pip')

    try:
        import pymysql
    except ImportError:
        os.system('pip install pymysql')

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

    if platform.system() == 'Linux':
        print('Database configuration: insert the password for root@localhost when it is required')
        os.system('mysql -u root -p < sql_scripts/houndsploit_db_setup.sql')
        os.system('mysql -u root -p HOUNDSPLOIT < sql_scripts/files_exploits.sql')
        os.system('mysql -u root -p HOUNDSPLOIT < sql_scripts/files_shellcodes.sql')
        os.system('mysql -u root -p HOUNDSPLOIT < sql_scripts/files_exceptions.sql')
        os.system('python test_db_connection.py')
    elif platform.system() == 'Darwin':
        print('Database configuration: insert the password for root@localhost when it is required')
        os.system('/usr/local/mysql/bin/mysql -u root -p < sql_scripts/houndsploit_db_setup.sql')
        os.system('/usr/local/mysql/bin/mysql -u root -p HOUNDSPLOIT < sql_scripts/files_exploits.sql')
        os.system('/usr/local/mysql/bin/mysql -u root -p HOUNDSPLOIT < sql_scripts/files_shellcodes.sql')
        os.system('/usr/local/mysql/bin/mysql -u root -p HOUNDSPLOIT < sql_scripts/files_exceptions.sql')
    else:
        print('Sorry, the new automated database setup is not available for your OS!')
        print('Please use the old automated procedure you can find in the software documentation.')


if __name__ == "__main__":
    main()
