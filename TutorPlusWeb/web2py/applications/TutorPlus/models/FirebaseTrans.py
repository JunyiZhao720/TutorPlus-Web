import csv
import os.path
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials

# my_path = os.path.abspath(os.path.dirname(__file__))
# path = os.path.join(my_path, "../private/tutorplus-93a0f-firebase-adminsdk-tvsuo-2a85fea19f.json")
# if (not len(firebase_admin._apps)):
#     cred = credentials.Certificate(path)
#     default_app = firebase_admin.initialize_app(cred)
#     print(default_app.name)
#     print("Initialized!")
#
# else:
#     print("Already initialized")
# cred = credentials.Certificate(path)
# default_app = firebase_admin.initialize_app(cred,None,"TutorPlus")