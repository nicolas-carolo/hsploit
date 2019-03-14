import requests
import re
import os


def is_update_available():
    try:
        repo = 'nicolas-carolo/HoundSploitBash'
        info_request = requests.get('https://api.github.com/repos/{0}/commits?per_page=1'.format(repo))
        commit = info_request.json()[0]["commit"]
        regex = re.search(r'\'message\': \'(?P<last_git_commit>[^\']*)\'', str(commit))
        try:
            last_git_commit = regex.group('last_git_commit')
            try:
                with open('./searcher/etc/last_commit.txt', 'r') as f:
                    content = f.readlines()
                    last_local_commit = ''.join(content)
                # print(last_local_commit)
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


def git_pull():
    os.system('git pull')
    print('Remember to update manually the Database!')
    exit(0)
