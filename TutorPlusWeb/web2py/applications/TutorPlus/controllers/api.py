def check_userId():
    id_token = request.vars.userId

    decoded_token = auth.verify_id_token(id_token)
    user.id = decoded_token['uid']
    print("user id:" + user.id)
    return "ok"