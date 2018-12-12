import json
from six import string_types
from querystring_parser import parser

import firebase_admin
from firebase_admin import credentials, auth, firestore
#from google.cloud import firestore

path = 'tutorPlusKey.json'
if not len(firebase_admin._apps):
	cred = credentials.Certificate(path)
	default_app = firebase_admin.initialize_app(cred)
db = firebase_admin.firestore.client()

db_fire = firestore.client()
auth = auth
# -------------------------------------------------------------------------
# Constants
# -------------------------------------------------------------------------
USER_COLLECTION = u"users"
SCHOOL_COLLECTION = u"schools"
COURSE_COLLECTION = u"courses"
STUDENT_COLLECTION = u"students"
TUTOR_COLLECTION = u"tutors"
UNREAD_COLLECTION = u"unread"
CHAT_COLLECTION = u"chats"
CHANNEL_COLLECTION = u"channel"
RATING_COLLECTION = u"rating"

IMAGE_FOLDER = u"images/"
IMAGE_EXTENSION = u".png"
# User fields
ID_FIELD = u"id"
GENDER_FIELD = u"gender"
IMAGE_URL_FIELD = u"imageURL"
MAJOR_FIELD = u"major"
PS_FIELD = u"ps"
SCHEDULE_FIELD = u"schedule"
NAME_FIELD = u"name"
COURSE_FIELD = u"courses"
UNIVERSITY_FIELD = u"university"
TAG_FIELD = u"tag"
COUNT_FIELD = u"count"
RATING_SUM_FIELD = u'rating_sum'
RATING_COUNT_FIELD = u'rating_count'

# Tutor fields
RATING_FIELD = u"rating"
REPLY_FIELD = u"reply"

USER_PROFILE_FIELDS = (ID_FIELD, COUNT_FIELD, GENDER_FIELD, IMAGE_URL_FIELD, MAJOR_FIELD, NAME_FIELD, PS_FIELD,
                       SCHEDULE_FIELD, TAG_FIELD, UNIVERSITY_FIELD, RATING_SUM_FIELD, RATING_COUNT_FIELD)
USER_EDITABLE_PROFILE_FIELDS = (GENDER_FIELD, IMAGE_URL_FIELD, MAJOR_FIELD, NAME_FIELD, PS_FIELD, SCHEDULE_FIELD, TAG_FIELD, UNIVERSITY_FIELD)

# School fields
SCHOOL_MAJOR_LIST_FIELD = "major_list"

# Transmission fields
TOKEN_TRANS = "idToken"
PACKET_TRANS = "packet"
DATA_TRANS = "data"
COURSE_TRANS = "course_id"
SCHOOL_TRANS = "school_id"
ACTIVE_TRANS = "is_active"
TUTOR_ID_TRANS = "tutor_id"

# Search tutors fields
GRADE_TUTOR = "grade"
RATING_TUTOR = "rating"

# -------------------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------------------
def test():
	print ("hwello world!!!")


def debug(funcName, content):
    print(bracket(funcName) + content)


def bracket(funcName):
    return str(funcName) + "():"

# -------------------------------------------------------------------------
# Private methods field
# -------------------------------------------------------------------------
# -------Helper functions------------


def __verify_idToken(id_token):
    if id_token is None:
        return False
    try:
        decoded_token = auth.verify_id_token(id_token)  # type:
        return decoded_token
    except Exception as e:
        debug("__verify_idToken", str(e))
        return None

def __parsePacket(packet, check_data=True, return_uid=False):
    if packet is None:
        debug("__parsePacket", "Packet is empty")
        return None
    else:
        packet = parser.parse(packet)
        if TOKEN_TRANS not in packet:
            debug("__parsePacket", "Packet doesn't contain idToken")
            return None
        else:
            cred = __verify_idToken(packet[TOKEN_TRANS])
            if cred is None:
                debug("__parsePacket", "IdToken is not valid")
                return None
            elif check_data:
                if DATA_TRANS not in packet:
                    debug("__parsePacket", "Data is empty")
                    return None
                else:
                    data = packet[DATA_TRANS]
                    if return_uid: data[TOKEN_TRANS] = cred
                    return data
            else:
                return dict()
'''
def __parsePacket(packet, check_data=True):
    if packet is None:
        debug("__parsePacket", "Packet is empty")
        return None
    else:
        packet = parser.parse(packet)
        if TOKEN_TRANS not in packet:
            debug("__parsePacket", "Packet doesn't contain idToken")
            return None
        else:
            cred = __verify_idToken(packet[TOKEN_TRANS])
            if cred is None:
                debug("__parsePacket", "IdToken is not valid")
                return None
            elif check_data:
                if DATA_TRANS not in packet:
                    debug("__parsePacket", "Data is empty")
                    return None
                else:
                    data = packet[DATA_TRANS]
                    return data
            else:
                return dict()
'''

def __checkStrList(lst):
    if lst and isinstance(lst, list):
        return all(isinstance(elem, string_types) for elem in lst)
    else:
        return False


def __parseCollection(collections):
    if __checkStrList(collections):
        if len(collections) < 0 and len(collections) % 2 == 0:
            raise ValueError('__parseCollection(): collections count not correct')
        else:
            collect_ref = db_fire.collection(collections[0])
            for i in range(1, len(collections), 2):
                collect_ref = collect_ref.document(collections[i]).collection(collections[i + 1])
            return collect_ref
    else:
        raise ValueError('__parseCollection(): collections type not correct')


# -------Single Document------------
def __downloadDoc(collections, uid):
    if __checkStrList(collections) and isinstance(uid, str):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            doc = doc_ref.get()
            doc_dict = doc.to_dict()  # type: object
            debug("__downloadDoc", uid + ": {}".format(doc_dict))
            return doc_dict
        except Exception as e:
            raise ValueError(bracket(__downloadDoc) + str(e))

    else:
        raise ValueError(bracket(__downloadDoc) + 'collections or uid type not correct')


def __updateDoc(collections, uid, dic):
    if __checkStrList(collections) and isinstance(uid, str) and isinstance(dic, dict):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            doc_ref.update(dic)
            debug("__updateDoc", uid + ": {}".format(dic))

        except Exception as e:
            raise ValueError(bracket(__updateDoc) + str(e))

    else:
        raise ValueError(bracket(__updateDoc) + 'collections or uid or dic type not correct')


def __createDoc(collections, uid, dic):
    if __checkStrList(collections) and isinstance(uid, str) and isinstance(dic, dict):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            doc_ref.set(dic)
            debug("__createDoc", uid + ": {}".format(dic))

        except Exception as e:
            raise ValueError(bracket(__createDoc) + str(e))
    else:
        raise ValueError(bracket(__createDoc) + 'collections or uid or dic type not correct')


def __deleteDoc(collections, uid):
    if __checkStrList(collections) and isinstance(uid, str):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            doc_ref.delete()
            debug("__deleteDoc", uid + " was successfully deleted.")

        except Exception as e:
            raise ValueError(bracket("__deleteDoc") + str(e))
    else:
        raise ValueError(bracket("__deleteDoc") + 'collections or uid type not correct')

# -------Collection------------
def __downloadAllFromCollection(collections):
    if __checkStrList(collections):
        try:
            collec_ref = __parseCollection(collections)
            docs = collec_ref.get()
            docs_back = []
            for doc in docs:
                data = doc.to_dict()
                data[ID_FIELD] = doc.id
                docs_back.append(data)
            return docs_back
        except Exception as e:
            raise ValueError(bracket("__downloadAllFromCollection") + str(e))
    else:
        raise ValueError(bracket("__downloadAllFromCollection") + 'collections type not correct')
        
        
        
def __ifDocExist(collections, uid):
    if __checkStrList(collections) and isinstance(uid, str):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            return doc_ref.get().exists

        except Exception as e:
            raise ValueError(bracket("__ifDocExist") + str(e))
    else:
        raise ValueError(bracket("__ifDocExist") + 'collections or uid type not correct') 
        

        
