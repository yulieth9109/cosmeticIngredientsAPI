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

@routes.route('/Product', methods=['POST'])
def createProduct():
    return mainControllerC.createProduct(request)

@routes.route('/User', methods=['POST'])
def createUser():
    return mainControllerC.createUser(request)

@routes.route('/Login', methods=['POST'])
def loginUser():
    return mainControllerC.loginUser(request)

@routes.route('/confirm/<token>')
def confirm_email(token):
    return mainControllerC.confirmEmail(token)

@routes.route('/getId', methods=['POST'])
def getInfoById():
    return mainControllerC.getInfoById(request)

@routes.route('/search', methods=['POST'])
def searchProducts():
    return mainControllerC.searchProducts(request)

@routes.route('/Review', methods=['POST'])
def createReview():
    return mainControllerC.createReview(request)

@routes.route('/Reviews', methods=['POST'])
def getReviews():
    return mainControllerC.getReviews(request)

@routes.route('/userReviews', methods=['POST'])
def getUserReviews():
    return mainControllerC.getUserReviews(request)

@routes.route('/deleteReview', methods=['POST'])
def deleteReview():
    return mainControllerC.deleteReview(request)