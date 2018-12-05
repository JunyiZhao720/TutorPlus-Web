# -------------------------------------------------------------------------
# Auth methods field
# -------------------------------------------------------------------------

import json


def check_userId():
    # id_token = request.vars.idToken
    # print(request.vars)
    # data = str(request.vars.data)
    # data = data.replace("'", "\"")
    # data = json.loads(data)
    data = simplejson.loads(request.vars.data)
    print(data["idToken"])

    # data = simplejson.loads(request.vars.data)
    # print(request.vars.data)
    # # data = str (request.vars.data)
    # # data = simplejson.loads(data)
    # print(data)
    # id_token = str(id_token)
    # print(id_token)
    # try:
    #     decoded_token = auth.verify_id_token(id_token)  # type:
    #     print(decoded_token)
    # except Exception, e:
    #     debug("check_userId", str(e))

    return "userId checked"


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
    except Exception, e:
        debug("__verify_idToken", str(e))
        return None


def __parsePacket(packet, check_data=True):
    if packet is None:
        debug("__parsePacket", "Packet is empty")
        return None
    else:
        packet = simplejson.loads(packet)
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


def __checkStrList(lst):
    if lst and isinstance(lst, list):
        return all(isinstance(elem, basestring) for elem in lst)
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
        except Exception, e:
            raise ValueError(bracket(__downloadDoc) + str(e))

    else:
        raise ValueError(bracket(__downloadDoc) + 'collections or uid type not correct')


def __updateDoc(collections, uid, dic):
    if __checkStrList(collections) and isinstance(uid, str) and isinstance(dic, dict):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            doc_ref.update(dic)
            debug("__updateDoc", uid + ": {}".format(dic))

        except Exception, e:
            raise ValueError(bracket(__updateDoc) + str(e))

    else:
        raise ValueError(bracket(__updateDoc) + 'collections or uid or dic type not correct')


def __createDoc(collections, uid, dic):
    if __checkStrList(collections) and isinstance(uid, str) and isinstance(dic, dict):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            doc_ref.set(dic)
            debug("__createDoc", uid + ": {}".format(dic))

        except Exception, e:
            raise ValueError(bracket(__createDoc) + str(e))
    else:
        raise ValueError(bracket(__createDoc) + 'collections or uid or dic type not correct')


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
        except Exception, e:
            raise ValueError(bracket("__downloadAllFromCollection") + str(e))
    else:
        raise ValueError(bracket("__downloadAllFromCollection") + 'collections type not correct')


# -------------------------------------------------------------------------
# Profile and User
# -------------------------------------------------------------------------
from gluon.contrib import simplejson


def get_profile():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("get_profile", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    if ID_FIELD not in data:
        debug("get_profile", "Empty id")
        raise HTTP(400, "Empty id")
    uid = data[ID_FIELD]
    uid = str(uid)
    collections = [USER_COLLECTION]
    try:
        profile = __downloadDoc(collections, uid)
        return response.json(dict(profile=profile))
    except ValueError, e:
        debug("get_profile", str(e))
        raise HTTP(400, uid + ": Document doesn't exist")


def update_profile():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("update_profile", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    if ID_FIELD not in data:
        debug("update_profile", "Empty id")
        raise HTTP(400, "Empty id")
    uid = data[ID_FIELD]
    uid = str(uid)
    for field_name in data:
        if field_name not in USER_PROFILE_FIELDS:
            debug("update_profile", uid + ": " + field_name + " is not a user field")
            raise HTTP(400, uid + ": " + field_name + " is not a user field")
    collections = [USER_COLLECTION]
    try:
        __updateDoc(collections, uid, data)
    except ValueError, e:
        debug(update_profile, str(e))
        raise HTTP(400, uid + ': Updating info encounters an error')


def create_profile():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("create_profile", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    if ID_FIELD not in data:
        debug("create_profile", "Empty id")
        raise HTTP(400, "Empty id")
    uid = data[ID_FIELD]
    uid = str(uid)
    for field_name in data:
        if field_name not in USER_PROFILE_FIELDS:
            debug("create_profile", uid + ": <" + field_name + "> is not a user field")
            raise HTTP(400, uid + ": " + field_name + " is not a user field")
    collections = [USER_COLLECTION]
    try:
        __createDoc(collections, uid, data)
    except ValueError, e:
        debug("create_profile", str(e))
        raise HTTP(400, uid + ': Creating info encounters an error')


def download_course_list_for_the_user():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("download_course_list_for_the_user", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    if ID_FIELD not in data:
        debug("download_course_list_for_the_user", "Empty id")
        raise HTTP(400, "Empty id")
    uid = data[ID_FIELD]
    uid = str(uid)
    collections = [USER_COLLECTION, uid, COURSE_COLLECTION]
    try:
        courses = __downloadAllFromCollection(collections)
        course_list_user = []
        for course in courses:
            course_list_user.append(course)
        return response.json(dict(course_list_user=course_list_user))
    except ValueError, e:
        debug("download_course_list_for_the_user", str(e))
        raise HTTP(400, "Internal error")


def upload_course_list_for_the_user():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("upload_course_list_for_the_user", "Packet errors")
        raise HTTP(400, "Packet errors")
    # check id
    if ID_FIELD not in data:
        debug("upload_course_list_for_the_user", "Empty id")
        raise HTTP(400, "Empty id")
    uid = data[ID_FIELD]
    uid = str(uid)

    # check course field
    if COURSE_FIELD not in data:
        debug("upload_course_list_for_the_user", "Empty course list")
        raise HTTP(400, "Empty course list")
    course_list = data[COURSE_FIELD]

    # server changes data
    update_list = []
    delete_list = []
    for course in course_list:
        if ACTIVE_TRANS not in course or DATA_TRANS not in course:
            debug("upload_course_list_for_the_user", "Course doesn't a is_active field or data field for " + course)
            raise HTTP(400, "Course doesn't a is_active field or data field for  " + course)
        else:
            state = bool(course[ACTIVE_TRANS])
            update_list.append(course[DATA_TRANS]) if state else delete_list.append(course[DATA_TRANS])

    # db change fields
    collections_user = [USER_COLLECTION]
    collections_school = [SCHOOL_COLLECTION]
    try:
        # update list
        # delete list
    except ValueError, e:
        debug("download_course_list_for_the_user", str(e))
        raise HTTP(400, "Internal error")


# -------------------------------------------------------------------------
# School & Course & Major
# -------------------------------------------------------------------------
def download_school_list():
    data = __parsePacket(request.vars.packet, False)
    if data is None:
        debug("download_school_list", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    collections = [SCHOOL_COLLECTION]
    try:
        schools = __downloadAllFromCollection(collections)
        school_list = []
        for school in schools:
            school_list.append(school[ID_FIELD])
        return response.json(dict(school_list=school_list))
    except Exception, e:
        debug("download_school_list", str(e))
        raise HTTP(400, "Internal error")


def download_school_fields():
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("download_school_fields", "Packet errors")
        raise HTTP(400, "Packet errors")
    # parse data
    if SCHOOL_TRANS not in data:
        debug("download_school_fields", "Empty school_id")
        raise HTTP(400, "Empty school_id")
    school = data[SCHOOL_TRANS]
    school = str(school)
    # main field
    collections = [SCHOOL_COLLECTION]
    try:
        # download school fields
        school = __downloadDoc(collections, school)
        return response.json(dict(school=school))
    except ValueError, e:
        debug("download_school_fields", str(e))
        raise HTTP(400, "Internal error")


# -------------------------------------------------------------------------
# tutor
# -------------------------------------------------------------------------

def download_tutor_profile_list():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("download_tutor_profile_list", "Packet errors")
        raise HTTP(400, "Packet errors")
    # parse data
    if SCHOOL_TRANS not in data:
        debug("download_tutor_profile_list", "Empty school_id")
        raise HTTP(400, "Empty school_id")
    school = data[SCHOOL_TRANS]
    school = str(school)
    if COURSE_TRANS not in data:
        debug("download_tutor_profile_list", "Empty course_id")
        raise HTTP(400, "Empty course_id")
    course = data[COURSE_TRANS]
    course = str(course)

    collections = [SCHOOL_COLLECTION, school, COURSE_COLLECTION, course, TUTOR_COLLECTION]
    try:
        # download tutor ids
        tutors = __downloadAllFromCollection(collections)
        tutor_list = []
        profile_list = []
        for tutor in tutors:
            tutor_list.append(str(tutor[ID_FIELD]))
        # download tutor profiles
        collections = [USER_COLLECTION]
        for tutor in tutor_list:
            profile_list.append(__downloadDoc(collections, tutor))
        return response.json(dict(profile_list=profile_list))
    except ValueError, e:
        debug("download_tutor_profile_list", str(e))
        raise HTTP(400, "Internal error")
