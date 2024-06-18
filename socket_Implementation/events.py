from .extentions import socketio


from flask import request
from DB_Connections.DB_EndPoints_Connections import UsersDB



users = {}

@socketio.on("connect")
def handle_connect():
    print("Client connected!")

@socketio.on("addUserToSocket")
def addUserToSocket(uId):

    print("addUserToSocket => " + str(uId))

    users[uId] = socketio

@socketio.on("sendMessage")
def handle_sendMessage(data):
    returnValue = UsersDB.addMessage(
        data={'uid':data['myID'],'receiver_id':data['receiverID'],'message':data['message']}   
    )

    if returnValue['message'] == False:
        socketio.emit('response', {'status':False})
    else:
        if data['receiverID'] in users:

            users[data['receiverID']].emit(
                'response',
                {'status':True,'message':data['message'],'isMyMessage':False},
                to=data['receiverID'])

        socketio.emit('response', {'status':True,'message':data['message'],'isMyMessage':True})
    




# @socketio.on("user_join")
# def handle_user_join(username):
#     print(f"User {username} joined!")
#     users[username] = request.sid

# @socketio.on("new_message")
# def handle_new_message(message):
#     print(f"New message: {message}")
#     username = None 
#     for user in users:
#         if users[user] == request.sid:
#             username = user
#     emit("chat", {"message": message, "username": username}, broadcast=True)