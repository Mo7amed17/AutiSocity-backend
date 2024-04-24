from DB_Connections.DB_connections import LinkDatabase
from flask import jsonify
from components import myMethods as me
import jwt
import datetime

db = LinkDatabase()

# ================== Add Post [POST] =========================

def addPost(data):
     
    query = me.insertQuery(tableName='Posts',columnsName=['user_id','type','[content]','likes','date'],values=[data['uid'],data['type'],data['content'],'0',datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    
    try :
        db.cursor.execute(query)
        db.conn.commit()
            
    except Exception as ex:

        return {'Message':str(ex)},400
            
        
        
    return {'Message':"تم إضافة منشور بنجاح "},201 

# ================== Get Doctors Posts [GET] =========================

def getDoctorsPosts(data):
     
    # query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'doctor'+"'")

    query = me.procQuery(procName='getAllPosts' , valuesDic={
        'user_id' : data['uid'],
        'user_type' : '1'
    })

    # return{'s':query}
    
    try :
        db.cursor.execute(query)


        result = postModel(data=db.cursor.fetchall())

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !"),400
        
        else:

            return {'data':result},200
            
    except Exception as ex:

        return {'Message':str(ex)},400
            

# ================== Get Patients Posts [GET] =========================

def getPatientsPosts(data):
     
    # query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'patient'+"'")

    query = me.procQuery(procName='getAllPosts' , valuesDic={
        'user_id' : data['uid'],
        'user_type' : '2'
    })

    
    
    try :
        db.cursor.execute(query)


        result = postModel(data=db.cursor.fetchall())

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !"),400
        
        else:

            return {'data':result},200
            
    except Exception as ex:

        return {'Message':str(ex)},400
    

# ================== Get User Posts [GET] =========================

# def getuserPosts(data):
     
#     # query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'patient'+"'")

#     query = me.procQuery(procName='getAllPosts' , valuesDic={
#         'user_id' : data['uid'],
#         'user_type' : '2'
#     })

    
    
#     try :
#         db.cursor.execute(query)


#         result = postModel(data=db.cursor.fetchall())

#         if len(result) == 0 :
            
#             return   me.message(message="لا يوجد بيانات !"),400
        
#         else:

#             return {'data':result},200
            
#     except Exception as ex:

#         return {'Message':str(ex)},400



# ================== add comment to a post [POST] =========================

def addComment(data):
     
    #query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'patient'+"'")

    query = me.insertQuery(tableName='Comments',columnsName=['user_id','post_id','content','date'],values=[data['uid'],data['post_id'],data['content'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    # return{'s':query}
    
    try :
        db.cursor.execute(query)
        db.conn.commit()

        
            
    except Exception as ex:

        return {'Message':str(ex)},400

    return {'Message':'تم إضافة تعليق بنجاح'},201



# ==================  get a post comments [GET] =========================

def getPostComments(data):
     
    #query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'patient'+"'")

    query = me.procQuery(procName='getPostComments',valuesDic={
        'userID':data['uid'],
        'postID' : data['post_id']
    })

    # return{'s':query}
    
    try :
        db.cursor.execute(query)

        result = commentModel(db.cursor.fetchall())
        
            
    except Exception as ex:

        return {'Message':str(ex)},400

    return {'data':result},201



# ==================  save post [POST] =========================
def savePost(data):

    query = me.insertQuery(tableName='Saved_Posts',columnsName=['user_id','post_id'],values=[data['uid'],data['post_id']])
    
    try :
        db.cursor.execute(query)
        db.conn.commit()

        
            
    except Exception as ex:

        return {'Message':str(ex)},400

    return {'Message':'تم حفظ المنشور بنجاح'},201
        




# ==================  delete post [DELETE] =========================

def deletePost(data):
    
    query = me.deleteQuery(tableName='Posts',where='id = '+str(data['post_id']))
    # return{'s':query}
    try :
        db.cursor.execute(query)
        db.conn.commit()

        
            
    except Exception as ex:

        return {'Message':str(ex)},400

    return {'Message':'تم حذف المنشور بنجاح'},200



# ==================  delete comment [POST] =========================
def deleteComment(data):
    # check if it is my cooment to delete
    query = me.deleteQuery(tableName='Comments',where='id = '+str(data['comment_id']))

    try :
        db.cursor.execute(query)
        db.conn.commit()

        
            
    except Exception as ex:

        return {'Message':str(ex)},400

    return {'Message':'تم حذف التعليق بنجاح'},200



def getUserPosts(data):
    

    query  = me.procQuery(procName='getUserTypeByUid',valuesDic={"userId":data['uid']})

    db.cursor.execute(query)

    userType = db.cursor.fetchone()[0]

    

    query = me.procQuery(procName='getAllPosts' , valuesDic={
        'user_id' : data['uid'],
        'user_type' : str(userType)
    })

    try :
        db.cursor.execute(query)
        db.conn.commit()

        
        result = postModel(data=db.cursor.fetchall())

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !"),400
        
        else:

            return {'data':result},200
            
    except Exception as ex:

        return {'Message':str(ex)},400
   

# Posts Model

def postModel(data):

        result = []
        
        for row in data:

            item_dic ={}
            item_dic["id"] = row[0]
            item_dic["name"] = row[1]
            item_dic["email"] = row[2]
            item_dic["type"] = row[3]
            item_dic["content"] = row[4]
            item_dic["date"] = row[5]
            item_dic["likes"] = row[7]
            item_dic["comments"] = row[8]
            item_dic["is_saved"] = row[9]
            
            
            result.append(item_dic)

        return result


# Comment Model

def commentModel(data):

        result = []
        
        for row in data:

            item_dic ={}
            item_dic["id"] = row[0]
            item_dic["content"] = row[3]
            item_dic["date"] = row[4]
            item_dic["is_my_comment"] = row[5]
           
            
            result.append(item_dic)

        return result