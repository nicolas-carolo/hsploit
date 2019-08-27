import zipfile
import requests
import re
import os

from searcher.engine.csv2sqlite import create_db


def is_update_available(repo, filename_last_commit):
    try:
        # repo = 'nicolas-carolo/HoundSploitBash'
        # './searcher/etc/last_hs_commit.txt'
        info_request = requests.get('https://api.github.com/repos/{0}/commits?per_page=1'.format(repo))
        commit = info_request.json()[0]["commit"]
        regex = re.search(r'\'message\': \'(?P<last_git_commit>[^\']*)\'', str(commit))
        try:
            last_git_commit = regex.group('last_git_commit')
            try:
                with open(filename_last_commit, 'r') as f:
                    content = f.readlines()
                    last_local_commit = ''.join(content)
                if str(last_local_commit) == str(last_git_commit):
                    return False
                else:
                    return True
            except FileNotFoundError:
                return True
        except AttributeError:
            return False
    except KeyError:
        return False


def download_update():
    os.system('wget https://github.com/nicolas-carolo/HoundSploitBash/archive/master.zip -O ~/HoundSploitBash.zip')
    print('The zip archive \'HoundSploitBash.zip\' has been saved in your home directory.')
    print('Download completed!')
    print('Remember to run setup.py before use HoundSploit again')
    exit(0)


def install_exploitdb_update():
    os.system('rm -fr ./searcher/vulnerabilities/*')
    if os.path.isfile("/hound_db.sqlite3"):
        os.system('rm ./hound_db.sqlite3')
    if os.path.isdir("exploitdb_temp"):
        os.system('rm -fr exploitdb_temp')
    os.system('wget https://github.com/offensive-security/exploitdb/archive/master.zip -O ./exploitdb.zip')
    os.system('mkdir exploitdb_temp')
    with zipfile.ZipFile("./exploitdb.zip", 'r') as zip_ref:
        zip_ref.extractall("exploitdb_temp")
    os.system('mv ./exploitdb_temp/exploitdb-master/exploits ./searcher/vulnerabilities/exploits')
    os.system('mv ./exploitdb_temp/exploitdb-master/shellcodes ./searcher/vulnerabilities/shellcodes')
    os.system('mv ./exploitdb_temp/exploitdb-master/files_exploits.csv ./csv')
    os.system('mv ./exploitdb_temp/exploitdb-master/files_shellcodes.csv ./csv')
    create_db()
    os.system('rm -fr exploitdb_temp')
    os.system('rm exploitdb.zip')
    print('The database has been updated successfully!')
