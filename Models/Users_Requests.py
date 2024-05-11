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
               return jsonify({'message':'Input data are missing !'}),400 


          return UsersDB.registerDoctor(data= request.form, files=request.files)
     
     # patient
     elif request.form['type'] == "patient": 

          # if 'avatar' not in request.files :
          #      return{'message':'avatar is required even U would not upload it !'},400

     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government" not in request.form or "city" not in request.form or "age" not in request.form :
               return jsonify({'message':'Inputs data are missing !'}) ,400


          return UsersDB.registerPatient(data=request.form , files= request.files)
     
     # admin
     elif request.form['type'] == "admin":
          # if 'avatar' not in request.files :
          #      return{'message':'avatar is required even U would not upload it !'},400
     

     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form :
               return jsonify({'message':'Input data are missing !'}) ,400
     
          return UsersDB.registerAdmin(data=request.form , files=request.files)
     
     else:
          return jsonify({'message':'enter  admin ,  doctor , patient ... not ' + request.form['type']}),400 

# ================== Autism Test [POST] =========================

@usersblp.route("/test",methods=['POST'])
def autiTest():

     
     request_data = request.get_json()
     
     if request_data is None  or len(request_data) != 15:
          print(len(request_data))
          
          return jsonify({'message':'Input data are missing !'}) ,400


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


# ================== GET Current User Data (PROFILE) By Token [GET] =========================

@usersblp.route("/profile",methods=['GET'])
@me.token_required
def profile(token):

     userID = 0

     try:
          request_data = request.get_json()
          if request_data is None or "user_id" not in  request_data :
               
               userID = token['uid'].split('.')[3]
               
          else:
               userID = request_data['user_id']
     except:
          return UsersDB.profile(id=token['uid'].split('.')[3])

     return UsersDB.profile(id=userID)


# ================== Update user profile [PUT] =========================

@usersblp.route("",methods=['POST'])
@me.token_required
def updateUser(token):

     if request.form is None or "type" not in  request.form:
          
          return jsonify({'message':'enter register type , admin ,  doctor ,  patient'}),400 
     
      # doctor
     if request.form['type'] == "doctor": 
     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government" not in request.form or "city" not in request.form :
               return jsonify({'message':'Input data are missing !'}),400 
     

      # patient
     elif request.form['type'] == "patient": 

          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government" not in request.form or "city" not in request.form or "age" not in request.form :
               return jsonify({'message':'Inputs data are missing !'}) ,400
          

     # Admin
     elif request.form['type'] == "admin":

     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form :
               return jsonify({'message':'Input data are missing !'}) ,400


     return UsersDB.updateUser(userId=str(token['uid'].split('.')[3]) , data=request.form , files=request.files)

# ================== DELETE USER [DELETE] =========================

@usersblp.route("",methods=['DELETE'])
@me.token_required
def deleteUser(token):

     request_data = request.get_json()
     if request_data is None or "user_id" not in  request_data :
          return jsonify({'message':'user_id is missing !'}) ,400

     request_data['uid'] = token['uid'].split('.')[3]

     return UsersDB.deleteUser(data=request_data)
