# -------------------------------------------------------------------------
# Auth methods field
# -------------------------------------------------------------------------


def check_userId():
    id_token = request.vars.userId
    decoded_token = auth.verify_id_token(id_token)  # type: dict
    debug("check_userId", "decoded_token" + decoded_token)
    return "userId checked"


# -------------------------------------------------------------------------
# Private methods field
# -------------------------------------------------------------------------

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
            for i in range(1, len(collections)):
                collect_ref = collect_ref.document(collections[i]).collection(collections[i + 1])
            return collect_ref
    else:
        raise ValueError('__parseCollection(): collections type not correct')


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


# -------------------------------------------------------------------------
# Profile
# -------------------------------------------------------------------------
from gluon.contrib import simplejson


def get_profile():
    uid = request.vars.id
    if uid is None:
        debug("get_profile", "Empty uid")
        return "Empty uid"
    uid = str(uid)
    collections = [USER_COLLECTION]
    try:
        profile = __downloadDoc(collections, uid)
        return response.json(dict(profile=profile))
    except ValueError, e:
        debug("get_profile", str(e))
        return uid + ": Document doesn't exist"


def update_profile():
    data = request.vars.data
    if data is None:
        debug("create_profile", "Empty data")
        return "Empty data"
    data = simplejson.loads(data)
    uid = data["id"]
    if uid is None:
        debug("create_profile", "Empty id")
        return "Empty id"
    uid = str(uid)
    # test code
    # data = dict()
    # data["count2"] = 0
    # end test code
    for field_name in data:
        if field_name not in USER_PROFILE_FIELDS:
            debug("update_profile", uid + ": " + field_name + " is not a user field")
            return uid + ": " + field_name + " is not a user field"
    collections = [USER_COLLECTION]
    try:
        __updateDoc(collections, uid, data)
        return uid + ': Updating successfully'
    except ValueError, e:
        debug(update_profile, str(e))
        return uid + ': Updating info encounters an error'


def create_profile():
    data = request.vars.data
    if data is None:
        debug("create_profile", "Empty data")
        return "Empty data"
    data = simplejson.loads(data)
    uid = data["id"]
    if uid is None:
        debug("create_profile", "Empty id")
        return "Empty id"
    uid = str(uid)
    # test code
    # data = dict()
    # data["count2"] = 0
    # end test code
    for field_name in data:
        if field_name not in USER_PROFILE_FIELDS:
            debug("create_profile", uid + ": <" + field_name + "> is not a user field")
            return uid + ": " + field_name + " is not a user field"
    collections = [USER_COLLECTION]
    try:
        __createDoc(collections, uid, data)
        return uid + ': Creating a profile succeeds'
    except ValueError, e:
        debug("create_profile", str(e))
    return uid + ': Creating info encounters an error'
