def check_userId():
    id_token = request.vars.userId

    decoded_token = auth.verify_id_token(id_token)
    user.id = decoded_token['uid']
    print("user id:" + user.id)
    return "ok"

def user_not_login_redirect():
    login_state = request.vars.state.lower().startswith('t')
    if not login_state:
        redirect(URL('default', 'login'))
