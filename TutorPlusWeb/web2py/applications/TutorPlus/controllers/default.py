# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# This is a sample controller
# this file is released under public domain and you can use without limitations
# -------------------------------------------------------------------------

# ---- example index page ----
def index():
    # check if the request contains userId
    # if "userId" in request.vars:
    #     # if contains put it into user.id
    #     id_token = request.vars.userId
    #     decoded_token = auth.verify_id_token(id_token)
    #     user.id = decoded_token['uid']
    #     redirect(URL('default', 'index'))
    # else:
    #     # if not contains, then redirects to login page
    #     redirect(URL('default', 'login'))
    #if request.vars.state is not None:
    #    login_state = request.vars.state.lower().startswith('t')
    #    if not login_state:
    #        redirect(URL('default', 'login'))
    return dict()

def login():
    return dict()


# ---- API (example) -----
# @auth.requires_login()
# def api_get_user_email():
#     if not request.env.request_method == 'GET': raise HTTP(403)
#     return response.json({'status':'success', 'email':auth.user.email})
#
# # ---- Smart Grid (example) -----
# @auth.requires_membership('admin') # can only be accessed by members of admin groupd
# def grid():
#     response.view = 'generic.html' # use a generic view
#     tablename = request.args(0)
#     if not tablename in db.tables: raise HTTP(403)
#     grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=False)
#     return dict(grid=grid)

# ---- Embedded wiki (example) ----
def wiki():
    auth.wikimenu()  # add the wiki to the menu
    return auth.wiki()


# ---- Action for login/register/etc (required for auth) -----
def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


# ---- action to server uploaded static content (required) ---
@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)

'''
def signup():
    # Use a service account
    firebaseKeyPath = '../private/tutorPlusKey.json'
    cred = credentials.Certificate(firebaseKeyPath)
    firebase_admin.initialize_app(cred)

    db = firestore.client()

    user_email = request.vars['user_email'].decode()
    user_pwd = request.vars['user_pwd'].decode()
    user_first_name = request.vars['user_first_name'].decode()
    user_last_name = request.vars['user_last_name'].decode()

    try:
        user = auth.get_user_by_email(user_email)
    except:
        #email is not used
        if len(user_pwd) < 6:
            ##there should be front end checking
            ##user password is not long enough, firebase request 6 at least
            pass
        else:
            #create account
            user = auth.create_user(
                email=user_email,
                email_verified=False,
                password=user_pwd,
                disabled=False)
            user_uid = user.uid.decode()

            ## assign a cookie to browser here!!!!!

            #put data to firestore
            user_data = {
                u'first_name': user_first_name,
                u'last_name': user_last_name,
                u'email': user_email
            }
            db.collection(u'users').document(user_uid).set(user_data)
            #user is created
    else:
        #email already used!!
        pass
'''
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import json
import os

userUidArr=[u'47M3QdWhfkMbrSDvuTglpwz30Gn1',
            u'8TyZ3sGCYYPA2p11wIGUPnxPW5A3',
            u'Ipus0TpfCzXVABANUoE32Qb3V7A2',
            u'N1OaUlBKfXaXhX24VbleWNwKmnc2',
            u'NElrjI2dYqNxTBTO2mVsteDgWDd2',
            u'dJAdQJFv6Lgk8fYRF8n3eTzLIDm1'
    ]



'''
def profile():

    db = firestore.client()

    newArr = []

    doc_ref = db.collection(u'users').document(u'dJAdQJFv6Lgk8fYRF8n3eTzLIDm1')
    doc = doc_ref.get()

    if doc :
        return doc.to_dict()
    else:
        return "cannot find"

    for uid in userUidArr:
        doc_ref = db.collection(u'users').document(uid)
        try:
            doc = doc_ref.get()
            newArr.append({uid:doc.to_dict()['email']})
        except:
            newArr.append({uid:"cannot find"})
            pass
            #print(u'No such document!')
        #print "Get document: " + uid

    #print "Hello World"
    #print

    return json.dumps(newArr,indent=4)
'''
