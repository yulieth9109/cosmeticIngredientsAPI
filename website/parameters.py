import json


with open('parameters.json') as json_file:

    hostDB = databaseP['host']
    userDB = databaseP['user']
    passwordDB = databaseP['password']
    database = databaseP['database']
    openAI = data['OpenAI']
    openAISecret = openAI['secretKey']