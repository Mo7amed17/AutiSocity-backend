from DB_Connections.DB_connections import LinkDatabase
from flask import jsonify
from components import myMethods as me
import jwt
import datetime
from ML.LR3 import doML
import os
db = LinkDatabase()

#========================== REGISTERATION & LOGIN ==================================

    ###############    L O G I N     ################
    
def login(data):
        

        query = me.selectQuery(tableName='vi_Users',where="email = '"+data['email']+"' AND password = '"+data['password']+"'")
        
        
        
        db.cursor.execute(query)

        result = me.usersModel(data=db.cursor.fetchall())        
        
        if len(result) == 0 :
            
            return   me.message(message="بيانات الدخول غير صحيحة !"),400
        
        else:
            if result[0]['status'] == 'pending' and result[0]['user_type'] == 'doctor' :

                return me.message(message='في إانتظار موافقة المسؤول !'),400
            
            if result[0]['status'] == 'rejected' and result[0]['user_type'] == 'doctor' :

                return me.message(message='تم رفض دخولك الي الموقع لعدم موافقة المسؤول !'),400
    
            
            token = jwt.encode({'uid':result[0]["id"] , 'exp':datetime.datetime.utcnow() + datetime.timedelta(weeks=9999)},"654321" )
            result[0].pop("id")
            return ({'message':'تم تسجيل الدخول بنجاح','token':token,'data':result[0]}),200



    ###############    R E G I S T E R   D O C T O R S    ################

def registerDoctor(data,files):
        
        # query = "INSERT INTO Users (Name ,Email,Nat_ID,Password,User_type,Semester,Confirmed"+(",Department" if data["Department"] != 'all' else "")+") VALUES('"+data["name"]+"','"+data["email"]+"','"+data["Nat_ID"]+"','"+data["password"]+"', '"+data["user_type"]+"','"+data["semester"]+"', "+ "'"+data["confirmed"]+"'"+ ((",'"+data["Department"]+"'") if data["Department"] != 'all' else "")+    ")"                                                 
        # query = me.insertQuery(tableName='Users',columnsName=['full_name','email','phone','password','user_type','government_id','profile_status'] ,values=[data['full_name'],data['email'],data['phone'],data['password'],data['user_type'],data['government_id'],data['profile_status']])
        avatarpath = ''
        cvPath = ''
        try:
            avatarpath = getAttachmentPath(file= files['avatar'],type=0)
            
            cvPath = getAttachmentPath(file= files['cv'],type=1)
        except Exception as e:
            print("no avatar or cv was send:", e)


        

        

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

            if cvPath != '':
                 saveAttachment(attachmentFile= files['cv'],oldAttachPath='' , newAttachPath=cvPath )

            if avatarpath != '':
                 saveAttachment(attachmentFile= files['avatar'],oldAttachPath='' , newAttachPath=avatarpath )
           
            
        except Exception as ex:
            
            if 'full_name_U' in str(ex.args[1]):
                return {'Message':"الأسم موجود بالفعل"},400
            
            elif 'email_U' in str(ex.args[1]):
                return {'Message':"البريد الألكتروني موجود بالفعل"},400
            
            elif 'phone_U' in str(ex.args[1]):
                return {'Message':"رقم الهاتف موجود بالفعل"},400
            
            else:
                return {'Message':str(ex)},400
            
        
        
        return {'Message':"تم تسجيل الطبيب بنجاح , في انتظار موافقة المسؤول"},201        



    ###############    R E G I S T E R   P A T I E N T    ################

def registerPatient(data,files):
        
        
        avatarpath = ''
        try:
            avatarpath = getAttachmentPath(file= files['avatar'],type=0)
        except Exception as e:
            print("no avatar was send:", e)





        # query = me.insertQuery(tableName='users',columnsName=['full_name','email','phone','password','user_type','government_id','profile_status'] , values=[data['full_name'],data['email'],data['phone'],data['password'],data['government_id']])
        query = me.procQuery(procName='AddNewPatient',valuesDic={
             'name' : data['name'],
             'phone' : data['phone'],
             'email' : data['email'],
             'password' : data['password'],
             'government' : data['government'],
             'city' : data['city'],
             'address':data['address'],
             'age':data['age'],
             'image':avatarpath
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
                return {'Message':"الأسم موجود بالفعل"},400
            
            elif 'email_U' in str(ex.args[1]):
                return {'Message':"البريد الألكتروني موجود بالفعل"},400
            
            elif 'phone_U' in str(ex.args[1]):
                return {'Message':"رقم الهاتف موجود بالفعل"},400
            
            else:
                return {'Message':str(ex)},400
            
        
        
        return {'Message':"تم تسجيل المريض بنجاح "},201  


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
                return {'Message':"الأسم موجود بالفعل"},400
            
            elif 'email_U' in str(ex.args[1]):
                return {'Message':"البريد الألكتروني موجود بالفعل"},400
            
            elif 'phone_U' in str(ex.args[1]):
                return {'Message':"رقم الهاتف موجود بالفعل"},400
            
            else:
                return {'Message':str(ex)},400
            
        
        
        return {'Message':"تم تسجيل الأدمن بنجاح "},201  


###############     A U T I S M   T E S T    ################
def autiTest(data):
    #  return {"result":data}
     
     return {"result":doML(inputData=data)}
# [1, 1, 1, 1, 1, 1, 1,0,0,0,28,0,0,0,0,1,0,0,0,0,0,0,1,1,1]



###############     G E T   P E N D I N G   D O C T O R    ################
def pendingDoctors(data):
     
    query = me.selectQuery(tableName='vi_Users',where="status = '"+"pending"+"'")

    try :
        db.cursor.execute(query)

        result = me.usersModel(data=db.cursor.fetchall())

        
            
    except Exception as ex:

        return {'Message':str(ex)},400
    
    return{'data':result}
            

###############     C O N F I R M   D O C T O R    ################
def confirmDoctor(docID):
     
    query = me.updateQuery(tableName='Doctors',valuesDic={'status':'1'},where='doctor_id = '+"'"+ docID + "'")
    
    try :
        db.cursor.execute(query)
        db.conn.commit()
            
    except Exception as ex:

        return {'Message':str(ex)},400
            
        
        
    return {'Message':"تم قبول الطبيب بنجاح "},201  


###############     R E J E C T   D O C T O R    ################
def rejectDoctor(docID):
     
    query = me.updateQuery(tableName='Doctors',valuesDic={'status':'0'},where='id = '+"'"+ docID + "'")
    
    try :
        db.cursor.execute(query)
        db.conn.commit()
            
    except Exception as ex:

        return {'Message':str(ex)},400
            
        
        
    return {'Message':"تم رفض الطبيب بنجاح "},201  




###############     P R O F I L E     ################
def profile(id):

        # query = "SELECT * FROM Users WHERE ID ="+id

        # query = me.selectQuery(tableName='Users' , where='id = '+ str(id))

        query = me.procQuery(procName='getUserProfile',valuesDic={
             'u_id':str(id)
        })
        
        
        # return{'sss':query}
        result = []
        
        db.cursor.execute(query)
        # result["message"] = "data retrieved succesfully"
        result = profileModel(row=db.cursor.fetchone())
        
        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !")
        else:
            
            clnicsResult = []

            if int(result[0]['user_type']) == 1:
                query2 = me.selectQuery(tableName='Clinics',columnsName=['address'],where='doctor_id = '+str(result[0]['doctor_id']))
            
                result[0].pop("doctor_id")

                db.cursor.execute(query2)

                clinic_dic = {}

                for row in db.cursor.fetchall():
                    
                    clinic_dic['address'] = row[0]

                    clnicsResult.append(clinic_dic)

            if len(clnicsResult) != 0:
                 
                 result[0]['clinics'] = clnicsResult

            # result[0].pop("user_type")
            
            return {'message':'تم إسترجاع البيانات بنجاح !','data':result[0]}
            


# def saveAttachment(file , path):

#     if path != '':
          
#         file.save(f'{path}')

def getAttachmentPath(file,type):

    fullPath = ''

    if file.filename != '':

        uniq_filename = str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')

        if type == 0:  # avatar image
            uploads_folder = "uploads/avatars"
        else:
            uploads_folder = "uploads/CVs"
            
        fullPath = os.path.join(os.path.dirname(os.path.abspath(__file__)), uploads_folder, f'{uniq_filename}_{file.filename}')
        

    return fullPath


def getOldAttachmentPath(userId):
    query = me.selectQuery(tableName='Users' , columnsName=['image'],where='id = ' +userId)

    db.cursor.execute(query)

    oldImgPath = ''

    oldImgPath = db.cursor.fetchone()[0]

    return oldImgPath

    

def saveAttachment(attachmentFile,oldAttachPath , newAttachPath):

    if oldAttachPath and oldAttachPath != '':

        os.remove(oldAttachPath)



    fullPath = ''

    fullPath = newAttachPath

    if fullPath and fullPath != '':

       attachmentFile.save(fullPath)

        

        
    



def updateUser(userId,data,imgFile):
     
    

    query = me.procQuery(procName='getUserTypeByUid',valuesDic={"userId":userId})

    db.cursor.execute(query)

    userType = db.cursor.fetchone()[0]

    
    if data is None or 'name' not in data or 'phone' not in data or 'password' not in data or 'government' not in data or 'city' not in data or 'profile_status' not in data :
        return {'message':'Missing data ! (name , phone , password , government , city , profile_status)'},400
    

    oldImgPath = getOldAttachmentPath(userId=userId)

    

    newImgPath = getAttachmentPath(file=imgFile,type=0)

    mainQuery = me.updateQuery(tableName='Users' , valuesDic={
        "name" : data['name'],
        "phone":data['phone'],
        "password":data['password'],
        "government":data['government'],
        'city' : data['city'],
        "profile_status":data['profile_status'],
        "image":newImgPath
    },where='id ='+userId)

    try:

        if(userType == 1):
            if 'specialist' not in data  :
                return {'message':'specialist required !'},400
            
            query = me.updateQuery(tableName='Doctors' , valuesDic={
                    "specialist": data['specialist']
            }, where='doctor_id = '+userId)            


            db.cursor.execute(mainQuery)
            db.conn.commit()

            db.cursor.execute(query)
            db.conn.commit()

            
            saveAttachment(attachmentFile=imgFile,oldAttachPath=oldImgPath,newAttachPath=newImgPath)
            
            return{'message':'تم تعديل بيانات الطبيب بنجاح !'},200
        
        elif(userType == 2):
            if 'address' not in data or 'age' not in data or 'patient_name' not in data  :
                return {'message':'address , age , patient_name are  required !'},400
            
            query = me.updateQuery(tableName='Patients' , valuesDic={
                    "address": data['address'],
                    "age": data['age'],
                    "patient_name": data['patient_name']
            }, where='patient_id = '+userId)

            db.cursor.execute(mainQuery)
            db.conn.commit()

            db.cursor.execute(query)
            db.conn.commit()

            saveAttachment(attachmentFile=imgFile,oldAttachPath=oldImgPath,newAttachPath=newImgPath)

            return{'message':'تم تعديل بيانات المريض بنجاح !'},200
        
        else:
            db.cursor.execute(mainQuery)
            db.conn.commit()

            saveAttachment(imgFile=imgFile,oldAttachPath=oldImgPath,newAttachPath=newImgPath)

            return{'message':'تم تعديل بيانات الأدمن !'},200
         
    
    
    except Exception as ex:
        
        if 'full_name_U' in str(ex.args[1]):
            return {'Message':"الأسم موجود بالفعل"},400
        
        elif 'email_U' in str(ex.args[1]):
            return {'Message':"البريد الألكتروني موجود بالفعل"},400
        
        elif 'phone_U' in str(ex.args[1]):
            return {'Message':"رقم الهاتف موجود بالفعل"},400
        
        else:
            return {'Message':str(ex)},400
    
    
    


    




     

    return{'message':userType}

# def addClinic(data):

        

#         query = me.insertQuery(tableName='Clinics',columnsName=['doctor_id','address'],values=[data['uid'],data['clinic_address']])
#         # return{'s':query}

#         try :
#             db.cursor.execute(query)
#             db.conn.commit()
            
#         except Exception as ex:

#             return {'Message':str(ex)},400
            
#         return {'Message':'تم إضافة عنوان عيادة جديدة بنجاح !'},201



# def addClinic(data):        

#         query = me.selectQuery(tableName='Clinics',columnsName=['address'],where='doctor_id ='+str(data['uid']))

#         try :
#             db.cursor.execute(query)
#             db.conn.commit()
            
#         except Exception as ex:

#             return {'Message':str(ex)},400
            
#         return {'Message':'تم إضافة عنوان عيادة جديدة بنجاح !'},201











def profileModel(row):

        result = []
        
        

        item_dic ={}
        # item_dic["id"] = row[0]
        item_dic["name"] = row[1]
        item_dic["email"] = row[2]
        item_dic["phone"] = row[3]
        item_dic["image"] = row[4]
        item_dic["user_type"] = row[5]

        if int(row[5]) == 1 or int(row[5]) == 2 :

            item_dic["government"] = row[6]
            item_dic["city"] = row[7]
            
            if int(row[5]) == 1:
                item_dic["profile_status"] = row[8]
                item_dic["doctor_id"] = row[9]

            elif int(row[5]) == 2:
                item_dic["address"] = row[8]
                item_dic["age"] = row[9]
                item_dic["patient_name"] = row[10]

            
            
        result.append(item_dic)

        return result


#===============================================================================================================
