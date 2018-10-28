import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


def signup(user_email, user_pwd, user_first_name, user_last_name):
    # Use a service account
    firebaseKeyPath = 'tutorplus-93a0f-firebase-adminsdk-tvsuo-68abb4e9eb.json'
    cred = credentials.Certificate(firebaseKeyPath)
    firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    
    #user = auth.get_user("2jeh6GbkVVUtK531nsgL8YSOmNx2")
    #print('Successfully fetched user data: {0}'.format(user.uid))
    
    
    ## string need to be converted to unicode in either two methods below
    ## otherwise in the firebase it would be blob instead of string
    #user_last_name = unicode(user_last_name, "utf-8")
    #user_last_name = user_last_name.decode()
    
    user_email = user_email.decode()
    user_pwd = user_pwd.decode()
    user_first_name = user_first_name.decode()
    user_last_name = user_last_name.decode()
    
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
            
            #put data to firestore
            user_data = {
                u'first_name': user_first_name,
                u'last_name': user_last_name,
                u'email': user_email
            }
            db.collection(u'users').document(user_uid).set(user_data)
            #user is created
            
            ## assign a cookie to browser here!!!!!
            ## redirect to the main page here!!!!!
    else:
        #email already used!!
        #redirect to the signup page with a warning report
        pass
