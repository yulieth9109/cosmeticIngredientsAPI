from flask import request, jsonify, Response, json
from .dbManager import dbManager
from .utilities import requestChatGPT
import website.parameters as parameters


class mainController:
    
    @staticmethod
    def getIngredientsAnalysis(request):
        try:
            text = request.data.decode('utf-8')
            ingredients = str(requestChatGPT(text))
            print('chat GPT' + ingredients)
            listIngredients = ingredients.split('++')
            print(listIngredients)
            if ingredients != 'VACIO' and len(listIngredients) > 0:
                dbIngredients = dbManager.getIngredientsInformation(listIngredients)
                data = Additional.getIngredientsInformation(dbIngredients)
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
            data = Additional.getIngredientsInformation(dbIngredients)
            return data
        except Exception as e:
            print(e)
            return Response("Error", status=500)

class Additional:

    @staticmethod
    def getIngredientsInformation(ingredients):
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
                if result[4] == 'GOOD':
                    goodDrySkin += 1
                if result[4] == 'BAD':
                    badDrySkin += 1
                if result[5] == 'GOOD':
                    goodOilSkin += 1
                if result[5] == 'BAD':
                    badOilSkin += 1
                if result[6] == 'GOOD':
                    goodSensitiveSkin += 1
                if result[6] == 'BAD':
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
                description = str(result[0]).capitalize() + ' (' + str(result[1]).capitalize() + ')'
                content = {"idIngredient": result[14], "EWG": result[3], "CIR" : result[2], "name": description, "drySkin": result[4], "oilSkin": result[5], "sensitiveSkin": result[6], "notableEffects": notableEffectsJ, "isParaben" : bool(result[8]), "isSulfate" : bool(result[9]), "isAlcohol" : bool(result[10]), "isSilicone" : bool(result[11]), "isEUAllergen" : bool(result[12]), "isFungalAcneSafe" : bool(result[13])}
                ingredients_json.append(content)
            summary_json = {"parabenFree": parabenFree, "sulfateFree": sulfateFree, "alcoholFree": alcoholFree, "siliconeFree": siliconeFree, "euAllergenFree": euAllergenFree, "fungalAcne": fungalAcne, "acneFighting": acneFighting, "brightening": brightening, "uvProtection": uvProtection, "woundHealing": woundHealing, "antiAging": antiAging, "goodDrySkin": goodDrySkin, "badDrySkin": badDrySkin, "goodOilSkin": goodOilSkin, "badOilSkin": badOilSkin, "goodSensitiveSkin": goodSensitiveSkin, "badSensitiveSkin": badSensitiveSkin, "ingredients": ingredients_json}
            print(jsonify(summary_json))
            return jsonify(summary_json)
        else:
            return Response("No information found", status = 404)