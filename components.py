from flask import request , jsonify
import jwt
from functools import wraps
from DB_Connections.DB_connections import linkDB as db



class myMethods :

    tableName = ""

    def message( message , data={}):
        return jsonify({'Message' : message,
                'Data' : data})
    



    # DATABASE QUERIES HELPER 

    def selectQuery(tableName , columnsName = ['*'] ,where = '',orderby = ''):
        columns = ""

        for item in columnsName:
            
            columns += item + ','


        columns = columns[:-1]
        return "SELECT "+columns+" FROM "+ tableName + ('' if (where == '') else (' Where ' + where)) + ('' if (orderby == '') else (' ORDER BY ' + orderby.split(',')[0] + ' ' + orderby.split(',')[1]))


    def insertQuery(tableName ,values, columnsName = ['']):
        columns = ""

        for item in columnsName:
            columns += item + ','


        getValuesQuery = ""

        for item in values:
            
            item = "'"+str(item)+"'"
            getValuesQuery += item + ','


        columns = columns[:-1]
        getValuesQuery = getValuesQuery[:-1]
        return "INSERT INTO "+tableName+" ("+columns+")"+" VALUES ("+ getValuesQuery+")"



    def updateQuery(tableName ,valuesDic , where = ''):
        query = ""

        for key , value in valuesDic.items():
            
            query += str(key) + '=' + "'"+value+"'" + ','

        
        query = query[:-1]
        return "UPDATE "+tableName+" SET "+query + ('' if (where == '') else (' Where ' + where))
    




    
    def deleteQuery(tableName,where = ''):

        return "DELETE FROM "+tableName + ('' if (where == '') else (' Where ' + where))


    def procQuery(procName ,valuesDic ):
        query = ""

        for key , value in valuesDic.items():
            
            query += '@'+ str(key) + '=' + "'"+str(value)+"'" + ','

        
        query = query[:-1]
        return "EXEC "+procName+' '+query

    
    # END
    
    




    def token_required(f):
        @wraps(f)
        def decorated(*args,**kwargs):

            Hdata = None

            if 'Authorization' in request.headers:

                Hdata = request.headers['Authorization']
        

            if not Hdata:
                return jsonify({"message":'Token Is Missing!'}),400

            try:
                token = jwt.decode(Hdata,"654321",algorithms=["HS256"])
                
                if len(token['uid'].split('.')) != 5:
                    
                    return jsonify({"Message":'Token Is Invalid'}),400
                
            except:            
                return jsonify({"Message":'Token Is Invalid'}),400
        
            return f(token,*args,**kwargs)
        
        return decorated



    def usersModel(data):

        result = []
        
        for row in data:

            item_dic ={}
            item_dic["id"] = row[0]
            item_dic["name"] = row[1]
            item_dic["email"] = row[2]
            item_dic["user_type"] = row[4]
            item_dic["status"] = row[5]
            item_dic["image"] = row[6] if  len(str(row[6])) > 0  else None

            if item_dic["user_type"] == 'doctor':
                item_dic["cv"] = row[7]
                item_dic["create_at"] = row[8]


            
            
            result.append(item_dic)

        return result
    
    def getUserTypeByUserID(uid):

        query = myMethods.procQuery(procName='getUserTypeByUid',valuesDic={"userId":uid})

        try:
            db.cursor.execute(query)

            userType = db.cursor.fetchone()[0]

            return userType
        except :
            return{'message':'id not found !'},400