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

    users[uId] = request.sid

@socketio.on("sendMessage")
def handle_sendMessage(data):
    print('users')
    print(users)
    
    returnValue = UsersDB.addMessage(
        data={'uid':data['myID'],'receiver_id':data['receiverID'],'message':data['message']}   
    )

    if returnValue['message'] == False:
        print('error message')
        
        socketio.emit('response', {'status':False})

    else:
        if data['receiverID'] in users:
            print('send to receiverID')

            if 'messengerData' in data :
                data['messengerData']['uId'] = data['myID']
                print(data)


                socketio.emit(
                    'response',
                    {'status':True,'message':data['message'],'isMyMessage':False,'messengerData':data['messengerData']},to=users[data['receiverID']])
            else:

                socketio.emit(
                'response',
                {'status':True,'message':data['message'],'isMyMessage':False},to=users[data['receiverID']])
                
        print('send to Meee')
        print(users[data['myID']])
        if 'messengerData' in data :
            socketio.emit('response', {'status':True,'message':data['message'],'isMyMessage':True,'messengerData':data['messengerData']},to=request.sid)
        else:
            socketio.emit('response', {'status':True,'message':data['message'],'isMyMessage':True},to=request.sid)
    




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