from flask import Blueprint,request
from flask_login import current_user, login_required, login_user, logout_user
from .mainController import mainController

routes = Blueprint('routes', __name__)

mainControllerC = mainController()

@routes.route('/getIngredientsAnalysis', methods=['POST'])
def getIngredientsAnalysis():
    return mainControllerC.getIngredientsAnalysis(request)

@routes.route('/getBarcode', methods=['POST'])
def getBarcode():
    return mainControllerC.getBarcode(request)
