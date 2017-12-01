import sys
import requests

if len(sys.argv) == 2:
    USER_LOGIN = sys.argv[1]
else:
    print("Invalid number of arguments, enter xlogin only")
    exit(0)

UID = "79739a0b9b8176755fbd38888eedd32450cbdbea9138d66e4470e0de5218caeb"
SECRET = "c28b45d82f1efe060a89ee56909f0cedb0e9a95b7e0057ef6f6f3a1c5a60db20"
AUTH_URL = "https://api.intra.42.fr/oauth/token"
USER_INFO_URL = "https://api.intra.42.fr/v2/users/{}/?access_token={}" #"https://api.intra.42.fr/v2/users/{}"

#forming two requests POST to authorise, GET to Parse info. Than return json() object to print id, name, etc.

def main():

    data = "grant_type=client_credentials&client_id={}&client_secret={}" #forms request data.
    auth = requests.post(AUTH_URL, data.format(UID, SECRET))
    token = auth.json()['access_token'] #auth returns binary with code and ather stuff. json['accses_token'] contain key.
    #print(token)
    #user_info = requests.get(url=USR_INFO_URL.format(USER_LOGIN), headers={'Authorization': token}) безопасный способ авторизации
    user_info = requests.get(url=USER_INFO_URL.format(USER_LOGIN, token))
    if user_info.status_code: #check response status (should return .json() only if 500) but it's not (
        return user_info.json()
    else:
        print(user_info.status_code)
        exit(0)

if __name__ == "__main__":

    user_info = main()
    if not user_info:
        print("No such user: %s" % (USER_LOGIN))
    else:
        print("ID: %s, FULL NAME: %s" % (user_info['id'], user_info['displayname']))
        print('Choosen in %s, %s ' % (user_info['pool_month'],user_info['pool_year']))
        print('Level %s most experienced in %s skill level: %s' % (user_info['cursus_users'][0]['level'], user_info['cursus_users'][0]['skills'][0]['name'], user_info['cursus_users'][0]['skills'][0]['level']))
        projects_users = user_info['projects_users']
        finished_projects = 0
        for project in projects_users:
            if project['status'] == 'finished':
                finished_projects += 1
        print("Finished %d projects so far" % (finished_projects))
        titles = user_info['titles']
        if not titles:
            print("Haven't selected any title")
        else:
            print("Self-proclaimed himself as %s" %(titles[0]['name'].replace('%login', USER_LOGIN)))