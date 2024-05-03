import requests

session = requests.Session

def login(username, password, print='no'):

    login_data = {
        'pid': '65edCTyg',
        'identity': username,
        'password': password
    }
    result = session.post('https://api.codemao.cn/tiger/v3/web/accounts/login',
                          json=login_data)
    code = str(result.status_code)
    global get

    def get():
        return (result.text)

    if code == '201':
        if print == 'yes':
            print("Login Successful[201]")
        else:
            return ('201')
    else:
        if print == 'yes':
            print("Login Failed[" + code + "]")
        else:
            return (code)


def logout(print='no'):

    result = session.post(
        'https://api.codemao.cn/tiger/v3/web/accounts/loginout')
    global get

    def get():
        return (result.text)

    if result.status_code == 200:
        if print == 'yes':
            print("Logout Successful[204]")
        else:
            return ('204')
    else:
        if print == 'yes':
            print("Logout Failed[" + str(result.status_code) + "]")
        else:
            return (str(result.status_code))


def usrinfo(kind, inputstr, inputint: int, print='no'):
    if kind == 'nick':

        change = {'nickname': inputstr}
        result = session.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'full':

        change = {'fullname': inputstr}
        result = session.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'desc':

        change = {'description': inputstr}
        result = session.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'sex':

        change = {'sex': inputint}
        result = session.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'birth':

        change = {'birthday	': inputint}
        result = session.patch("/tiger/v3/web/accounts/info", data=change)

    if kind == 'avat':

        change = {'avatar_url': inputstr}
        result = session.patch("/tiger/v3/web/accounts/info", data=change)
    global get

    def get():
        return (result.text)

    if result.status_code == 204:
        if print == 'yes':
            print("Change Info Successful[204]")
        else:
            return ('204')
    else:
        if print == 'yes':
            print("Change Info Failed[" + str(result.status_code) + "]")
        else:
            return (str(result.status_code))


def psc(old_password, new_password, print='no'):

    change = {
        'old_password': old_password,
        'password': new_password,
        'confirm_password': new_password
    }
    result = session.patch("/tiger/v3/web/accounts/info", data=change)

    global get
    def get():
        return (result.text)

    if result.status_code == 204:
        if print == 'yes':
            print("Change Password Successful[204]")
        else:
            return ('204')
    else:
        if print == 'yes':
            print("Change Password Failed[" + str(result.status_code) + "]")
        else:
            return (str(result.status_code))


def like(workid, print='no'):

    result = session.post("https://api.codemao.cn/nemo/v2/works/" + workid +
                          "/like")
    global get

    def get():
        return (result.text)

    if result.status_code == 201:
        if print == 'yes':
            print("Like Successful[201]")
        else:
            return ('201')
    else:
        if print == 'yes':
            print("Like Failed[" + str(result.status_code) + "]")
        else:
            return (str(result.status_code))


def coll(workid, print='no'):

    result = session.post("https://api.codemao.cn/nemo/v2/works/" + workid +
                          "/collection")
    global get

    def get():
        return (result.text)

    if result.status_code == 201:
        if print == 'yes':
            print("Collection Successful[201]")
        else:
            return ('201')
    else:
        if print == 'yes':
            print("Collection Failed[" + str(result.status_code) + "]")
        else:
            return (str(result.status_code))


def fork(workid, print='no'):

    result = session.post("https://api.codemao.cn/nemo/v2/works/" + workid +
                          "/fork")
    global get

    def get():
        return (result.text)

    if result.status_code == 201:
        if print == 'yes':
            print("Fork Successful[201]")
        else:
            return ('201')
    else:
        if print == 'yes':
            print("Fork Failed[" + str(result.status_code) + "]")
        else:
            return (str(result.status_code))


def follow(userid, print='no'):

    result = session.post("https://api.codemao.cn/nemo/v2/user/" + userid +
                          "/follow")
    global get
    def get():
        return (result.text)

    if result.status_code == 204:
        if print == 'yes':
            print("Fork Successful[204]")
        else:
            return ('204')
    else:
        if print == 'yes':
            print("Fork Failed[" + str(result.status_code) + "]")
        else:
            return (str(result.status_code))
