from flask import Blueprint , jsonify ,request
from components import myMethods as me
from flask_cors import cross_origin
from DB_Connections.DB_EndPoints_Connections import UsersDB


# log_reg_blp = Blueprint("log_reg_blp",__name__,static_folder="static",template_folder="templates")

usersblp = Blueprint("usersblp",__name__,static_folder="static",template_folder="templates")

# ================== LOGIN [POST] =========================

# @cross_origin(origin='*',headers=['Content-Type','x-access-token'])
@usersblp.route("/login",methods=['GET'])
def login():
     
     # request_data = request.get_json()
     # if request_data is None or "email" not in  request_data or "password" not in request_data:
     #      return jsonify({'Message':'email & password are requeired !'}) ,400
     # return UsersDB.login(request_data)
     return ({'message':'koko'}),200



# ================== REGISTER DOCTOR [POST] =========================

@usersblp.route("/register/doctor",methods=['POST'])
def registerDoctor():
     
     if 'avatar' not in request.files or 'attachment' not in request.files:
          return{'message':'avatar and attachment are required even U would not upload it !'},400
     
     if request.form is None or "full_name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government_id" not in request.form or "specialist" not in request.form  or "deg_of_specialist_id" not in request.form :
          return jsonify({'Message':'Input data are missing !'}),400 
     
     # request_data = {}
     
     
     # request_data['user_type'] = '1'
     # request_data['status'] = '0'
     # request_data['profile_status'] = '1'


     return UsersDB.registerDoctor(data= request.form, files=request.files)


# ================== REGISTER Patient [POST] =========================

# @cross_origin(origin='*',headers=['Content-Type','x-access-token'])

@usersblp.route("/register/patient",methods=['POST'])
def registerPatient():
     
     if 'avatar' not in request.files :
          return{'message':'avatar is required even U would not upload it !'},400

     
     if request.form is None or "full_name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government_id" not in request.form or "address" not in request.form or "age" not in request.form :
          return jsonify({'Message':'Inputs data are missing !'}) ,400


     return UsersDB.registerPatient(data=request.form , files= request.files)


# ================== REGISTER Admin [POST] =========================

@usersblp.route("/register/admin",methods=['POST'])
def registerAdmin():
     

     if 'avatar' not in request.files :
          return{'message':'avatar is required even U would not upload it !'},400
     

     
     if request.form is None or "full_name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form :
          return jsonify({'Message':'Input data are missing !'}) ,400
     


     return UsersDB.registerAdmin(data=request.form , files=request.files)


# ================== Autism Test [POST] =========================

@usersblp.route("/test",methods=['POST'])
def autiTest():
     
     request_data = request.get_json()
     if request_data is None  or len(request_data) != 15:
          return jsonify({'Message':'Input data are missing !'}) ,400


     return UsersDB.autiTest(request_data)



# ================== PENDING DOCTOR [POST] =========================\

@usersblp.route("/doctors/pending",methods=['GET'])
@me.token_required
def pendingDoctors(token):
     
     request_data = request.get_json()
     # if request_data is None or "doctor_id" not in  request_data :
     #      return jsonify({'Message':'doctor_id is missing !'}) 


     return UsersDB.pendingDoctors(request_data)

# ================== CONFORM DOCTOR [POST] =========================\

@usersblp.route("/doctors/confirm",methods=['POST'])
@me.token_required
def confirmDoctor(token):
     
     request_data = request.get_json()
     if request_data is None or "doctor_id" not in  request_data :
          return jsonify({'Message':'doctor_id is missing !'}) ,400


     return UsersDB.confirmDoctor(request_data["doctor_id"])



# ================== REJECT DOCTOR [POST] =========================

@usersblp.route("/doctors/reject",methods=['POST'])
@me.token_required
def rejectDoctor(token):
     
     request_data = request.get_json()
     if request_data is None or "doctor_id" not in  request_data :
          return jsonify({'Message':'doctor_id is missing !'}) ,400


     return UsersDB.rejectDoctor(request_data["doctor_id"])


# ================== GET Current User Data (PROFILE) By Token [GET] =========================

@usersblp.route("/profile",methods=['GET'])
@me.token_required
def profile(token):
     
     return UsersDB.profile(id=str(token['uid']))


# ================== Update user profile [PUT] =========================

@usersblp.route("",methods=['PUT'])
@me.token_required
def updateUser(token):

     if 'avatar' not in request.files:
          return{'message':'avatar is required even U would not upload it !'},400
     
     
     # imagePath = UsersDB.uploadImage(request.files)
     
     return UsersDB.updateUser(userId=str(token['uid']) , data=request.form , imgFile = request.files['avatar'])



# ================== Add Clinic [POST] =========================

# @usersblp.route("/doctors/clinic",methods=['POST'])
# @me.token_required
# def addClinic(token):
#      request_data = request.get_json()
#      if request_data is None or "clinic_address" not in  request_data :
#           return jsonify({'Message':'clinic_address is missing !'}) 
#      request_data['uid'] = str(token['uid'])
#      return UsersDB.addClinic(data=request_data)

# # ================== Update Profile [POST] =========================

# @usersblp.route("/profile_status",methods=['POST'])
# @me.token_required
# def changeProfileStatus(token):
     
#      return UsersDB.getCurrentUser(id=str(token['uid']))




















#===============================================================================================================


# ================== get instructors [POST] =========================

@usersblp.route("/instructors",methods=['POST'])
@me.token_required
def getInstructors(token):

     return UsersDB.getInstructors()

# ================== get instudents [POST] =========================

@usersblp.route("/students",methods=['POST'])
@me.token_required
def getStudents(token):

     return UsersDB.getStudents()

@usersblp.route("/students/pending",methods=['POST'])
@me.token_required
def getStudentspending(token):

     return UsersDB.getStudents_binding()

@usersblp.route("/students/confirmed",methods=['POST'])
@me.token_required
def getStudentsconfirmed(token):

     return UsersDB.getStudents_confirmed()


# ================== GET Current User By Token [GET] =========================

@usersblp.route("",methods=['POST'])
@cross_origin(origin='*',headers=['Content-Type','x-access-token'])
@me.token_required
def getUserByToken(token):
     
     return UsersDB.getUser(id=str(token['uid']))


# ================== Update User [PUT] =========================
@usersblp.route("/profile",methods=['PUT'])
@me.token_required
def register(token):
     
     request_data = request.get_json()
     if request_data is None or "Name" not in  request_data or "Email" not in  request_data or "Nat_ID" not in  request_data:
          return jsonify({'Message':'Inputs data are missing !'}),400 



     return UsersDB.updateUser(id= str(token['uid']), data=request_data)

# ================== Update User Password [PUT] =========================

@usersblp.route("/updatepass",methods=['PUT'])
@me.token_required
def registerPassword(token):
     
     request_data = request.get_json()
     if request_data is None or "current_password" not in  request_data or "password" not in  request_data :
          return jsonify({'Message':'password data are missing !'}) 



     return UsersDB.updateUserpassword(id= str(token['uid']), data=request_data)

# ================== Delete User [DELETE] =========================

@usersblp.route("/<id>",methods=['DELETE'])
@me.token_required
def deleteUser(token,id):
     
     return UsersDB.deleteUser(id=id)

# ================== Confirm Student [POST] =========================

@usersblp.route("/confirmStudent/<id>",methods=['POST'])
@me.token_required
def confirmStudent(token,id):
     
     return UsersDB.confirmStudent(id=id)

# ================== Reject Student [POST] =========================

@usersblp.route("/rejectStudent/<id>",methods=['POST'])
@me.token_required
def rejectuser(token,id):
     
     return UsersDB.rejectStudent(id=id)

# ==================  Students Count [POST] =========================

@usersblp.route("/students/count",methods=['POST'])
@me.token_required
def getStuCount(token):

     return UsersDB.getStuCount()

# ================== Instructors Count [POST] =========================
@usersblp.route("/instructors/count",methods=['POST'])
@me.token_required
def getInsCount(token):

     return UsersDB.getInsCount()


@usersblp.route("",methods=['POST'])
@me.token_required
def moveToNextSem(token):
    return UsersDB.moveToNextSemster()