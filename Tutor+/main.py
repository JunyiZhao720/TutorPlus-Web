# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# [START gae_python37_app]
from flask import Flask, request
from flask_cors import CORS
from flask import jsonify
from flask import render_template

import os
import json

import helperFunc as apiPri
from helperFunc import *
from querystring_parser import parser


# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__, static_url_path='')
CORS(app)


class InvalidUsage(Exception):
    status_code = 400
    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

def __parsePacket(packet, check_data=True):
    if packet is None:
        debug("__parsePacket", "Packet is empty")
        return None
    else:
        #packet = simplejson.loads(packet)
        packet = parser.parse(packet)
        print (packet)
        return packet
        if TOKEN_TRANS not in packet:
            debug("__parsePacket", "Packet doesn't contain idToken")
            return None
        else:
            cred = apiPri.__verify_idToken(packet[TOKEN_TRANS])
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

@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    fh = open("index.html", "r")
    return fh.read()
    #return 'Hello Cross Origin Flask World!'
    

@app.route('/check')
def profile():
	userUidArr=[u'47M3QdWhfkMbrSDvuTglpwz30Gn1',
           u'8TyZ3sGCYYPA2p11wIGUPnxPW5A3',
           u'Ipus0TpfCzXVABANUoE32Qb3V7A2',
           u'N1OaUlBKfXaXhX24VbleWNwKmnc2',
           u'NElrjI2dYqNxTBTO2mVsteDgWDd2',
          u'dJAdQJFv6Lgk8fYRF8n3eTzLIDm1']
	
	newArr = []
	
	for uid in userUidArr:
		doc_ref = db.collection(u'users').document(uid)
		try:
			doc = doc_ref.get()
			newArr.append({uid:doc.to_dict()['email']})
		except:
			newArr.append({uid:"cannot find"})
			pass
	return jsonify(dict(data=newArr))

'''
@app.route('/get-profile')
def get_profile():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    #packet = request.args
    #if (apiPri.__verify_idToken(packet[TOKEN_TRANS]) is None):
    #	raise InvalidUsage('Invalid Token', status_code=400)
    #data=packet[DATA_TRANS]
    if data is None:
        debug("get_profile", "Packet errors")
        raise InvalidUsage('Packet errors', status_code=400)
    # main fields
    if ID_FIELD not in data:
        debug("get_profile", "Empty id")
        raise InvalidUsage("Empty id", status_code=400)
    uid = str(data[ID_FIELD])
    collections = [USER_COLLECTION]
    try:
        profile = apiPri.__downloadDoc(collections, uid)
        return jsonify(dict(profile=profile))
    except Exception as e:
        debug("get_profile", str(e))
        raise InvalidUsage(uid + ": Document doesn't exist", status_code=400)
'''
   
@app.route('/get-profile')
def get_profile():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string, True, True)
    if data is None:
        debug("get_profile", "Packet errors")
        raise InvalidUsage('Packet errors', status_code=400)
    # main fields
    if ID_FIELD not in data:
        debug("get_profile", "Empty id")
        raise InvalidUsage("Empty id", status_code=400)
    uid = data[ID_FIELD]
    uid = str(uid)
    cred = data[TOKEN_TRANS]
    cred = str(cred[u"uid"])
    
    requestSelfProfile = True if cred == uid else False
    
    user = auth.get_user(uid)
    user_email = user.email
    
    # get data
    collections = [USER_COLLECTION]
    try:
        profile = {}
        if apiPri.__ifDocExist(collections, uid):
            profile = apiPri.__downloadDoc(collections, uid)
            profileFix = False
            for Field in USER_PROFILE_FIELDS:
            	if Field not in profile:
            		profileFix= True
            		if Field == ID_FIELD:
            			profile.update({Field: uid})
            		elif Field == COUNT_FIELD:
            			profile.update({Field: 0})
            		elif Field == GENDER_FIELD:
            			profile.update({Field: u""})
            		elif Field == IMAGE_URL_FIELD:
            			profile.update({Field: "https://cdn.vuetifyjs.com/images/cards/halcyon.png"})
            		elif Field == MAJOR_FIELD:
            			profile.update({Field: u""})
            		elif Field == NAME_FIELD:
            			profile.update({Field: u""})
            		elif Field == PS_FIELD:
            			profile.update({Field: u""})
            		elif Field == SCHEDULE_FIELD:
            			profile.update({Field: u""})
            		elif Field == TAG_FIELD:
            			profile.update({Field: []})
            		elif Field == UNIVERSITY_FIELD:
            			profile.update({Field: u""})
            		elif Field == RATING_SUM_FIELD:
            			profile.update({Field: 0})
            		elif Field == RATING_COUNT_FIELD:
            			profile.update({Field: 0})
            	try:
            	    profile[Field] = profile[Field].decode()
            	except AttributeError:
            	    pass
            	else:
            		profileFix = True
            if (profileFix):
            	collections = [USER_COLLECTION]
            	apiPri.__updateDoc(collections, uid, profile)
        elif requestSelfProfile:
            profile = {
                COUNT_FIELD: 0,
                RATING_SUM_FIELD: 0,
                RATING_COUNT_FIELD: 0,
                GENDER_FIELD: u"",
                ID_FIELD: str(uid),
                IMAGE_URL_FIELD: "https://cdn.vuetifyjs.com/images/cards/halcyon.png",
                MAJOR_FIELD: u"",
                NAME_FIELD: u"",
                PS_FIELD: u"",
                SCHEDULE_FIELD: u"",
                TAG_FIELD: [],
                UNIVERSITY_FIELD: u""
            }
            apiPri.__createDoc(collections, uid, profile)
        profile.update({"email":user_email})
        return jsonify({"profile": profile})
    except ValueError as e:
        debug("get_profile", str(e))
        raise InvalidUsage(uid + ": Document doesn't exist", status_code=400)
        
@app.route('/update-profile')
def update_profile():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    if data is None:
        debug("update_profile", "Packet errors")
        raise InvalidUsage('Packet errors', status_code=400)
    # main fields
    decoded_token = auth.verify_id_token(request.args["idToken"])
    uid = decoded_token['uid']
    collections = [USER_COLLECTION]
    '''
    if ID_FIELD not in data:
        debug("update_profile", "Empty id")
        raise InvalidUsage("Empty id", status_code=400)
    uid = data[ID_FIELD]
    uid = str(uid)
    '''
    newProfile = apiPri.__downloadDoc(collections, uid)
    for field_name in data:
        if field_name not in USER_EDITABLE_PROFILE_FIELDS:
            debug("update_profile", uid + ": " + field_name + " is not a user field")
            raise InvalidUsage(uid + ": " + field_name + " is not a user field", 400)
        else:
        	newProfile.update({field_name: data[field_name]})
    newProfile.update({u"id": uid})
    try:
        apiPri.__updateDoc(collections, uid, newProfile)
    except ValueError as e:
        debug(update_profile, str(e))
        raise InvalidUsage(uid + ': Updating info encounters an error', 400)
    return jsonify({"status": "success"})


@app.route('/create-profile')
def create_profile():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    if data is None:
        debug("create_profile", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # main fields
    if ID_FIELD not in data:
        debug("create_profile", "Empty id")
        raise InvalidUsage("Empty id", 400)
    uid = data[ID_FIELD]
    uid = str(uid)
    for field_name in data:
        if field_name not in USER_PROFILE_FIELDS:
            debug("create_profile", uid + ": <" + field_name + "> is not a user field")
            raise InvalidUsage(uid + ": " + field_name + " is not a user field", 400)
    collections = [USER_COLLECTION]
    try:
        apiPri.__createDoc(collections, uid, data)
    except ValueError as e:
        debug("create_profile", str(e))
        raise InvalidUsage(uid + ': Creating info encounters an error', 400)
    return jsonify({"status": "success"})


@app.route('/download-course-list-for-the-user')
def download_course_list_for_the_user():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    #data = request.args
    if data is None:
        debug("download_course_list_for_the_user", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # main fields
    if ID_FIELD not in data:
        debug("download_course_list_for_the_user", "Empty id")
        raise InvalidUsage("Empty id", 400)
    uid = data[ID_FIELD]
    uid = str(uid)
    collections = [USER_COLLECTION, uid, COURSE_COLLECTION]
    try:
        courses = apiPri.__downloadAllFromCollection(collections)
        course_list_user = []
        for course in courses:
            course_list_user.append(course)
        return jsonify(dict(course_list_user=course_list_user))
    except ValueError as e:
        debug("download_course_list_for_the_user", str(e))
        raise InvalidUsage("Internal error", 400)
    return jsonify({"status": "success"})


@app.route('/upload-course-list-for-the-user')
def upload_course_list_for_the_user():
    # check if packet valid
    packet = json.loads(request.args["packet"])
    cred = apiPri.__verify_idToken(packet[TOKEN_TRANS])
    if cred is None:
        raise InvalidUsage("IdToken is not valid", 400)
    
    #data = apiPri.__parsePacket(packet)
    #data =  parser.parse(request.query_string)
    data = packet["data"]
    if data is None:
        debug("upload_course_list_for_the_user", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # check id
    if ID_FIELD not in data:
        debug("upload_course_list_for_the_user", "Empty id")
        raise InvalidUsage("Empty id", 400)
    uid = data[ID_FIELD]
    uid = str(uid)

    # check course field
    if COURSE_FIELD not in data:
        debug("upload_course_list_for_the_user", "Empty course list")
        raise InvalidUsage("Empty course list", 400)
    course_list = data[COURSE_FIELD]

    # delete all previous data
    collections_user = [USER_COLLECTION, uid, COURSE_COLLECTION]
    try:
        courses = apiPri.__downloadAllFromCollection(collections_user)
        for course in courses:
            school = str(course["school"])
            courseName = str(course["course"])
            Name = school + "-" + courseName
            # delete from school
            collections_school = [SCHOOL_COLLECTION, school, COURSE_COLLECTION, courseName, TUTOR_COLLECTION]
            apiPri.__deleteDoc(collections_school, uid)
            # delete from our field
            apiPri.__deleteDoc(collections_user, Name)
    except Exception as e:
        debug("upload_course_list_for_the_user: delete previous data: ", str(e))
        raise InvalidUsage("Internal error", 400)

    # check is active
    update_list = []
    for course in course_list:
        if (course):
            if (ACTIVE_TRANS not in course) or (DATA_TRANS not in course):
                debug("upload_course_list_for_the_user",
                      "Course doesn't contain a is_active field or data field for " + str(course))
                raise InvalidUsage("Course doesn't contain a is_active field or data field for  " + str(course), 400)
            else:
                 #append different state list to different lists
                 state = bool(course[ACTIVE_TRANS])
                 if state:
                     update_list.append(course[DATA_TRANS])

    # db insert
    try:
        # update list
        for course in update_list:
            if course["grade"] and course["school"] and course["course"]:
                school = str(course[u"school"])
                courseName = str(course[u"course"])
                name = str(school + u"-" + courseName)
                # to our own collection
                apiPri.__createDoc(collections_user, name, course)
                # to school collection
                collections_school = [SCHOOL_COLLECTION, school, COURSE_COLLECTION, courseName, TUTOR_COLLECTION]
                apiPri.__createDoc(collections_school, uid, {ID_FIELD: str(uid)})
    except ValueError as e:
        debug("upload_course_list_for_the_user", str(e))
        raise InvalidUsage("Internal error", 400)
    return jsonify({"status": "success"})
        


# -------------------------------------------------------------------------
# School & Course & Major
# -------------------------------------------------------------------------
@app.route('/download-school-fields')
def download_school_fields():
    data = request.args
    #data = apiPri.__parsePacket(request.query_string)
    if data is None:
        debug("download_school_fields", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # parse data
    if SCHOOL_TRANS not in data:
        debug("download_school_fields", "Empty school_id")
        raise InvalidUsage("Empty school_id", 400)
    school = data[SCHOOL_TRANS]
    school = str(school)
    # main field
    collections = [SCHOOL_COLLECTION]
    try:
        # download school fields
        school = apiPri.__downloadDoc(collections, school)
        return jsonify(dict(school=school))
    except ValueError as e:
        debug("download_school_fields", str(e))
        raise InvalidUsage("Internal error", 400)


# -------------------------------------------------------------------------
# tutor
# -------------------------------------------------------------------------
@app.route('/download-tutor-profile-list')
def download_tutor_profile_list():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    #data = request.args
    if data is None:
        debug("download_tutor_profile_list", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # parse data
    if SCHOOL_TRANS not in data:
        debug("download_tutor_profile_list", "Empty school_id")
        raise InvalidUsage("Empty school_id", 400)
    school = data[SCHOOL_TRANS]
    school = str(school)
    if COURSE_TRANS not in data:
        debug("download_tutor_profile_list", "Empty course_id")
        raise InvalidUsage("Empty course_id", 400)
    course = data[COURSE_TRANS]
    course = str(course)

    collections = [SCHOOL_COLLECTION, school, COURSE_COLLECTION, course, TUTOR_COLLECTION]
    try:
        # download tutor ids
        tutors = apiPri.__downloadAllFromCollection(collections)
        tutor_list = []
        profile_list = []
        for tutor in tutors:
            tutor_list.append(str(tutor[ID_FIELD]))
        # download tutor profiles
        collections = [USER_COLLECTION]
        for tutor in tutor_list:
            profile = apiPri.__downloadDoc(collections, tutor)
            courseName = school + "-" + course
            courseInfo = apiPri.__downloadDoc([USER_COLLECTION, tutor, COURSE_COLLECTION], courseName)

            name = profile[NAME_FIELD] if NAME_FIELD in profile and profile[NAME_FIELD] else ""
            university = profile[UNIVERSITY_FIELD] if UNIVERSITY_FIELD in profile and profile[UNIVERSITY_FIELD] else ""
            rating = float(profile[RATING_SUM_FIELD]) / float(
                profile[RATING_COUNT_FIELD]) if RATING_SUM_FIELD in profile and RATING_COUNT_FIELD in profile and float(profile[RATING_SUM_FIELD]) !=0 else "N/A"
            major = profile[MAJOR_FIELD] if MAJOR_FIELD in profile and profile[MAJOR_FIELD] else ""
            grade = courseInfo[GRADE_TUTOR] if courseInfo is not None and GRADE_TUTOR in courseInfo and courseInfo[GRADE_TUTOR] else ""
            imageURL = profile[IMAGE_URL_FIELD] if IMAGE_URL_FIELD in profile and profile[IMAGE_URL_FIELD] else "https://cdn.vuetifyjs.com/images/cards/halcyon.png"
            profile_list.append({
                "id": tutor,
                "name": name,
                "university": university,
                "major": major,
                "rating": rating,
                "grade": grade,
                "imageURL": imageURL
            })
        return jsonify({"profile_list": profile_list})
    except ValueError as e:
        debug("download_tutor_profile_list", str(e))
        raise InvalidUsage("Internal error", 400)
        
@app.route('/download-tutor-profile-list-by-name')
def download_tutor_profile_list_by_name():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    #data = request.args
    if data is None:
        debug("download_tutor_profile_list_by_name", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # parse data
    if NAME_FIELD not in data:
        debug("download_tutor_profile_list_by_name", "Empty name")
        raise InvalidUsage("Empty name", 400)
    name = str(data[NAME_FIELD])

    try:
        # download tutor ids
        collect = apiPri.__parseCollection([USER_COLLECTION])
        docs = collect.where(NAME_FIELD, u'==', name).get()
        profile_list = []
        for tutor in docs:
            tutor_id = tutor.id
            tutor = tutor.to_dict()
            name = tutor[NAME_FIELD]
            university = tutor[UNIVERSITY_FIELD] if UNIVERSITY_FIELD in tutor and tutor[UNIVERSITY_FIELD] else ""
            rating = float(tutor[RATING_SUM_FIELD]) / float(
                tutor[RATING_COUNT_FIELD]) if RATING_SUM_FIELD in tutor and RATING_COUNT_FIELD in tutor and float(tutor[RATING_SUM_FIELD])!=0 else "N/A"
            major = tutor[MAJOR_FIELD] if MAJOR_FIELD in tutor and tutor[MAJOR_FIELD] else ""
            grade = ""
            imageURL = tutor[IMAGE_URL_FIELD] if IMAGE_URL_FIELD in tutor and tutor[IMAGE_URL_FIELD] else "https://cdn.vuetifyjs.com/images/cards/halcyon.png"
            profile_list.append({
                ID_FIELD: tutor_id,
                NAME_FIELD: name,
                UNIVERSITY_FIELD: university,
                MAJOR_FIELD: major,
                RATING_FIELD: rating,
                GRADE_TUTOR: grade,
                IMAGE_URL_FIELD: imageURL
            })
        return jsonify({"profile_list": profile_list})
    except ValueError as e:
        debug("download_tutor_profile_list", str(e))
        raise InvalidUsage("Internal error", 400)

@app.route('/download-tutor-replies')
def download_tutor_replies():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    if data is None:
        debug("download_tutor_replies", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # main fields
    if ID_FIELD not in data:
        debug("download_tutor_replies", "Empty id")
        raise InvalidUsage("Empty id", 400)
    uid = data[ID_FIELD]
    uid = str(uid)
    collections = [USER_COLLECTION, uid, RATING_COLLECTION]
    try:
        replies = apiPri.__downloadAllFromCollection(collections)
        tutor_reply_list = []
        for reply in replies:
            tutor_reply_list.append(reply)
        return jsonify(dict(tutor_reply_list=tutor_reply_list))
    except ValueError as e:
        debug("download_tutor_replies", str(e))
        raise InvalidUsage("Internal error", 400)

@app.route('/upload-user-rating')
def upload_user_rating():
    # check if packet valid
    data = apiPri.__parsePacket(request.query_string)
    if data is None:
        debug("upload_user_rating", "Packet errors")
        raise InvalidUsage("Packet errors", 400)
    # main fields
    if ID_FIELD not in data or TUTOR_ID_TRANS not in data:
        debug("upload_user_rating", "Empty id or tutor_id")
        raise InvalidUsage("Empty id or tutor_id", 400)
    uid = data[ID_FIELD]
    uid = str(uid)
    tutor_id = data[TUTOR_ID_TRANS]
    tutor_id = str(tutor_id)

    # check if exists
    collections_tutor = [USER_COLLECTION, tutor_id, RATING_COLLECTION]
    exist_state = apiPri.__ifDocExist(collections_tutor, uid)

    # db storage
    try:
        new_reply = {
            ID_FIELD: str(uid),
            REPLY_FIELD: str(data[REPLY_FIELD]),
            RATING_FIELD: str(data[RATING_FIELD])
        }
        tutor_profile = apiPri.__downloadDoc([USER_COLLECTION], tutor_id)

        # got previous tutor profile
        if RATING_COUNT_FIELD in tutor_profile and RATING_SUM_FIELD in tutor_profile:
            tutor_sum = tutor_profile[RATING_SUM_FIELD]
            tutor_count = tutor_profile[RATING_COUNT_FIELD]
        else:
            tutor_sum = 0
            tutor_count = 0

        # check if the reply already exists
        if exist_state:
            old_reply = apiPri.__downloadDoc(collections_tutor, uid)
            old_rating = int(old_reply[RATING_FIELD])

            tutor_sum -= old_rating
            tutor_sum += int(data[RATING_FIELD])
        else:
            tutor_sum += int(data[RATING_FIELD])
            tutor_count += 1

        apiPri.__createDoc(collections_tutor, uid, new_reply)
        tutor_profile[RATING_COUNT_FIELD] = tutor_count
        tutor_profile[RATING_SUM_FIELD] = tutor_sum
        print(tutor_count)
        print()
        apiPri.__createDoc([USER_COLLECTION], tutor_id, tutor_profile)
    except ValueError as e:
        debug("upload_user_rating", str(e))
        raise InvalidUsage("Internal error", 400)
    return jsonify({"status": "success"})

        

@app.route('/echo', methods=['GET', 'POST'])
def echo():
	newDict = {"status":"success"}
	try:
		valuesData = request.values
		newDict.update({"valuesData": valuesData})
	except:
		pass
	try:
		fromData = request.form
		newDict.update({"fromData": fromData})
	except:
		pass
	try:
		argsData = request.args
		newDict.update({"argsData": argsData})
	except:
		pass
	try:
		jsonData = request.get_json()
		newDict.update({"jsonData": jsonData})
	except:
		pass
	return json.dumps(newDict)

@app.route('/echojson')
def echojson():
	packet = parser.parse(request.query_string)
	return jsonify(packet)

@app.route('/400')
def error():
	raise InvalidUsage('Packet errors', status_code=400)
	#return json.dumps({ "data": "null" }), 400
	
	


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]
