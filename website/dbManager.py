import mysql.connector, datetime
from mysql.connector import Error
import website.parameters as parameters

class ConexionDB:
    
    def executeQry(qryString, Operation, data) :
        result = ''
        try:
            connection = mysql.connector.connect(host = parameters.hostDB, database = parameters.database, user = parameters.userDB, password = parameters.passwordDB)
            if connection.is_connected() :
                cursor = connection.cursor()
                #print("Execute Qry" + qryString)
                if Operation == "MULTI-INSERT":
                    cursor.executemany(qryString, data)
                    connection.commit()
                    result = cursor.rowcount
                if Operation == "QRY":
                    cursor.execute(qryString)
                    result = cursor.fetchall()
                elif Operation == "INSERT":
                    cursor.execute(qryString)
                    connection.commit()
                    inserted_id = cursor.lastrowid
                    result = inserted_id
                elif Operation == "UPDATE":
                    cursor.execute(qryString)
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
            finalIngredient = ingredients[index].lstrip()
            finalIngredient = finalIngredient.rstrip()
            condition += "name = '" + ingredients[index].lstrip() + "'"
            if index != length - 1:
                condition += " OR "
        qry = "SELECT * FROM analyzer.ingredient WHERE " + condition
        print(qry)
        result = ConexionDB.executeQry(qry,"QRY", "")
        return result

    @staticmethod
    def getProductIngredients(barcode):
        qry = "SELECT i.*, p.* FROM product p JOIN analyzer.product_ingredient pi ON p.Id = pi.idProduct JOIN ingredient i ON pi.idIngredient = i.Id WHERE p.barcode = " + barcode
        print(qry)
        result = ConexionDB.executeQry(qry,"QRY", "")
        return result


    @staticmethod
    def createProduct(name, description, barcode):
        name = dbManager.formatString(name)
        description = description.lstrip()
        description = description.rstrip()
        qry = "INSERT INTO analyzer.product (`name`, `description`,`barcode`) VALUES('" + name + "', '" + description + "', '" + barcode + "')"
        print(qry)
        result = ConexionDB.executeQry(qry,"INSERT", "")
        return result

    @staticmethod
    def associateIngredient(data):
        qry = "INSERT INTO analyzer.product_ingredient (`idProduct`, `idingredient`) VALUES (%s, %s)"
        print(qry)
        result = ConexionDB.executeQry(qry,"MULTI-INSERT", data)
        return result

    @staticmethod
    def formatString(input_string):
        input_string = input_string.lstrip()
        input_string = input_string.rstrip()
        words = input_string.split()
        formatted_words = [word.capitalize() if len(word) > 2 else word for word in words]
        formatted_string = ' '.join(formatted_words)
        return formatted_string

    @staticmethod
    def createUser(name, email, password):
        name = dbManager.formatString(name)
        email = email.lower()
        qry = "INSERT INTO analyzer.user (email, name, password, status) VALUES('" + email + "', '" + name + "', '" + password + "', 'No Verificado')"
        print(qry)
        result = ConexionDB.executeQry(qry,"INSERT", "")
        return result

    @staticmethod
    def checkUserE(email):
        qry = "SELECT * FROM analyzer.user WHERE email ='" + email + "'"
        result = ConexionDB.executeQry(qry, "QRY", "")
        return result

    @staticmethod
    def activateAccount(email) :
        qry = "UPDATE analyzer.user SET status = 'Verificado' WHERE email = '" + email + "';"
        result = ConexionDB.executeQry(qry, "UPDATE", "")
        return result

    @staticmethod
    def getUserInfo(email) :
        qry = "SELECT name, email, status, password, id FROM analyzer.user WHERE email = '" + email.lower() + "'"
        result = ConexionDB.executeQry(qry, "QRY", "")
        if result:
            user = User(result[0][0], result[0][1], result[0][2], result[0][3], result[0][4])
            return user
        else:
            return None

    @staticmethod
    def getProductId(id):
        qry = "SELECT i.*, p.* FROM product p JOIN analyzer.product_ingredient pi ON p.Id = pi.idProduct JOIN ingredient i ON pi.idIngredient = i.Id WHERE p.Id = " + id
        print(qry)
        result = ConexionDB.executeQry(qry,"QRY", "")
        return result

    @staticmethod
    def searchKeyword(keyword):
        sanitized_keyword = keyword.replace("%", r"\%").replace("_", r"\_")
        qry = "SELECT * FROM analyzer.product WHERE name LIKE '%" + sanitized_keyword + "%'"
        print(qry)
        result = ConexionDB.executeQry(qry, "QRY", "")
        return result

    @staticmethod
    def createReview(title, description, rate, author, product):
        creation_date = str(datetime.datetime.now().date())
        qry = f"INSERT INTO review (title, description, rate, author, product, creationDate) VALUES ('{title}', '{description}', {rate}, {author}, {product}, '{creation_date}')"
        print('qry' + qry)
        result = ConexionDB.executeQry(qry,"INSERT", "")
        return result

    @staticmethod
    def getReviews(idProduct):
        qry = """
            SELECT r.id AS id, r.title, r.description, r.rate, r.creationDate, u.name AS authorName
            FROM analyzer.review AS r
            JOIN analyzer.user AS u ON r.author = u.id
            WHERE r.product = """ + idProduct + " ORDER BY creationDate DESC;"
        result = ConexionDB.executeQry(qry, "QRY", "")
        return result

    @staticmethod
    def getUserReviews(userId):
        qry = """
            SELECT r.id AS id, r.title, r.description, r.rate, r.creationDate, p.name AS productName
            FROM analyzer.review AS r
            JOIN analyzer.product AS p ON r.product = p.Id
            WHERE r.author = """ + userId + " ORDER BY creationDate DESC;"
        print(qry)
        result = ConexionDB.executeQry(qry, "QRY", "")
        return result

    @staticmethod
    def deleteReview(idReview):
        qry = f"DELETE FROM analyzer.review WHERE id = {idReview}"
        print(qry)
        result = ConexionDB.executeQry(qry, "UPDATE", "")
        return result



class User ():
  def __init__(self, name, email, status, password, id):
    self.name = name
    self.email = email
    self.status = status
    self.password = password
    self.id = id