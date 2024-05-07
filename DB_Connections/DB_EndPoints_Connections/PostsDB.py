from DB_Connections.DB_connections import linkDB as db
from flask import jsonify
from components import myMethods as me
import jwt
import datetime



# ================== Add Post [POST] =========================

def addPost(data):

    type = ''

    userType = me.getUserTypeByUserID(uid=data['uid'])

    if userType == 2:
        type = '0'
    else:
        if 'type' not in data:
            return{'message':'type is required with doctor\'s posts'}

        if data['type'] == 'question':
            type = '1'

        elif data['type'] == 'advice':
            type = '2'

        elif data['type'] == 'information':
            type = '3'
        else:
            return{'message':'choose between question , advice and information type'},400
     
    query = me.insertQuery(tableName='Posts',columnsName=['user_id','type','[content]','date'],values=[data['uid'],type,data['content'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])
    
    try :
        db.cursor.execute(query)
        db.conn.commit()
            
    except Exception as ex:

        return {'message':str(ex)},400
            
        
        
    return {'message':"تم إضافة منشور بنجاح "},201 

# ================== Get Doctors Posts [GET] =========================

def getDoctorsPosts(data):
     
    # query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'doctor'+"'")

    query = me.procQuery(procName='getAllPosts' , valuesDic={
        'user_id' : data['uid'],
        'posts_type' : '1'
    })

    # return{'s':query}
    
    try :
        db.cursor.execute(query)


        result = postModel(data=db.cursor.fetchall())

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !"),200
        
        else:

            return {'data':result},200
            
    except Exception as ex:

        return {'message':str(ex)},400
            

# ================== Get Patients Posts [GET] =========================

def getPatientsPosts(data):
     
    # query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'patient'+"'")

    query = me.procQuery(procName='getAllPosts' , valuesDic={
        'user_id' : data['uid'],
        'posts_type' : '0'
    })

    
    
    try :
        db.cursor.execute(query)


        result = postModel(data=db.cursor.fetchall())

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !"),200
        
        else:

            return {'data':result},200
            
    except Exception as ex:

        return {'message':str(ex)},400
    

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

#         return {'message':str(ex)},400



# ================== add comment to a post [POST] =========================

def addComment(data):
     
    #query = me.selectQuery(tableName='vi_posts',where='user_type = '+"'"+'patient'+"'")

    query = me.insertQuery(tableName='Comments',columnsName=['user_id','post_id','content','date'],values=[data['uid'],data['post_id'],data['content'],datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')])

    # return{'s':query}
    
    try :
        db.cursor.execute(query)
        db.conn.commit()

        
            
    except Exception as ex:

        return {'message':str(ex)},400

    return {'message':'تم إضافة تعليق بنجاح'},201



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

        return {'message':str(ex)},400

    return {'data':result},201



# ==================  save post [POST] =========================
def savePost(data):

    query = me.insertQuery(tableName='Saved_Posts',columnsName=['user_id','post_id'],values=[data['uid'],data['post_id']])
    
    try :
        db.cursor.execute(query)
        db.conn.commit()

        
            
    except Exception as ex:
        
        if 'U_SavedPost' in str(ex.args[1]):
            return {'message':'تم حفظ هذا المنشور من قبل !'},400

        return {'message':'No post found with this id !'},400
        return {'message':str(ex)},400

    return {'message':'تم حفظ المنشور بنجاح'},200
        
# ==================  unsave post [POST] =========================
def unsavePost(data):

    query = me.selectQuery(tableName='Saved_Posts',where='post_id = '+str(data['post_id']) + ' AND user_id = '+str(data['uid']))
    db.cursor.execute(query)
    result=db.cursor.fetchall()

    if(len(result) == 0):
        return{'message':'cannot unsave a post that you did not saved it before !'},400


    
    query = me.deleteQuery(tableName='Saved_Posts',where='post_id = '+str(data['post_id']) + ' AND user_id = '+str(data['uid']))
    try :
        db.cursor.execute(query)
        db.conn.commit()
        return{'message':'تم إزالة المنشور من المحفوظات بنجاح !'},200

        
            
    except Exception as ex:
        
        if 'U_SavedPost' in str(ex.args[1]):
            return {'message':'تم حفظ هذا المنشور من قبل !'},400

        return {'message':'No post found with this id !'},400
        return {'message':str(ex)},400

    return {'message':'تم حفظ المنشور بنجاح'},200


def getSavedPosts(uid):

    query = me.procQuery(procName='getAllSavedPosts' , valuesDic={
    'user_id' : uid,
    })

    # return{'s':query}
    
    try :
        db.cursor.execute(query)


        result = postModel(data=db.cursor.fetchall())

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !"),200
        
        else:

            return {'data':result},200
            
    except Exception as ex:

        return {'message':str(ex)},400



# ==================  delete post [DELETE] =========================

def deletePost(data):

    ## check if admin or user post

    userType = me.getUserTypeByUserID(uid=data['uid'])
    
    if userType != 0:
        query = me.selectQuery(tableName='Posts',where='id = '+str(data['post_id']) + ' AND user_id = '+str(data['uid']))

        db.cursor.execute(query)
        result=db.cursor.fetchall()
        if len(result) == 0 :
            return{'message':'لا يمكن حذف المنشور لعدم وجودة او لعدم وجود صلاحية بذلك'},400

    # return{'ss':query}



    query = me.deleteQuery(tableName='Posts',where='id = '+str(data['post_id']))
    # return{'s':query}
    try :
        db.cursor.execute(query)
        db.conn.commit()

        return {'message':'تم حذف المنشور بنجاح'},200
            
    except Exception as ex:

        return {'message':str(ex)},400

    



# ==================  delete comment [POST] =========================
def deleteComment(data):
    # check if it is my cooment to delete
    query = me.selectQuery(tableName='Comments',where='id = '+str(data['comment_id']) + ' AND user_id = '+str(data['uid']))

    db.cursor.execute(query)
    result=db.cursor.fetchall()

    # return{'ss':query}

    if len(result) == 0 :
        return{'message':'لا يمكن حذف التعليق لعد وجودة او لعدم وجود صلاحية بذلك'},400

    query = me.deleteQuery(tableName='Comments',where='id = '+str(data['comment_id']))

    try :
        db.cursor.execute(query)
        db.conn.commit()

        
            
    except Exception as ex:

        return {'message':str(ex)},400

    return {'message':'تم حذف التعليق بنجاح'},200



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
            
            return   me.message(message="لا يوجد بيانات !"),200
        
        else:

            return {'data':result},200
            
    except Exception as ex:

        return {'message':str(ex)},400
   
# ==================  report post [POST] =========================
def reportPost(data):

    query = me.insertQuery(tableName='Posts_Reports',columnsName=['user_id','post_id','complaint'],values=[data['uid'],data['post_id'],data['user_id']])
    
    try :
        db.cursor.execute(query)
        db.conn.commit()

        return {'message':'تم تبليغ المنشور الي المسؤولين بنجاح'},200
            
    except Exception as ex:
        if 'U_Report' in str(ex.args[1]):

            return {'message':"لقد بلغت علي هذا المنشور مسبقا !"},400
        else:

            return {'message':str(ex)},400

    

# ==================  Get reported posts [GET] =========================
def getReportedPosts(uid):

    userType = me.getUserTypeByUserID(uid=uid)

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403

    query = me.selectQuery(tableName='vi_ReportedPosts', orderby='date,DESC')
    
    try :
        db.cursor.execute(query)
        
        result = reportedPostsModel(data=db.cursor.fetchall())

        if len(result) == 0 :
            
            return   me.message(message="لا يوجد بيانات !"),200
        
        else:
            result.reverse()

            return {'data':result},200

        
            
    except Exception as ex:

        return {'message':str(ex)},400


# ==================  approve report post [POST] =========================
def approveReportPost(data):

    userType = me.getUserTypeByUserID(uid=data['uid'])

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403

    
    query = me.selectQuery(tableName='Posts_Reports',where='id = '+str(data['report_id']))
    db.cursor.execute(query)
    result=db.cursor.fetchall()

    if len(result) == 0 :

        return{'message':'تم قبول او رفض هذا المنشور بالفعل !'}
    
    query = me.deleteQuery(tableName='Posts_Reports',where='id = '+str(data['report_id']) )
    
    try :
    
        db.cursor.execute(query)
        db.conn.commit()

        return {'message':'تم السماح بالمنشور بنجاح'},200
            
    except Exception as ex:
       
        return {'message':str(ex)},400
    


# ==================  delete report post [DELETE] =========================

def deleteReportPost(data):

    userType = me.getUserTypeByUserID(uid=data['uid'])

    if userType != 0 :
        return{'message':'Permission denied ,Only admins allowed !'},403

    
    query = me.selectQuery(tableName='Posts_Reports',columnsName=['post_id'],where='id = '+str(data['report_id']))
    db.cursor.execute(query)
    result=db.cursor.fetchall()
    

    if len(result) == 0 :

        return{'message':'تم قبول او رفض هذا المنشور بالفعل !'}


    
    query = me.deleteQuery(tableName='Posts',where='id = '+str(result[0][0]) )
    
    try :
    
        db.cursor.execute(query)
        db.conn.commit()

        return {'message':'تم حذف المنشور بنجاح'},200
            
    except Exception as ex:
       
        return {'message':str(ex)},400



# ==================  like a post [POST] =========================

def likePost(data):

    
    query = me.insertQuery(tableName='Post_Likes',columnsName=['post_id','user_id'],values=[int(data['post_id']) , int(data['uid'])])
    try :
        db.cursor.execute(query)
        db.conn.commit()
        return{'message':'تم عمل لايك بنجاح !'},200
            
    except Exception as ex:
        if 'U_Like' in str(ex.args[1]):
            return {'message':'تم عمل لايك لهذا المنشور من قبل !'},400
        else:
            return {'message':str(ex)},400
    

# ==================  unlike a post [POST] =========================
def unlikePost(data):

    query = me.selectQuery(tableName='Post_Likes',where='post_id = '+str(data['post_id']) + ' AND user_id = '+str(data['uid']))
    db.cursor.execute(query)
    result=db.cursor.fetchall()

    if(len(result) == 0):
        return{'message':'cannot unlike a post that you did not liked it before !'},400


    
    query = me.deleteQuery(tableName='Post_Likes',where='post_id = '+str(data['post_id']) + ' AND user_id = '+str(data['uid']))
    try :
        db.cursor.execute(query)
        db.conn.commit()
        return{'message':'تم حذف الايك بنجاح !'},200
            
    except Exception as ex:
       
        return {'message':str(ex)},400




#################################### Models Section ###################################################



# Posts Model

def postModel(data):

        result = []
        
        for row in data:

            item_dic ={}
            item_dic["id"] = row[0]
            item_dic["content"] = row[1]
            item_dic["date"] = row[2]
            item_dic["likes"] = row[3]
            item_dic["isLiked"] = row[4]
            item_dic["comments"] = row[5]
            item_dic["saves"] = row[6]
            item_dic["isSaved"] = row[7]
            item_dic["type"] = row[8]
            item_dic["post_user_id"] = row[9]
            item_dic["name"] = row[10]
            item_dic["email"] = row[11]
            item_dic["image"] = row[12]
            
            
            
            
            result.append(item_dic)

        return result


def reportedPostsModel(data):

        result = []
        
        for row in data:

            item_dic ={}
            item_dic["id"] = row[0]
            item_dic["date"] = row[1]
            item_dic["content"] = row[2]
            item_dic["type"] = row[3]
            item_dic["comp_from"] = row[4]
            item_dic["comp_to"] = row[5]
            item_dic["image"] = row[6]
            item_dic["complaint"] = row[7]
            
            
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