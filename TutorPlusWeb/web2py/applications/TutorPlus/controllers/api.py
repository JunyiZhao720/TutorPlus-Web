# -------------------------------------------------------------------------
# Private methods field
# -------------------------------------------------------------------------
# -------Helper functions------------


def __verify_idToken(id_token):
    if id_token is None:
        return None
    try:
        decoded_token = auth.verify_id_token(id_token)  # type:
        return decoded_token
    except Exception, e:
        debug("__verify_idToken", str(e))
        return None


def __parsePacket(packet, check_data=True, return_uid=False):
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
                    if return_uid: data[TOKEN_TRANS] = cred
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
            raise ValueError(bracket("__createDoc") + str(e))
    else:
        raise ValueError(bracket("__createDoc") + 'collections or uid or dic type not correct')


def __deleteDoc(collections, uid):
    if __checkStrList(collections) and isinstance(uid, str):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            doc_ref.delete()
            debug("__deleteDoc", uid + " was successfully deleted.")

        except Exception, e:
            raise ValueError(bracket("__deleteDoc") + str(e))
    else:
        raise ValueError(bracket("__deleteDoc") + 'collections or uid type not correct')


def __ifDocExist(collections, uid):
    if __checkStrList(collections) and isinstance(uid, str):
        try:
            doc_ref = __parseCollection(collections).document(uid)
            return doc_ref.get().exists

        except Exception, e:
            raise ValueError(bracket("__ifDocExist") + str(e))
    else:
        raise ValueError(bracket("__ifDocExist") + 'collections or uid type not correct')


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
    data = __parsePacket(request.vars.packet, True, True)
    if data is None:
        debug("get_profile", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    if ID_FIELD not in data:
        debug("get_profile", "Empty id")
        raise HTTP(400, "Empty id")
    uid = data[ID_FIELD]
    uid = str(uid)
    cred = data[TOKEN_TRANS]
    cred = str(cred[u"uid"])
    if cred != uid:
        debug("get_profile", cred + " " + uid + " doesn't match")
        raise HTTP(400, "Id doesn't match!")

    # get data
    collections = [USER_COLLECTION]
    try:
        if __ifDocExist(collections, uid):
            profile = __downloadDoc(collections, uid)
        else:
            profile = {
                COUNT_FIELD: 0,
                GENDER_FIELD: "",
                ID_FIELD: str(uid).decode('unicode-escape'),
                IMAGE_URL_FIELD: "",
                MAJOR_FIELD: "",
                NAME_FIELD: "",
                PS_FIELD: "",
                SCHEDULE_FIELD: "",
                TAG_FIELD: [],
                UNIVERSITY_FIELD: ""
            }
            __createDoc(collections, uid, profile)
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


# def create_profile():
#     # check if packet valid
#     data = __parsePacket(request.vars.packet)
#     if data is None:
#         debug("create_profile", "Packet errors")
#         raise HTTP(400, "Packet errors: data is null")
#     # main fields
#     if ID_FIELD not in data:
#         debug("create_profile", "Empty id")
#         raise HTTP(400, "Empty id")
#     uid = data[ID_FIELD]
#     uid = str(uid)
#     try:
#             profile = {
#                 COUNT_FIELD: 0,
#                 GENDER_FIELD: "",
#                 ID_FIELD: str(uid).decode('unicode-escape'),
#                 IMAGE_URL_FIELD: "",
#                 MAJOR_FIELD: "",
#                 NAME_FIELD: "",
#                 PS_FIELD: "",
#                 SCHEDULE_FIELD: "",
#                 TAG_FIELD: [],
#                 UNIVERSITY_FIELD: ""
#             }
#             __createDoc([USER_COLLECTION], uid, profile)
#     except ValueError, e:
#         debug("create_profile", str(e))
#         raise HTTP(400, uid + ': Creating info encounters an error')


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

    # delete all previous data
    collections_user = [USER_COLLECTION, uid, COURSE_COLLECTION]
    try:
        courses = __downloadAllFromCollection(collections_user)
        for course in courses:
            school = str(course["school"])
            courseName = str(course["course"])
            Name = school + "-" + courseName
            # delete from school
            collections_school = [SCHOOL_COLLECTION, school, COURSE_COLLECTION, courseName, TUTOR_COLLECTION]
            __deleteDoc(collections_school, uid)
            # delete from our field
            __deleteDoc(collections_user, Name)
    except Exception, e:
        debug("upload_course_list_for_the_user: delete previous data: ", str(e))
        raise HTTP(400, "Internal error")

    # check is active
    update_list = []
    for course in course_list:
        if ACTIVE_TRANS not in course or DATA_TRANS not in course:
            debug("upload_course_list_for_the_user",
                  "Course doesn't contain a is_active field or data field for " + str(course))
            raise HTTP(400, "Course doesn't contain a is_active field or data field for  " + str(course))
        else:
            # append different state list to different lists
            state = bool(course[ACTIVE_TRANS])
            if state: update_list.append(course[DATA_TRANS])

    # db insert
    try:
        # update list
        for course in update_list:
            school = str(course[u"school"])
            courseName = str(course[u"course"])
            name = str(school + u"-" + courseName)
            # to our own collection
            __createDoc(collections_user, name, course)
            # to school collection
            collections_school = [SCHOOL_COLLECTION, school, COURSE_COLLECTION, courseName, TUTOR_COLLECTION]
            __createDoc(collections_school, uid, {ID_FIELD: str(uid).decode('unicode-escape')})
    except ValueError, e:
        debug("upload_course_list_for_the_user", str(e))
        raise HTTP(400, "Internal error")


# -------------------------------------------------------------------------
# School & Course & Major
# -------------------------------------------------------------------------

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
            profile = __downloadDoc(collections, tutor)
            courseName = school + "-" + course
            courseInfo = __downloadDoc([USER_COLLECTION, tutor, COURSE_COLLECTION], courseName)

            name = profile[NAME_FIELD] if NAME_FIELD in profile else ""
            university = profile[UNIVERSITY_FIELD] if UNIVERSITY_FIELD in profile else ""
            rating = float(profile[RATING_SUM_FIELD]) / float(
                profile[RATING_COUNT_FIELD]) if RATING_SUM_FIELD in profile and RATING_COUNT_FIELD in profile else 0
            major = profile[MAJOR_FIELD] if MAJOR_FIELD in profile else ""
            grade = courseInfo[GRADE_TUTOR] if courseInfo is not None and GRADE_TUTOR in courseInfo else "Null"
            imageURL = profile[IMAGE_URL_FIELD] if IMAGE_URL_FIELD in profile else ""
            profile_list.append({
                ID_FIELD: tutor,
                NAME_FIELD: name,
                UNIVERSITY_FIELD: university,
                MAJOR_FIELD: major,
                RATING_FIELD: rating,
                GRADE_TUTOR: grade,
                IMAGE_URL_FIELD: imageURL
            })
        return response.json(dict(profile_list=profile_list))
    except ValueError, e:
        debug("download_tutor_profile_list", str(e))
        raise HTTP(400, "Internal error")


def download_tutor_profile_list_by_name():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("download_tutor_profile_list_by_name", "Packet errors")
        raise HTTP(400, "Packet errors")
    # parse data
    if NAME_FIELD not in data:
        debug("download_tutor_profile_list_by_name", "Empty name")
        raise HTTP(400, "Empty school_id")
    name = str(data[NAME_FIELD]).decode('unicode-escape')

    try:
        # download tutor ids
        collect = __parseCollection([USER_COLLECTION])
        docs = collect.where(NAME_FIELD, u'==', name).get()
        profile_list = []
        for tutor in docs:
            tutor_id = tutor.id
            tutor = tutor.to_dict()
            name = tutor[NAME_FIELD]
            university = tutor[UNIVERSITY_FIELD] if UNIVERSITY_FIELD in tutor else ""
            rating = float(tutor[RATING_SUM_FIELD]) / float(
                tutor[RATING_COUNT_FIELD]) if RATING_SUM_FIELD in tutor and RATING_COUNT_FIELD in tutor else 0
            major = tutor[MAJOR_FIELD] if MAJOR_FIELD in tutor else ""
            grade = None
            imageURL = tutor[IMAGE_URL_FIELD] if IMAGE_URL_FIELD in tutor else ""
            profile_list.append({
                ID_FIELD: tutor_id,
                NAME_FIELD: name,
                UNIVERSITY_FIELD: university,
                MAJOR_FIELD: major,
                RATING_FIELD: rating,
                GRADE_TUTOR: grade,
                IMAGE_URL_FIELD: imageURL
            })
        return response.json(dict(profile_list=profile_list))
    except ValueError, e:
        debug("download_tutor_profile_list", str(e))
        raise HTTP(400, "Internal error")

def download_tutor_replies():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("download_tutor_replies", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    if ID_FIELD not in data:
        debug("download_tutor_replies", "Empty id")
        raise HTTP(400, "Empty id")
    uid = data[ID_FIELD]
    uid = str(uid)
    collections = [USER_COLLECTION, uid, RATING_COLLECTION]
    try:
        replies = __downloadAllFromCollection(collections)
        tutor_reply_list = []
        for reply in replies:
            tutor_reply_list.append(reply)
        return response.json(dict(tutor_reply_list=tutor_reply_list))
    except ValueError, e:
        debug("download_tutor_replies", str(e))
        raise HTTP(400, "Internal error")


def upload_user_rating():
    # check if packet valid
    data = __parsePacket(request.vars.packet)
    if data is None:
        debug("upload_user_rating", "Packet errors")
        raise HTTP(400, "Packet errors")
    # main fields
    if ID_FIELD not in data or TUTOR_ID_TRANS not in data:
        debug("upload_user_rating", "Empty id or tutor_id")
        raise HTTP(400, "Empty id or tutor_id")
    uid = data[ID_FIELD]
    uid = str(uid)
    tutor_id = data[TUTOR_ID_TRANS]
    tutor_id = str(tutor_id)

    # check if exists
    collections_tutor = [USER_COLLECTION, tutor_id, RATING_COLLECTION]
    exist_state = __ifDocExist(collections_tutor, uid)

    # db storage
    try:
        new_reply = {
            ID_FIELD: str(uid).decode('unicode-escape'),
            REPLY_FIELD: str(data[REPLY_FIELD]).decode('unicode-escape'),
            RATING_FIELD: str(data[RATING_FIELD]).decode('unicode-escape')
        }
        tutor_profile = __downloadDoc([USER_COLLECTION], tutor_id)

        # got previous tutor profile
        if RATING_COUNT_FIELD in tutor_profile and RATING_SUM_FIELD in tutor_profile:
            tutor_sum = tutor_profile[RATING_SUM_FIELD]
            tutor_count = tutor_profile[RATING_COUNT_FIELD]
        else:
            tutor_sum = 0
            tutor_count = 0

        # check if the reply already exists
        if exist_state:
            old_reply = __downloadDoc(collections_tutor, uid)
            old_rating = int(old_reply[RATING_FIELD])

            tutor_sum -= old_rating
            tutor_sum += int(data[RATING_FIELD])
        else:
            tutor_sum += int(data[RATING_FIELD])
            tutor_count += 1

        __createDoc(collections_tutor, uid, new_reply)
        tutor_profile[RATING_COUNT_FIELD] = tutor_count
        tutor_profile[RATING_SUM_FIELD] = tutor_sum
        print(tutor_count)
        print()
        __createDoc([USER_COLLECTION], tutor_id, tutor_profile)
    except ValueError, e:
        debug("upload_user_rating", str(e))
        raise HTTP(400, uid + ': Internal error')
