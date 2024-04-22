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
          return jsonify({'Message':'email & password are requeired !'}) ,400
     return UsersDB.login(request_data)
     



# ================== REGISTER [POST] =========================
@usersblp.route("/register",methods=['POST'])
def register():
     
     if request.form is None or "type" not in  request.form:
          
          return jsonify({'Message':'enter register type , admin ,  doctor ,  patient'}),400 
     

     # doctor
     if request.form['type'] == "doctor": 
     
          if 'cv' not in request.files :
               return{'message':str(request.files)},400
               return{'message':'cv is required !'},400
     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government" not in request.form or "city" not in request.form :
               return jsonify({'Message':'Input data are missing !'}),400 


          return UsersDB.registerDoctor(data= request.form, files=request.files)
     
     # patient
     elif request.form['type'] == "patient": 

          # if 'avatar' not in request.files :
          #      return{'message':'avatar is required even U would not upload it !'},400

     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form  or "government" not in request.form or "city" not in request.form or "age" not in request.form :
               return jsonify({'Message':'Inputs data are missing !'}) ,400


          return UsersDB.registerPatient(data=request.form , files= request.files)
     
     # admin
     elif request.form['type'] == "admin":
          # if 'avatar' not in request.files :
          #      return{'message':'avatar is required even U would not upload it !'},400
     

     
          if request.form is None or "name" not in  request.form or "email" not in  request.form or "phone" not in  request.form or "password" not in  request.form :
               return jsonify({'Message':'Input data are missing !'}) ,400
     
          return UsersDB.registerAdmin(data=request.form , files=request.files)
     
     else:
          return jsonify({'Message':'enter  admin ,  doctor , patient ... not ' + request.form['type']}),400 

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

     # if 'avatar' not in request.files:
     #      return{'message':'avatar is required even U would not upload it !'},400
     
     
     # imagePath = UsersDB.uploadImage(request.files)
     
     return UsersDB.updateUser(userId=str(token['uid']) , data=request.form , imgFile = request.files['avatar'])
