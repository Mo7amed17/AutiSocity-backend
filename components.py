from flask import request , jsonify
import jwt
from functools import wraps
# from main import app

class myMethods :

    tableName = ""

    def message( message , data={}):
        return jsonify({'Message' : message,
                'Data' : data})
    



    # DATABASE QUERIES HELPER 

    def selectQuery(tableName , columnsName = ['*'] ,where = ''):
        columns = ""

        for item in columnsName:
            
            columns += item + ','


        columns = columns[:-1]
        return "SELECT "+columns+" FROM "+ tableName + ('' if (where == '') else (' Where ' + where))

    def insertQuery(tableName ,values, columnsName = ['']):
        columns = ""

        for item in columnsName:
            columns += item + ','


        getValuesQuery = ""

        for item in values:
            
            item = "'"+item+"'"
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
            
            query += '@'+ str(key) + '=' + "'"+value+"'" + ','

        
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

            
            
            result.append(item_dic)

        return result