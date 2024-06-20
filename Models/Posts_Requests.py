from flask import Blueprint , jsonify ,request
from components import myMethods as me
from flask_cors import cross_origin
from DB_Connections.DB_EndPoints_Connections import PostsDB

postsblp = Blueprint("postsblp",__name__,static_folder="static",template_folder="templates")

# ================== ADD POST [POST] =========================
@postsblp.route("",methods=['POST'])
@me.token_required
def addPost(token):
    
    request_data = request.get_json()
    if request_data is None or "content" not in  request_data :
          return jsonify({'message':'content is missing !'}) ,400

    request_data['uid'] = token['uid'].split('.')[3]

    return PostsDB.addPost(data=request_data)



# ================== Get doctors posts [GET] =========================
@postsblp.route("/doctors",methods=['GET'])
@me.token_required
def getDoctorsPosts(token):
    request_data = {}
    # request_data = request.get_json()
    # if request_data is None or "type" not in  request_data or "content" not in  request_data or "date" not in  request_data :
    #       return jsonify({'message':'data is missing !'}) 
    request_data['uid'] = token['uid'].split('.')[3]
    return PostsDB.getDoctorsPosts(data=request_data)


# ================== Get patients posts [GET] =========================
@postsblp.route("/patients",methods=['GET'])
@me.token_required
def getPatientsPosts(token):
     
    # request_data = request.get_json()
    request_data = {}
    # if request_data is None or "type" not in  request_data or "content" not in  request_data or "date" not in  request_data :
    #       return jsonify({'message':'data is missing !'}) 
    request_data['uid'] = token['uid'].split('.')[3]
    return PostsDB.getPatientsPosts(data=request_data)


# ================== Get User posts [GET] =========================
@postsblp.route("/user",methods=['GET'])
@me.token_required
def getUserPosts(token):
     
    # request_data = request.get_json()
    request_data = {}
    # if request_data is None or "type" not in  request_data or "content" not in  request_data or "date" not in  request_data :
    #       return jsonify({'message':'data is missing !'}) 
    request_data['uid'] = token['uid'].split('.')[3]
    return PostsDB.getUserPosts(data=request_data)


# ================== make a comment to a post [POST] =========================
@postsblp.route("/comment",methods=['POST'])
@me.token_required
def addComment(token):
     
    request_data = request.get_json()
    if request_data is None or "post_id" not in  request_data or "content" not in  request_data :
          return jsonify({'message':'post_id,content are missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]
    return PostsDB.addComment(data=request_data)


# ================== get a post comments [GET] =========================
@postsblp.route("/comment",methods=['PUT'])
@me.token_required
def getPostComments(token):
     
    request_data = request.get_json()
    if request_data is None or "post_id" not in  request_data :
          return jsonify({'message':'post_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]
    return PostsDB.getPostComments(data=request_data)

# ================== get a post comments [GET] =========================
@postsblp.route("/onepost",methods=['PUT'])
@me.token_required
def getOnepost(token):
     
    request_data = request.get_json()
    if request_data is None or "post_id" not in  request_data :
          return jsonify({'message':'post_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]

    return PostsDB.getOnePost(data=request_data)


# ==================  save a post [POST] =========================
@postsblp.route("/savePost",methods=['POST'])
@me.token_required
def savePost(token):
     
    request_data = request.get_json()
    if request_data is None or "post_id" not in  request_data :
          return jsonify({'message':'post_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]
    return PostsDB.savePost(data=request_data)

# ==================  unSave a post [POST] =========================
# @postsblp.route("/unsavePost",methods=['POST'])
# @me.token_required
# def unsavePost(token):
     
#     request_data = request.get_json()
#     if request_data is None or "post_id" not in  request_data :
#           return jsonify({'message':'post_id is missing !'}) ,400
    
#     request_data['uid'] = token['uid'].split('.')[3]
#     return PostsDB.unsavePost(data=request_data)

# ==================  GET SAVED posts [GET] =========================
@postsblp.route("/savedPosts",methods=['GET'])
@me.token_required
def getSavedPosts(token):
    
    return PostsDB.getSavedPosts(uid=token['uid'].split('.')[3])

# ==================  delete a post [DELETE] =========================
@postsblp.route("",methods=['DELETE'])
@me.token_required
def deletePost(token):
     
    request_data = request.get_json()
    if request_data is None or "post_id" not in  request_data :
          return jsonify({'message':'post_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]
    return PostsDB.deletePost(data=request_data)

@postsblp.route("/comment",methods=['DELETE'])
@me.token_required
def deleteComment(token):

    # check if it is my cooment to delete
     
    request_data = request.get_json()
    if request_data is None or "comment_id" not in  request_data :
          return jsonify({'message':'comment_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]
    
    return PostsDB.deleteComment(data=request_data)

@postsblp.route("/report",methods=['POST'])
@me.token_required
def reportPost(token):
     
    request_data = request.get_json()
    if request_data is None or "post_id" not in  request_data  or "user_id" not in  request_data   or "complaint" not in  request_data :
          return jsonify({'message':'post_id ,user_id , complaint  are missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]
    
    return PostsDB.reportPost(data=request_data)


@postsblp.route("/report",methods=['GET'])
@me.token_required
def getReportedPosts(token):
        
    return PostsDB.getReportedPosts(uid=token['uid'].split('.')[3])

@postsblp.route("/report/approve",methods=['POST'])
@me.token_required
def approveReportPost(token):
        
    request_data = request.get_json()

    if request_data is None or "report_id" not in  request_data:
        return jsonify({'message':'report_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]


    return PostsDB.approveReportPost(data = request_data)

@postsblp.route("/report",methods=['DELETE'])
@me.token_required
def deleteReportPost(token):
        
    request_data = request.get_json()

    if request_data is None or "report_id" not in  request_data:
        return jsonify({'message':'report_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]


    return PostsDB.deleteReportPost(data = request_data)

@postsblp.route("/like",methods=['POST'])
@me.token_required
def likePost(token):
        
    request_data = request.get_json()

    if request_data is None or "post_id" not in  request_data:
        return jsonify({'message':'post_id is missing !'}) ,400
    
    request_data['uid'] = token['uid'].split('.')[3]


    return PostsDB.likePost(data = request_data)

# @postsblp.route("/unlike",methods=['POST'])
# @me.token_required
# def unlikePost(token):
        
#     request_data = request.get_json()

#     if request_data is None or "post_id" not in  request_data:
#         return jsonify({'message':'post_id is missing !'}) ,400
    
#     request_data['uid'] = token['uid'].split('.')[3]


#     return PostsDB.unlikePost(data = request_data)