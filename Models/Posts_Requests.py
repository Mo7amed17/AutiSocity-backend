from flask import Blueprint , jsonify ,request
from components import myMethods as me
from flask_cors import cross_origin
from DB_Connections.DB_EndPoints_Connections import PostsDB

postsblp = Blueprint("postsblp",__name__,static_folder="static",template_folder="templates")

# ================== ADD POST [POST] =========================
@postsblp.route("",methods=['POST'])
@me.token_required
def addPost(token):
     
    # request_data = request.get_json()
    request_data = request.form
    if request_data is None or "type" not in  request_data or "content" not in  request_data :
          return jsonify({'Message':'data is missing !'}) ,400

    request_data['uid'] = str(token['uid'])

    return PostsDB.addPost(data=request_data)



# ================== Get doctors posts [GET] =========================
@postsblp.route("/doctors",methods=['GET'])
@me.token_required
def getDoctorsPosts(token):
    request_data = {}
    # request_data = request.form
    # if request_data is None or "type" not in  request_data or "content" not in  request_data or "date" not in  request_data :
    #       return jsonify({'Message':'data is missing !'}) 
    request_data['uid'] = str(token['uid'])
    return PostsDB.getDoctorsPosts(data=request_data)


# ================== Get patients posts [GET] =========================
@postsblp.route("/patients",methods=['GET'])
@me.token_required
def getPatientsPosts(token):
     
    # request_data = request.form
    request_data = {}
    # if request_data is None or "type" not in  request_data or "content" not in  request_data or "date" not in  request_data :
    #       return jsonify({'Message':'data is missing !'}) 
    request_data['uid'] = str(token['uid'])
    return PostsDB.getPatientsPosts(data=request_data)


# ================== Get User posts [GET] =========================
@postsblp.route("/user",methods=['GET'])
@me.token_required
def getUserPosts(token):
     
    # request_data = request.form
    request_data = {}
    # if request_data is None or "type" not in  request_data or "content" not in  request_data or "date" not in  request_data :
    #       return jsonify({'Message':'data is missing !'}) 
    request_data['uid'] = str(token['uid'])
    return PostsDB.getUserPosts(data=request_data)


# ================== make a comment to a post [POST] =========================
@postsblp.route("/comment",methods=['POST'])
@me.token_required
def addComment(token):
     
    request_data = request.form
    if request_data is None or "post_id" not in  request_data or "content" not in  request_data :
          return jsonify({'Message':'data is missing !'}) ,400
    
    request_data['uid'] = str(token['uid'])
    return PostsDB.addComment(data=request_data)


# ================== get a post comments [GET] =========================
@postsblp.route("/comment",methods=['GET'])
@me.token_required
def getPostComments(token):
     
    request_data = request.form
    if request_data is None or "post_id" not in  request_data :
          return jsonify({'Message':'data is missing !'}) ,400
    
    request_data['uid'] = str(token['uid'])
    return PostsDB.getPostComments(data=request_data)


# ==================  save a post [POST] =========================
@postsblp.route("/savePost",methods=['POST'])
@me.token_required
def savePost(token):
     
    request_data = request.form
    if request_data is None or "post_id" not in  request_data :
          return jsonify({'Message':'post_id is missing !'}) ,400
    
    request_data['uid'] = str(token['uid'])
    return PostsDB.savePost(data=request_data)


# ==================  delete a post [DELETE] =========================
@postsblp.route("",methods=['DELETE'])
@me.token_required
def deletePost(token):
     
    request_data = request.form
    if request_data is None or "post_id" not in  request_data :
          return jsonify({'Message':'post_id is missing !'}) ,400
    
    request_data['uid'] = str(token['uid'])
    return PostsDB.deletePost(data=request_data)

@postsblp.route("/comments",methods=['DELETE'])
@me.token_required
def deleteComment(token):
     
    request_data = request.form
    if request_data is None or "comment_id" not in  request_data :
          return jsonify({'Message':'comment_id is missing !'}) ,400
    
    request_data['uid'] = str(token['uid'])
    return PostsDB.deleteComment(data=request_data)