from flask import Blueprint , jsonify ,request
from components import myMethods as me
from flask_cors import cross_origin
from DB_Connections.DB_EndPoints_Connections import UsersDB


# log_reg_blp = Blueprint("log_reg_blp",__name__,static_folder="static",template_folder="templates")

usersblp = Blueprint("usersblp",__name__,static_folder="static",template_folder="templates")

# ================== LOGIN [POST] =========================

# @cross_origin(origin='*',headers=['Content-Type','x-access-token'])
@usersblp.route("/login",methods=['POST'])
def login():
     
     request_data = request.get_json()
     if request_data is None or "email" not in  request_data or "password" not in request_data:
          return jsonify({'message':'email & password are requeired !'}) ,400
     return UsersDB.login(request_data)
     



# ================== REGISTER [POST] =========================
@usersblp.route("/register",methods=['POST'])
def register():
     
     if request.form is None or "type" not in  request.form:
          
          return jsonify({'message':'enter register type , admin ,  doctor ,  patient'}),400 
     

     # doctor
     if request.form['type'] == "doctor": 

          
     
          if 'cv' not in request.files or str(request.files['cv'].filename) == '':
               return{'message':'cv is required !'},400
     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government" not in request.form or "city" not in request.form :
               return jsonify({'message':'enter name , email , phone ,  password ,  government , city'}),400 


          return UsersDB.registerDoctor(data= request.form, files=request.files)
     
     # patient
     elif request.form['type'] == "patient": 

          # if 'avatar' not in request.files :
          #      return{'message':'avatar is required even U would not upload it !'},400

     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government" not in request.form or "city" not in request.form or "age" not in request.form :
               return jsonify({'message':'enter name , email , phone ,  password ,  government , city , age'}) ,400


          return UsersDB.registerPatient(data=request.form , files= request.files)
     
     # admin
     elif request.form['type'] == "admin":
          # if 'avatar' not in request.files :
          #      return{'message':'avatar is required even U would not upload it !'},400
     

     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form :
               return jsonify({'message':'enter name , email , phone ,  password '}) ,400
     
          return UsersDB.registerAdmin(data=request.form , files=request.files)
     
     else:
          return jsonify({'message':'enter  admin ,  doctor , patient ... not ' + request.form['type']}),400 


# ================== Autism Test [POST] =========================

@usersblp.route("/test",methods=['POST'])
def autiTest():

     
     request_data = request.get_json()
     
     if request_data is None  or 'data' not in request_data:
          return jsonify({'message':'data is missing !'}) ,400


     if len(request_data['data']) != 15:
          print(len(request_data))
          
          return jsonify({'message':'list of length = 15 is missing !'}) ,400


     return UsersDB.autiTest(request_data)




# ================== PENDING DOCTOR [POST] =========================\

@usersblp.route("/doctors/pending",methods=['GET'])
@me.token_required
def pendingDoctors(token):

     uid = token['uid'].split('.')[3]



     return UsersDB.pendingDoctors(uid=uid)

# ================== CONFiRM DOCTOR [POST] =========================\

@usersblp.route("/doctors/confirm",methods=['POST'])
@me.token_required
def confirmDoctor(token):

     
     
     request_data = request.get_json()
     if request_data is None or "doctor_id" not in  request_data :
          return jsonify({'message':'doctor_id is missing !'}) ,400
     
     uid = token['uid'].split('.')[3]


     return UsersDB.confirmDoctor(docID=request_data["doctor_id"],uid=uid)



# ================== REJECT DOCTOR [POST] =========================

@usersblp.route("/doctors/reject",methods=['POST'])
@me.token_required
def rejectDoctor(token):
     
     request_data = request.get_json()
     if request_data is None or "doctor_id" not in  request_data :
          return jsonify({'message':'doctor_id is missing !'}) ,400

     uid = token['uid'].split('.')[3]

     return UsersDB.rejectDoctor(docID=request_data["doctor_id"],uid=uid)
     



# ================== GET ADMINS [GET] =========================

@usersblp.route("/admins",methods=['GET'])
@me.token_required
def getAdmins(token):

     return UsersDB.getAdmins(uid=token['uid'].split('.')[3])

# ================== GET DOCTORS [GET] =========================

@usersblp.route("/doctors",methods=['GET'])
@me.token_required
def getDoctors(token):

     return UsersDB.getDoctors(uid=token['uid'].split('.')[3])

# ================== GET PATIENTS [GET] =========================

@usersblp.route("/patients",methods=['GET'])
@me.token_required
def getPatients(token):

     return UsersDB.getPatients(uid=token['uid'].split('.')[3])


@usersblp.route("/list",methods=['GET'])
@me.token_required
def getUsersList(token):

     return UsersDB.getUsersList(uid=token['uid'].split('.')[3])


# ================== GET Current User Data (PROFILE) By Token [GET] =========================

@usersblp.route("/profile",methods=['PUT'])
@me.token_required
def profile(token):

     

     userID = 0

     try:
          request_data = request.get_json()
          if request_data is None or "user_id" not in  request_data:
               
               userID = token['uid'].split('.')[3]
          else:
               userID = request_data['user_id']
     except:
          return UsersDB.profile(id=token['uid'].split('.')[3])

     return UsersDB.profile(id=userID)


# ================== Update user profile [PUT] =========================

@usersblp.route("/update",methods=['POST'])
@me.token_required
def updateUser(token):

     # if request.form is None or "type" not in  request.form:
          
     #      return jsonify({'message':'enter register type , admin ,  doctor ,  patient'}),400 

     usertype = me.getUserTypeByUserID(str(token['uid'].split('.')[3]) )

     
      # doctor
     if usertype == 1: 
     
          if request.form is None or "name" not in  request.form  or "phone" not in  request.form or "email" not in  request.form  or "government" not in request.form or "city" not in request.form or "about" not in request.form or "clinicAddress" not in request.form:
               return jsonify({'message':'name,phone,email,government,city,about,clinicAddress are missing !'}),400 
     

      # patient
     elif usertype == 2: 

          if request.form is None or "name" not in  request.form  or "phone" not in  request.form or "email" not in  request.form or "government" not in request.form or "city" not in request.form or "age" not in request.form or "patient_name" not in request.form:
               return jsonify({'message':'name ,phone , email,government,city,age,patient_name  are missing !'}) ,400
          

     # Admin
     elif usertype == 0:

     
          if request.form is None or "name" not in  request.form or "phone" not in  request.form or "email" not in  request.form  :
               return jsonify({'message':'name ,phone , email  are missing !'}) ,400


     return UsersDB.updateUserData(userId=str(token['uid'].split('.')[3]) , data=request.form , files=request.files , userType=usertype)

@usersblp.route("/update/password",methods=['POST'])
@me.token_required
def updateUserPassword(token):

     request_data = request.get_json()

     if request_data is None or "old_password" not in  request_data or "new_password" not in  request_data:
          
          return jsonify({'message':'old_password or new_password is missing !'}) ,400
     
     request_data['uid'] = token['uid'].split('.')[3]

     return UsersDB.updateUserPassword(data=request_data)


@usersblp.route("/update/profile_status",methods=['POST'])
@me.token_required
def changeProfileStauts(token):

     request_data = {}
     
     request_data['uid'] = token['uid'].split('.')[3]

     return UsersDB.changeProfileStauts(data=request_data)
# ================== DELETE USER [DELETE] =========================

@usersblp.route("",methods=['DELETE'])
@me.token_required
def deleteUser(token):

     request_data = request.get_json()
     if request_data is None or "user_id" not in  request_data :
          return jsonify({'message':'user_id is missing !'}) ,400

     request_data['uid'] = token['uid'].split('.')[3]

     return UsersDB.deleteUser(data=request_data)


@usersblp.route("/messengers",methods=['GET'])
@me.token_required
def getMessengers(token):

     return UsersDB.getMessengers(uid=token['uid'].split('.')[3])


@usersblp.route("/messages",methods=['PUT'])
@me.token_required
def getMessages(token):

     request_data = request.get_json()
     if request_data is None or "receiver_id" not in  request_data :
          return jsonify({'message':'receiver_id is missing !'}) ,400

     request_data['uid'] = token['uid'].split('.')[3]

     return UsersDB.getMessages(data=request_data)


# @usersblp.route("/messages",methods=['POST'])
# @me.token_required
# def addMessage(token):

#      request_data = request.get_json()
#      if request_data is None or "receiver_id" not in  request_data or "message" not in  request_data :
#           return jsonify({'message':'receiver_id or message is missing !'}) ,400

#      request_data['uid'] = token['uid'].split('.')[3]

#      return UsersDB.addMessage(data=request_data)


@usersblp.route("/search",methods=['POST'])
@me.token_required
def search(token):

     request_data = request.get_json()
     if request_data is None or "name" not in  request_data:
          return jsonify({'message':'name is missing !'}) ,400

     request_data['uid'] = token['uid'].split('.')[3]

     return UsersDB.search(data=request_data)

@usersblp.route("/image",methods=['POST'])
@me.token_required
def image(token):
     
     if 'image' not in request.files or str(request.files['image'].filename) == '':
               return{'message':'image is required !'},400

      

     return UsersDB.addImages(uid=token['uid'].split('.')[3] , image=request.files['image'])