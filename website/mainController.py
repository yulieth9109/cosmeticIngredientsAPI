from flask import request, jsonify, Response, url_for, render_template, json
from .dbManager import dbManager
from .utilities import requestChatGPT, generate_confirmation_token, confirm_token, send_email
from werkzeug.security import generate_password_hash, check_password_hash
import website.parameters as parameters

urlS = "https://pristine-dahlia-377509.ey.r.appspot.com/"

class mainController:
    
    @staticmethod
    def getIngredientsAnalysis(request):
        try:
            text = request.data.decode('utf-8')
            ingredients = str(requestChatGPT(text))
            print('chat GPT' + ingredients)
            listIngredients = ingredients.split('++')
            print(listIngredients)
            if len(listIngredients) == 0:
                listIngredients = ingredients.split('•')
            if ingredients != 'VACIO' and len(listIngredients) > 0:
                dbIngredients = dbManager.getIngredientsInformation(listIngredients)
                data = Additional.getIngredientsInformation(dbIngredients, 1)
                print(str(data))
                return data
            else:
                return Response('VACIO', status=500)
        except Exception as e:
            print(e)
            return Response("Error", status=500)
    
    @staticmethod
    def getBarcode(request):
        try:
            barcode = request.data.decode('utf-8')
            dbIngredients = dbManager.getProductIngredients(barcode)
            data = Additional.getIngredientsInformation(dbIngredients, 2)
            return data
        except Exception as e:
            print(e)
            return Response("El código de barras no se encuentra registrado", status=400)

    @staticmethod
    def getInfoById(request):
        try:
            id = request.data.decode('utf-8')
            print(id)
            dbIngredients = dbManager.getProductId(id)
            data = Additional.getIngredientsInformation(dbIngredients, 2)
            return data
        except Exception as e:
            print(e)
            return Response("El id del producto no existe", status=400)

    @staticmethod
    def searchProducts(request):
        try:
            keyword = request.data.decode('utf-8')
            keyword = keyword[1:-1]
            dbProducts = dbManager.searchKeyword(keyword)
            data = Additional.getProductsList(dbProducts)
            return data
        except Exception as e:
            print(e)
            return Response("No se encontraron resultados", status=400)

    @staticmethod
    def createProduct(request):
        try:
            bodyData = request.json
            print(request.json)
            name = bodyData['name']
            description = bodyData['description']
            barcode = bodyData['barcode']
            idProduct = dbManager.createProduct(name, description, barcode)
            if isinstance(idProduct, int) and idProduct > 0:
                print(idProduct)
                ingredient_ids = bodyData['ingredients']
                data = [(idProduct, idIngredient) for idIngredient in ingredient_ids]
                print(data)
                result = dbManager.associateIngredient(data)
                print(result)
                if isinstance(result, int) and result > 0:
                    return Response(str(idProduct), status=200)
                else:
                    return Response(str(0), status=400)
            else:
                print(idProduct)
                return Response(str(0), status=400)
        except Exception as e:
            print(e)
            return Response("Eror en servidor", status=400)       

    @staticmethod
    def createUser(request):
        try:
            bodyData = request.json
            print(request.json)
            name = bodyData['name']
            email = bodyData['email']
            password = bodyData['password']
            user = dbManager.checkUserE(email.lower())
            if user :
                return Response("El usuario ya existe en el sistema", status=400)
            else: 
                idUser = dbManager.createUser(name, email, generate_password_hash(password, method='sha256'))
                if isinstance(idUser, int) and idUser > 0:
                    token = generate_confirmation_token(email.lower())
                    confirm_url = url_for('routes.confirm_email', token=token, _external=True)
                    html = render_template('activate.html', confirm_url=confirm_url, urlS = str(urlS))
                    subject = "SKIN Confirmar email"
                    send_email(email, subject, html)
                    return Response(str(idUser), status=200)
                else:
                    print(idUser)
                    return Response("Registro de usuario fallida, intente de nuevo", status=400)
        except Exception as e:
            print(e)
            return Response("Error interno en el servidor", status=400)

    @staticmethod
    def confirmEmail(token):
        global urlS
        try:
            emailU = confirm_token(token, 3600)
            if emailU != False :
                result = dbManager.activateAccount(emailU.lower())
                if result == "OK":
                    return render_template('message.html', message = "Cuenta verificada", urlS = str(urlS))
                else:
                    return render_template('message.html', message="Error en verificación intenten más tarde", urlS=str(urlS))
            else:
                return render_template('message.html', message="The confirmation link is invalid.", urlS = str(urlS))
        except:
            return render_template('message.html', message="The confirmation link is invalid or has expired.", urlS = str(urlS))

    @staticmethod
    def loginUser(request):
        bodyData = request.json
        user = dbManager.getUserInfo(bodyData['email'])
        if user:
            print(str(user.password))
            if check_password_hash(user.password, str(bodyData['password'])) :
                content = {"id": str(user.id), "name": str(user.name), "email": str(user.email), "status": user.status}
                print(content)
                return jsonify(content)
            else:
                return Response("Contraseña Incorrecta", status = 400)
        else:
            return Response("El usuario no existe", status = 400)

class Additional:

    @staticmethod
    def retrieveData(result) :
        if result is not None:
            return list(result)[0]
        else:
            return ''

    @staticmethod
    def getProductsList(products):
        if products:
            products_json = []
            for result in products:
                content = {"idProduct": result[0], "name": result[1], "description" : result[3]}
                products_json.append(content)
                print(products_json)
            return jsonify(products_json)
        else:
            return Response("No information found", status=404)

    @staticmethod
    def getIngredientsInformation(ingredients, option):
        if ingredients:
            summary_json = []
            ingredients_json = []
            parabenFree = True
            sulfateFree = True
            alcoholFree = True
            siliconeFree = True
            euAllergenFree = True
            fungalAcne = True
            acneFighting = []
            brightening = []
            uvProtection = []
            woundHealing = []
            antiAging = []
            goodDrySkin = 0
            badDrySkin = 0
            goodOilSkin = 0
            badOilSkin = 0
            goodSensitiveSkin = 0
            badSensitiveSkin = 0
            for result in ingredients:
                if option == 2:
                    idProduct = result[15]
                    productName = result[16]
                    barcode = result[17]
                    descriptionP = result[18]
                if bool(result[8]) == True:
                    parabenFree = not bool(result[8])
                elif bool(result[9]) == True:
                    sulfateFree = not bool(result[9])
                elif bool(result[10]) == True:
                    alcoholFree = not bool(result[10])
                elif bool(result[11]) == True:
                    siliconeFree = not bool(result[11])
                elif bool(result[12]) == True:
                    euAllergenFree = not bool(result[12])
                elif bool(result[13]) == True:
                    fungalAcne = not bool(result[13])
                if result[4] is not None and list(result[4])[0] == 'GOOD':
                    goodDrySkin += 1
                if result[4] is not None and list(result[4])[0] == 'BAD':
                    badDrySkin += 1
                if result[5] is not None and list(result[4])[0] == 'GOOD':
                    goodOilSkin += 1
                if result[5] is not None and list(result[4])[0] == 'BAD':
                    badOilSkin += 1
                if result[6] is not None and list(result[4])[0] == 'GOOD':
                    goodSensitiveSkin += 1
                if result[6] is not None and list(result[4])[0] == 'BAD':
                    badSensitiveSkin += 1
                notableEffects = result[7]
                if isinstance(notableEffects, set) and (result[7] != 'None'):
                    notableEffectsJ = list(notableEffects)
                    for effect in notableEffects:
                        if effect == 'ACNE_FIGHTING':
                            acneFighting.append(result[0].capitalize())
                        elif effect == 'BRIGHTENING':
                            brightening.append(result[0].capitalize())
                        elif effect == 'UV_PROTECTION':
                            uvProtection.append(result[0].capitalize())
                        elif effect == 'WOUND_HEALING':
                            woundHealing.append(result[0].capitalize())
                        elif effect == 'ANTI_AGING':
                            antiAging.append(result[0].capitalize())
                else:
                    notableEffectsJ = []
                drySkin = Additional.retrieveData(result[4])
                oilSkin = Additional.retrieveData(result[5])
                sensitiveSkin = Additional.retrieveData(result[6])
                description = str(result[0]).capitalize() + ' (' + str(result[1]).capitalize() + ')'
                content = {"idIngredient": result[14], "EWG": result[3], "CIR" : result[2], "name": description, "drySkin": drySkin, "oilSkin": oilSkin, "sensitiveSkin": sensitiveSkin, "notableEffects": notableEffectsJ, "isParaben" : bool(result[8]), "isSulfate" : bool(result[9]), "isAlcohol" : bool(result[10]), "isSilicone" : bool(result[11]), "isEUAllergen" : bool(result[12]), "isFungalAcneSafe" : bool(result[13])}
                ingredients_json.append(content)
            if option == 1:
                summary_json = {"idProduct": 0 ,"parabenFree": parabenFree, "sulfateFree": sulfateFree, "alcoholFree": alcoholFree, "siliconeFree": siliconeFree, "euAllergenFree": euAllergenFree, "fungalAcne": fungalAcne, "acneFighting": acneFighting, "brightening": brightening, "uvProtection": uvProtection, "woundHealing": woundHealing, "antiAging": antiAging, "goodDrySkin": goodDrySkin, "badDrySkin": badDrySkin, "goodOilSkin": goodOilSkin, "badOilSkin": badOilSkin, "goodSensitiveSkin": goodSensitiveSkin, "badSensitiveSkin": badSensitiveSkin, "ingredients": ingredients_json}
            if option == 2:
                summary_json = {"idProduct": idProduct, "productName": productName, "barcode": barcode, "description": descriptionP, "parabenFree": parabenFree, "sulfateFree": sulfateFree, "alcoholFree": alcoholFree, "siliconeFree": siliconeFree, "euAllergenFree": euAllergenFree, "fungalAcne": fungalAcne, "acneFighting": acneFighting, "brightening": brightening, "uvProtection": uvProtection, "woundHealing": woundHealing, "antiAging": antiAging, "goodDrySkin": goodDrySkin, "badDrySkin": badDrySkin, "goodOilSkin": goodOilSkin, "badOilSkin": badOilSkin, "goodSensitiveSkin": goodSensitiveSkin, "badSensitiveSkin": badSensitiveSkin, "ingredients": ingredients_json}
            #print(summary_json)
            return jsonify(summary_json)
        else:
            return Response("No information found", status=404)
    
