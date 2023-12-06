import mysql.connector, datetime
from.User import User
from mysql.connector import Error
import website.parameters as parameters

class ConexionDB:
    
    def executeQry(qryString, Operation) :
        result = ''
        try:
            connection = mysql.connector.connect(host = parameters.hostDB, database = parameters.database, user = parameters.userDB, password = parameters.passwordDB)
            if connection.is_connected() :
                cursor = connection.cursor()
                cursor.execute(qryString)
                #print("Execute Qry" + qryString)
                if Operation == "QRY" :
                    result = cursor.fetchall()
                elif Operation == "INSERT" :
                    connection.commit()
                    result = "OK"   
        except Error as e:
            print("Error while connecting to MySQL", e)
            result = "Error while connecting to MySQL"
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close() 
            return result


class dbManager:

    @staticmethod
    def getIngredientsInformation(ingredients):
        condition = ''
        length = len(ingredients) - 1
        print('Len:')
        print(length)
        for index in range(length):
            condition += "name = '" + ingredients[index] + "'"
            if index != length - 1:
                condition += " OR "
        qry = "SELECT * FROM analyzer.ingredient WHERE " + condition
        print(qry)
        result = ConexionDB.executeQry(qry,"QRY")
        return result

    @staticmethod
    def getProductIngredients(barcode):
        qry = "SELECT i.* FROM product p JOIN analyzer.product_ingredient pi ON p.Id = pi.idProduct JOIN ingredient i ON pi.idIngredient = i.Id WHERE p.barcode = '" + barcode + "'"
        print(qry)
        result = ConexionDB.executeQry(qry,"QRY")
        return result