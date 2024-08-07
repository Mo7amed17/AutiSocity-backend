from DB_Connections.DB_connections import linkDB as db
from flask import jsonify
from components import myMethods as me
import jwt
import datetime
from ML.LR3 import doML
import os
import phonenumbers
# import constants 

#========================== REGISTERATION & LOGIN ==================================

    
baseURL = 'http://192.168.237.148:5000/'

###############    L O G I N     ################
def login(data):

        query   = me.selectQuery(tableName='vi_Users',where="email = '"+data['email']+"' AND password = '"+data['password']+"'")
    
    # try:
        db.cursor.execute(query)

        result = []

        result = me.usersModel(data=db.cursor.fetchall())  
        
        if len(result) == 0 :
            return   me.message(message="بيانات الدخول غير صحيحة !"),400
        
        else:

            if result[0]['user_type'] == 'doctor':

                query = me.selectQuery(tableName='Doctors',columnsName=['about','clinicAddress'],where="doctor_id = " + str(result[0]['id']))

                db.cursor.execute(query)

                for row in db.cursor.fetchall():
                    item_dic ={}
                    item_dic['about'] = row[0]
                    item_dic['clinicAddress'] = row[1]


                

                result[0]['about'] = item_dic['about']
                result[0]['clinicAddress'] = item_dic['clinicAddress']

            elif result[0]['user_type'] == 'patient':

                query = me.selectQuery(tableName='Patients',columnsName=['age','patient_name','test_result'],where="patient_id = " + str(result[0]['id']))

                db.cursor.execute(query)

                for row in db.cursor.fetchall():
                    item_dic ={}
                    item_dic['age'] = row[0]
                    item_dic['patient_name'] = row[1]
                    item_dic['test_result'] = row[2]


                

                result[0]['age'] = item_dic['age']
                result[0]['patient_name'] = item_dic['patient_name']
                result[0]['test_result'] = item_dic['test_result']

            

            if result[0]['status'] == 'pending' and result[0]['user_type'] == 'doctor' :

                return me.message(message='في إنتظار موافقة المسؤول !'),400
            
            if result[0]['status'] == 'rejected' and result[0]['user_type'] == 'doctor' :

                return me.message(message='تم رفض دخولك الي الموقع لعدم موافقة المسؤول !'),400
            
            token_text =  str(datetime.datetime.now().time().hour) + '.' + str(datetime.datetime.now().time().minute) +'.' + str(datetime.datetime.now().time().second)+'.' + str(result[0]["id"]) +'.' + str(datetime.datetime.now().time().microsecond)

            token = jwt.encode({'uid':token_text , 'exp':datetime.datetime.utcnow() + datetime.timedelta(weeks=2)},"654321" )
            return ({'message':'تم تسجيل الدخول بنجاح','token':token,'data':result[0]}),200
    # except Exception as e:
    #     print(e)
    #     return{'message':'حدث خطأ اثناء تسجيل الدخول'},400




    ###############    R E G I S T E R   D O C T O R S    ################

def registerDoctor(data,files):
        
        # query = "INSERT INTO Users (Name ,Email,Nat_ID,Password,User_type,Semester,Confirmed"+(",Department" if data["Department"] != 'all' else "")+") VALUES('"+data["name"]+"','"+data["email"]+"','"+data["Nat_ID"]+"','"+data["password"]+"', '"+data["user_type"]+"','"+data["semester"]+"', "+ "'"+data["confirmed"]+"'"+ ((",'"+data["Department"]+"'") if data["Department"] != 'all' else "")+    ")"                                                 
        # query = me.insertQuery(tableName='Users',columnsName=['full_name','email','phone','password','user_type','government_id','profile_status'] ,values=[data['full_name'],data['email'],data['phone'],data['password'],data['user_type'],data['government_id'],data['profile_status']])
        avatarpath = ''
        cvPath = ''
        
        
        try:
            cvPath = getAttachmentPath(file= files['cv'],type=1)
            avatarpath = getAttachmentPath(file= files['avatar'],type=0)

            
            
        except Exception as e:
            print("no avatar or cv was send:", e)

        # print('avatarpath')
        # print(avatarpath)
        # print('avatarpath')


        try:
            phone_number = phonenumbers.parse('+2' + data['phone'])
        except Exception as e:
            return{'message':'رقم الهاتف غير صالح !'},400


        

        query = me.procQuery(procName='AddNewDoctor',valuesDic={
             'name' : data['name'],
             'phone' : data['phone'],
             'email' : data['email'],
             'password' : data['password'],
             'government' : data['government'],
             'city' : data['city'],
            #  'specialist':data['specialist'],
            #  'deg_of_specialist_id':data['deg_of_specialist_id'],
             'attachment':cvPath,
             'image':avatarpath
        })

       
        try :
            db.cursor.execute(query)
            db.conn.commit()

            if avatarpath != '':
                 saveAttachment(attachmentFile= files['avatar'],oldAttachPath='' , newAttachPath=avatarpath ) 
            if cvPath != '':
                 saveAttachment(attachmentFile= files['cv'],oldAttachPath='' , newAttachPath=cvPath )

            
           
            
        except Exception as ex:
            
            if 'full_name_U' in str(ex.args[1]):
                return {'message':"الأسم موجود بالفعل"},400
            
            elif 'email_U' in str(ex.args[1]):
                return {'message':"البريد الألكتروني موجود بالفعل"},400
            
            elif 'phone_U' in str(ex.args[1]):
                return {'message':"رقم الهاتف موجود بالفعل"},400
            
            else:
                return {'message':str(ex)},400
            
        
        
        return {'message':"تم تسجيل الطبيب بنجاح , في انتظار موافقة المسؤول"},201        



    ###############    R E G I S T E R   P A T I E N T    ################

def registerPatient(data,files):
        
        
        avatarpath = ''
        try:
            avatarpath = getAttachmentPath(file= files['avatar'],type=0)
        except Exception as e:
            print("no avatar was send:", e)



        try:
            phone_number = phonenumbers.parse('+2' + data['phone'])
        except Exception as e:
            return{'message':'رقم الهاتف غير صالح !'},400



        # if phonenumbers.is_valid_number(phone_number):
        #     return{'message': 'Phone number is invalid !'},400


        # query = me.insertQuery(tableName='users',columnsName=['full_name','email','phone','password','user_type','government_id','profile_status'] , values=[data['full_name'],data['email'],data['phone'],data['password'],data['government_id']])


        if 'test_Result' in data:
            query = me.procQuery(procName='AddNewPatient',valuesDic={
                'name' : data['name'],
                'phone' : data['phone'],
                'email' : data['email'],
                'password' : data['password'],
                'government' : data['government'],
                'city' : data['city'],
                'age':data['age'],
                'image':avatarpath,
                'test_Result':data['test_Result'],
            })
        else:
             query = me.procQuery(procName='AddNewPatient',valuesDic={
                'name' : data['name'],
                'phone' : data['phone'],
                'email' : data['email'],
                'password' : data['password'],
                'government' : data['government'],
                'city' : data['city'],
                'age':data['age'],
                'image':avatarpath,
                })

        # return{'ss':str(query)}

        try :
            db.cursor.execute(query)
            db.conn.commit()

            if avatarpath != '':
                 saveAttachment(attachmentFile= files['avatar'],oldAttachPath='' , newAttachPath=avatarpath )
            
        except Exception as ex:
            # return{'ss':str(str(ex.args[1]))}
            
            if 'full_name_U' in str(str(ex.args[1])):
                return {'message':"الأسم موجود بالفعل"},400
            
            elif 'email_U' in str(ex.args[1]):
                return {'message':"البريد الألكتروني موجود بالفعل"},400
            
            elif 'phone_U' in str(ex.args[1]):
                return {'message':"رقم الهاتف موجود بالفعل"},400
            
            else:
                return {'message':str(ex)},400
            
        
        
        return {'message':"تم تسجيل المريض بنجاح "},201  


###############    R E G I S T E R   A D M I N    ################

def registerAdmin(data , files):
        
        avatarpath = ''

        try:
            avatarpath = getAttachmentPath(file= files['avatar'],type=0)
        except Exception as e:
            print("no avatar was send:", e)

        

        query = me.insertQuery(tableName='users',columnsName=['name','email','phone','password','user_type','image'] , values=[data['name'],data['email'],data['phone'],data['password'],'0',avatarpath])
        

        try :
            db.cursor.execute(query)
            db.conn.commit()

            if avatarpath != '':
                saveAttachment(attachmentFile= files['avatar'] , oldAttachPath='' , newAttachPath=avatarpath )
            
        except Exception as ex:
            
            if 'full_name_U' in str(ex.args[1]):
                return {'message':"الأسم موجود بالفعل"},400
            
            elif 'email_U' in str(ex.args[1]):
                return {'message':"البريد الألكتروني موجود بالفعل"},400
            
            elif 'phone_U' in str(ex.args[1]):
                return {'message':"رقم الهاتف موجود بالفعل"},400
            
            else:
                return {'message':str(ex)},400
            
        
        
        return {'message':"تم تسجيل الأدمن بنجاح "},201  


###############     A U T I S M   T E S T    ################
def autiTest(data):

    result = str(doML(inputData=data['data']))

    if('user_id' in data and result != None):

        # return{'sss':'ssss'}
        # query = me.updateQuery(tableName='Patients',columnsName=['test_result'] , values=[result])
        query = me.updateQuery(tableName='Patients',valuesDic={'test_result':result},where='patient_id = '+str(data['user_id']))
        try :
            db.cursor.execute(query)
            db.conn.commit()
            
        except Exception as ex:
                print(str(ex))
                return {'message':str(ex)},400

     
    return {"result":result}





###############     G E T   P E N D I N G   D O C T O R    ################
def pendingDoctors(uid):


    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403


    query = me.selectQuery(tableName='vi_Users',where="status = '"+"pending"+"'" , orderby='create_at,DESC')

    # return{'ss':query}

    

    try :
        db.cursor.execute(query)

        result = me.usersModel(data=db.cursor.fetchall())

        return{'data':result}

            
    except Exception as ex:

        return {'message':str(ex)},400
    
            

###############     C O N F I R M   D O C T O R    ################
def confirmDoctor(docID , uid):
    
    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403
    
    whereCond = 'doctor_id = '+str(docID)

    query = me.selectQuery(tableName='Doctors' , columnsName=['status'],where=whereCond)

    try :
        db.cursor.execute(query)
        data=db.cursor.fetchall()

        if len(data) == 0 :

            return{'message':'no doctors found with this id !'},400
        
        if data[0][0] == True:

            return{'message':'تم قبول هذا الطبيب من قبل !'},400
            

        query = me.updateQuery(tableName='Doctors',valuesDic={'status':'1'},where='doctor_id = '+"'"+ str(docID) + "'")

        db.cursor.execute(query)
        db.conn.commit()
            
    except Exception as ex:

        return {'message':str(ex)},400
            
        
        
    return {'message':"تم قبول الطبيب بنجاح "},200


###############     R E J E C T   D O C T O R    ################
def rejectDoctor(docID , uid):

    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403


    whereCond = 'doctor_id = '+str(docID)

    query = me.selectQuery(tableName='Doctors' , columnsName=['status'],where=whereCond)

    try :
        db.cursor.execute(query)
        data=db.cursor.fetchall()

        if len(data) == 0 :

            return{'message':'no doctors found with this id !'},400
        if data[0][0] == False:

            return{'message':'تم رفض هذا الطبيب من قبل !'},400


        query = me.updateQuery(tableName='Doctors',valuesDic={'status':'0'},where='doctor_id = '+"'"+ str(docID) + "'")
    
        db.cursor.execute(query)
        db.conn.commit()
            
    except Exception as ex:

        return {'message':str(ex)},400
            
        
        
    return {'message':"تم رفض الطبيب بنجاح "},200


###############      G E T   A D M I N S     ################
def getAdmins(uid):

    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403



    query = me.selectQuery(tableName='vi_Users',columnsName=['id' , 'name' , 'email' ,'image','user_type'] ,where='user_type = \'admin\' AND id <> 1')
    
    # try :
    db.cursor.execute(query)

    result = []
    
    for row in db.cursor.fetchall():
        data=profileModel(row=row, getBasicData=True)
        result.append(data[0])

    

    # if len(result) == 0 :

    #     return{'message':'no admins found'},400
    
    result.reverse()
    
    return{'data':result},200

            
    # except Exception as ex:

    #     return {'message':str(ex)},400
            

###############      G E T   D O C T O R S     ################
def getDoctors(uid):

    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403



    query = me.selectQuery(tableName='vi_Users',columnsName=['id' , 'name' , 'email' ,'image','user_type'] ,where='user_type = \'doctor\'')
    
    try :
        db.cursor.execute(query)

        result = []
        
        for row in db.cursor.fetchall():
            data=profileModel(row=row , getBasicData=True)
            result.append(data[0])

        

        # if len(result) == 0 :

            # return{'message':'no doctors found','data':[]},400
        
        result.reverse()
        
        return{'data':result},200

            
    except Exception as ex:

        return {'message':str(ex)},400
    

###############      G E T   P A T I E N T S     ################
def getPatients(uid):

    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403



    query = me.selectQuery(tableName='vi_Users',columnsName=['id' , 'name' , 'email' ,'image','user_type'] ,where='user_type = \'patient\'')
    
    try :
        db.cursor.execute(query)

        result = []
        
        for row in db.cursor.fetchall():
            data=profileModel(row=row , getBasicData=True)
            result.append(data[0])

        

        # if len(result) == 0 :

        #     return{'message':'no patient found','data':[]},400
        
        result.reverse()
        
        return{'data':result},200

            
    except Exception as ex:

        return {'message':str(ex)},400

###############      G E T   D O C T O R S   A N D   P A T I E N T S     ################
def getUsersList(uid):

    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403



    query = me.selectQuery(tableName='vi_Users',columnsName=['id' , 'name' , 'email' ,'image','user_type'] ,where='user_type = \'patient\' OR user_type = \'doctor\'')
    
    try :
        db.cursor.execute(query)

        result = []
        
        for row in db.cursor.fetchall():
            data=profileModel(row=row , getBasicData=True)
            result.append(data[0])

        

        # if len(result) == 0 :

        #     return{'message':'no data found','data':[]},400
        
        result.reverse()
        
        return{'data':result},200

            
    except Exception as ex:

        return {'message':str(ex)},400


###############     P R O F I L E     ################
def profile(id):

        query = me.procQuery(procName='getUserProfile',valuesDic={
             'u_id':str(id)
        })
        
        
        # return{'sss':query}
        result = []
        
        db.cursor.execute(query)
        
        # result["message"] = "data retrieved succesfully"
        data = db.cursor.fetchone()
        if(data != None):
            
            result = profileModel(row=data)
        

            # query2 = me.selectQuery(tableName='profile_Images' , columnsName=['image'] , where= 'user_id = '+result[0]['id'])
            # db.cursor.execute(query2)

            # imagesResult = []

            # for row in db.cursor.fetchall():

            #     item_dic ={}
            #     item_dic["image"] = row[0]

            #     imagesResult.append(item_dic)
            
            # result[0]['images'] = imagesResult
        



        if len(result) == 0 :
            
            return   {'message':"لا يوجد بيانات !",'data':[]},200
        else:
            # result[0].pop("user_type")
            
            return {'message':'تم إسترجاع البيانات بنجاح !','data':result[0]}
            




def updateUserData(userId,data,files,userType):
     

    req_img_path = None

    oldImgPath = '' # null or value

    if 'avatar' not in files:
        #delete
        req_img_path = None
        oldImgPath = getOldAttachmentPath(userId=userId)

    elif files['avatar'].filename == '':
        #keep
        req_img_path = ''
    else:
        #update
        oldImgPath = getOldAttachmentPath(userId=userId)
        req_img_path = getAttachmentPath(file= files['avatar'],type=0)


    
    # return{'s':'s'}
    

    # newImgPath = ''
    
    # try:
    #     newImgPath = getAttachmentPath(file= files['avatar'],type=0)

    # except Exception as e:
    #     newImgPath = None
    #     print("no avatar was send:", e)

    
    

    

    # try:
    #     db.cursor.execute(query)

    #     password = db.cursor.fetchone()[0]

    #     if data['password'] != password :
    #         return {'message':'الرقم السري غير صحيح !'},400
    # except :
    #     return{'message':'id not found !'},400
    
    
    # if newImgPath == '' or newImgPath == None:
    #         avatarpath = None
    # else:
    #         # avatarpath = str(os.path.basename(newImgPath))
    #         avatarpath = newImgPath

        
    # print('img pahhhhhhhhhhhhhhh')
    # print(avatarpath)
    # print(newImgPath)


    try:

        def saveDeleteImage():
                if req_img_path == None:
                    
                    deleteAttachment(attachmentPath=oldImgPath)
                
                    
                elif req_img_path != '':
                    

                    saveAttachment(attachmentFile=files['avatar'],oldAttachPath=oldImgPath,newAttachPath=req_img_path)
        
    
        
        

        query = ''
        if userType == 2:  #PATIENT

            if req_img_path == None:
                #delete

                query = me.procQuery(procName='updatePatient',valuesDic={
                    'uId' : userId,
                    'name' : data['name'],
                    'phone' : data['phone'],
                    'email' : data['email'],
                    'government' : data['government'],
                    'city' : data['city'],
                    'patient_name' : data['patient_name'],
                    'age' : data['age'],
                    'image':''
                    
                })

            elif req_img_path == '':
                #keep
                query = me.procQuery(procName='updatePatient',valuesDic={
                        'uId' : userId,
                        'name' : data['name'],
                        'phone' : data['phone'],
                        'email' : data['email'],
                        'government' : data['government'],
                        'city' : data['city'],
                        'patient_name' : data['patient_name'],
                        'age' : data['age'],
                        
                    })
                
            else:
                #update
                query = me.procQuery(procName='updatePatient',valuesDic={
                        'uId' : userId,
                        'name' : data['name'],
                        'phone' : data['phone'],
                        'email' : data['email'],
                        'government' : data['government'],
                        'city' : data['city'],
                        'patient_name' : data['patient_name'],
                        'age' : data['age'],
                        'image':req_img_path
                        
                    })
        
            db.cursor.execute(query)
                
            saveDeleteImage()

            return{'message':'تم تعديل بيانات المريض بنجاح !'},200

        elif userType == 1:  #DOCTOR

            if req_img_path == None:

                query = me.procQuery(procName='updateDoctor',valuesDic={
                        'uId' : userId,
                        'name' : data['name'],
                        'phone' : data['phone'],
                        'email' : data['email'],
                        'government' : data['government'],
                        'city' : data['city'],
                        'about' : data['about'],
                        'clinicAddress' : data['clinicAddress'],
                        'image':''
                        
                    })
            elif req_img_path == '':

                query = me.procQuery(procName='updateDoctor',valuesDic={
                    'uId' : userId,
                    'name' : data['name'],
                    'phone' : data['phone'],
                    'email' : data['email'],
                    'government' : data['government'],
                    'city' : data['city'],
                    'about' : data['about'],
                    'clinicAddress' : data['clinicAddress']
                    })

            else:

                query = me.procQuery(procName='updateDoctor',valuesDic={
                    'uId' : userId,
                    'name' : data['name'],
                    'phone' : data['phone'],
                    'email' : data['email'],
                    'government' : data['government'],
                    'city' : data['city'],
                    'about' : data['about'],
                    'clinicAddress' : data['clinicAddress'],
                    'image':req_img_path
                })
            
            db.cursor.execute(query)

            saveDeleteImage()

            return{'message':'تم تعديل بيانات الطبيب بنجاح !'},200
        
        elif userType == 0:  #ADMIN

            if req_img_path == None:

                query = me.updateQuery(tableName='Users' , valuesDic={
                "name" : data['name'],
                "phone":data['phone'],
                'email' : data['email'],
                "image":''
                },where='id ='+userId)
                
            elif req_img_path == '':
                query = me.updateQuery(tableName='Users' , valuesDic={
                "name" : data['name'],
                "phone":data['phone'],
                'email' : data['email'],
                },where='id ='+userId)
            
            else:
                query = me.updateQuery(tableName='Users' , valuesDic={
                "name" : data['name'],
                "phone":data['phone'],
                'email' : data['email'],
                'image':req_img_path
                },where='id ='+userId)
                
            db.cursor.execute(query)

            saveDeleteImage()

            return{'message':'تم تعديل بيانات الأدمن  بنجاح !'},200



    except Exception as ex:
        
        if 'full_name_U' in str(ex.args[1]):
            return {'message':"الأسم موجود بالفعل"},400
        
        elif 'email_U' in str(ex.args[1]):
            return {'message':"البريد الألكتروني موجود بالفعل"},400
        
        elif 'phone_U' in str(ex.args[1]):
            return {'message':"رقم الهاتف موجود بالفعل"},400
        
        else:
            return {'message':str(ex)},400



def changeProfileStauts(data):
     


    query = me.selectQuery(columnsName=['profile_status'],tableName='Users',where='id = '+str(data['uid']))

    

    try:
        db.cursor.execute(query)

        profile_status = db.cursor.fetchone()[0]

       
    except :
        return{'message':'id not found !'},400

    
    query = me.updateQuery(tableName='Users',valuesDic={'profile_status':str(not profile_status)},where='id = '+"'"+ str(data['uid']) + "'")

    try:
        db.cursor.execute(query)
        db.conn.commit()

        return {'message':'تم تغيير صلاحية الوصول الي الملف الشخصي بنجاح'},200

    except Exception as ex:

        return {'message':str(ex)},400
        
        

def updateUserPassword(data):
     


    query = me.selectQuery(columnsName=['password'],tableName='Users',where='id = '+str(data['uid']))

    

    try:
        db.cursor.execute(query)

        password = db.cursor.fetchone()[0]

        if data['old_password'] != password :
            return {'message':'الرقم السري غير صحيح !'},400
    except :
        return{'message':'id not found !'},400

    
    query = me.updateQuery(tableName='Users',valuesDic={'password':data['new_password']},where='id = '+"'"+ str(data['uid']) + "'")

    try:
        db.cursor.execute(query)
        db.conn.commit()

        return {'message':'تم تعديل الرقم السري بنجاح'},200

    except Exception as ex:

        return {'message':str(ex)},400
        
        


def deleteUser(data):

    ## check if admin

    userType = me.getUserTypeByUserID(uid=data['uid'])

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403
    
    
    
    try :
    
        query = me.selectQuery(tableName='Users',columnsName=['user_type'],where='id = '+str(data['user_id']))
        db.cursor.execute(query)
        result=db.cursor.fetchall()
        deletedUserType = result[0][0]
        
        
        
        if deletedUserType == 0 and data['uid'] != '1':
            return{'message':'Only super admin can delete admins'},400


        query = me.deleteQuery(tableName='Users',where='id = '+str(data['user_id']))
        db.cursor.execute(query)
        db.conn.commit()

        if deletedUserType == 0 :
            return {'message':'تم حذف المسؤول بنجاح'},200
        elif deletedUserType == 1 :
            return {'message':'تم حذف الطبيب بنجاح'},200
        else:
            return {'message':'تم حذف المريض بنجاح'},200
        
            
    
        
    except Exception as ex:
        return {'message':'no user with this id'},400
        


def getMessengers(uid):

    query = me.procQuery(procName='getMessengers',valuesDic={
        'user_id':uid,
    })
    
    try :
        db.cursor.execute(query)

        result=messageModel(data=db.cursor.fetchall())
            
        
            
    except Exception as ex:

        return {'message':str(ex)},400

    return {'data':result},200


def getMessages(data):

    query = me.procQuery(procName='getUserMessages',valuesDic={
        'user_id':data['uid'],
        'receiver_id':data['receiver_id'],
    })

    try :
        db.cursor.execute(query)

        result=messageModel(data=db.cursor.fetchall(),isGetMessage=True)
            
        
            
    except Exception as ex:

        return {'message':str(ex)},400

    return {'data':result},200



# ==================  like a post [POST] =========================

def addMessage(data):

    
    # query = me.insertQuery(tableName='Messages',columnsName=['from_user_id','to_user_id','message','date'],values=[int(data['uid']) , int(data['reveiver_id']) , data['message']])

    query = me.procQuery(procName='insertMessage',valuesDic={
        'from_user_id':data['uid'],
        'to_user_id':data['receiver_id'],
        'message':data['message'],
    })

    try :
        db.cursor.execute(query)
        db.conn.commit()
        return{'message':True}
        # return{'message':'تم إرسال الرسالة بنجاح !'},200
            
    except Exception as ex:
      
      return {'message':False}




def search(data):
     
    whereQuery = 'name like \'%'+data['name'] + '%\' AND id <> '+ str(data['uid'] + ' AND user_type <> 0')

    if("country" in data):
        
        whereQuery += ' and city = \'' + data['country']+ '\''

    if("government" in data):
        
        whereQuery += ' and government = \'' + data['government']+ '\''


    query = me.selectQuery(columnsName=['id','name','city','government','image'],tableName='Users',where=whereQuery)

    
    # return{'aa':query}
    try:
        db.cursor.execute(query)

        result =searchModel(db.cursor.fetchall()) 


        return{'data':result}

    except Exception as ex:

        return {'message':str(ex)},400



def addImages(uid,image):

    avatarpath = ''
    
    avatarpath = getAttachmentPath(file= image ,type=0)
    


    query = me.insertQuery(tableName='profile_Images',columnsName=['patient_id','image'] , values=[uid,avatarpath])

    
    # return{'aa':query}
    try:
        db.cursor.execute(query)
        db.conn.commit()


        return{'data':'تم غضافة الصورة بنجاح'},200

    except Exception as ex:

        return {'message':str(ex)},400




# def addClinic(data):

        

#         query = me.insertQuery(tableName='Clinics',columnsName=['doctor_id','address'],values=[data['uid'],data['clinic_address']])
#         # return{'s':query}

#         try :
#             db.cursor.execute(query)
#             db.conn.commit()
            
#         except Exception as ex:

#             return {'message':str(ex)},400
            
#         return {'message':'تم إضافة عنوان عيادة جديدة بنجاح !'},201



# def addClinic(data):        

#         query = me.selectQuery(tableName='Clinics',columnsName=['address'],where='doctor_id ='+str(data['uid']))

#         try :
#             db.cursor.execute(query)
#             db.conn.commit()
            
#         except Exception as ex:

#             return {'message':str(ex)},400
            
#         return {'message':'تم إضافة عنوان عيادة جديدة بنجاح !'},201







def messageModel(data , isGetMessage = False):

        result = []
        
        
        for row in data:

            item_dic ={}
            item_dic["id"] = row[0]
            item_dic["message"] = row[1]
            item_dic["date"] = row[2]
            item_dic["is_my_message"] = row[3]
            item_dic["name"] = row[4]   
            item_dic["image"] = row[5]
                
            
                
            # else:
            #     item_dic["uId"] = row[3]
            #     item_dic["name"] = row[4]
            #     item_dic["image"] = row[5]

            result.append(item_dic)

        return result



def profileModel(row , getBasicData = False):

        result = []
        
        

        item_dic ={}
        item_dic["id"] = row[0]
        item_dic["name"] = row[1]
        item_dic["email"] = row[2]
        item_dic["image"] = row[3]
        item_dic["user_type"] = row[4]

        if getBasicData == False :
            item_dic["phone"] = row[5]

        if (row[4] == 'doctor' or row[4] == 'patient') and getBasicData == False :
            

            item_dic["government"] = row[6]
            item_dic["city"] = row[7]
            item_dic["profile_status"] = row[8]
            
            if row[4] == 'doctor':
                
                item_dic["doctor_id"] = row[9]
                item_dic["about"] = row[10]
                item_dic["clinicAddress"] = row[11]

            elif row[4] == 'patient':
                item_dic["age"] = row[9]
                item_dic["patient_name"] = row[10]
                item_dic["test_result"] = row[11]

            
            
        result.append(item_dic)

        return result



def searchModel(data):

        result = []
        
        for row in data:
        

            item_dic ={}
            item_dic["id"] = row[0]
            item_dic["name"] = row[1]
            item_dic["country"] = row[2]
            item_dic["government"] = row[3]
            item_dic["image"] = row[4]
            

                
            result.append(item_dic)

        return result


def getAttachmentPath(file,type):

    fullPath = ''

    if file.filename != '':

        uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')

        if type == 0 : # avatar image
        
            # dic =  os.path.join('http://127.0.0.1:5000/uploads/', "uploads", "avatars")
            dic = baseURL
        
        else: # CV
             
            #  dic = os.path.join('http://127.0.0.1:5000/uploads/', "uploads", "CVs") 

             dic = baseURL

        

        # dic = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads", "CVs") 
        
        

        

        # dir ='http://127.0.0.1:5000/uploads/'+uniq_filename +  file.filename

        # return{'ss':dir}

        # print(dir)
                    
        fullPath = f'{dic}{uniq_filename}{file.filename}'

        fullPath.replace("\\\\","\\")

        fullPath.replace("\\","/")

        # print('1111111s25111')
        # print(fullPath)
        # print('11111111111')
        # print(fullPath)
        # print('111111111111')
        # print(file.filename)

        #
          
        

    return fullPath


def getOldAttachmentPath(userId):
    query = me.selectQuery(tableName='Users' , columnsName=['image'],where='id = ' +userId)

    db.cursor.execute(query)

    

    oldImgPath = db.cursor.fetchone()[0]

    return oldImgPath

    

def saveAttachment(attachmentFile,oldAttachPath , newAttachPath):


    print('save')
    # print(oldAttachPath)
    # print(newAttachPath)
    print('save')

    if oldAttachPath and oldAttachPath != '':

        try:
            deleteAttachment(oldAttachPath)
        except Exception as ex:
            print(str(ex))



    fullPath = ''

    fullPath = newAttachPath

    if fullPath and fullPath != '':
       
        dic = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads")

        
        # print(dic)
        attachmentFile.save(dic+'\\' + os.path.basename(fullPath))

def deleteAttachment(attachmentPath):
    

    print('removeeeee')
    # print(attachmentPath)
    print('removeeeee')

    if attachmentPath and attachmentPath != '':

        dic = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "uploads")

        fullPath = f'{dic}\{os.path.basename(attachmentPath)}'

        print('fullPath')
        # print(fullPath)
        print('fullPath')

        os.remove(fullPath)

        print('removed !!!!!!!!!!!!')

        



# def onlyAdminAllowed(uid):
#     userType = getUserTypeByUserID(uid=uid)

#     print(userType)

#     if userType != 0 :
#         return{'message':'Permission denied ,Only admins allowed !'},403


#===============================================================================================================
