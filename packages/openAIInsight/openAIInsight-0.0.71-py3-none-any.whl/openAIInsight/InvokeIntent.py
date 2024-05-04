import requests, json, traceback, openai
from flask import request
import loggerutility as logger
import commonutility as common
import os
from datetime import datetime
from .InvokeIntent_LocalAI import InvokeIntentLocalAI
from .InvokeIntent_OpenAI import InvokeIntentOpenAI

class InvokeIntent:

    def getInvokeIntent(self):
        try:
            logger.log(f"\n\nInside getInvokeIntent()","0")
            jsonData = request.get_data('jsonData', None)
            logger.log(f"\njsonData openAI class::: {jsonData}","0")
            intentJson = json.loads(jsonData[9:])

            invokeIntentModel      = intentJson['INVOKE_INTENT_MODEL']
            if 'LocalAI' == invokeIntentModel:
                invokeIntentLocalAI = InvokeIntentLocalAI()
                finalResult = invokeIntentLocalAI.getInvokeIntent(intentJson, invokeIntentModel)

            elif 'OpenAI' == invokeIntentModel:
                invokeIntentOpenAI = InvokeIntentOpenAI()
                finalResult = invokeIntentOpenAI.getInvokeIntent(intentJson, invokeIntentModel)

            logger.log(f"\n\nOpenAI endpoint finalResult ::::: {finalResult} \n{type(finalResult)}","0")
            return finalResult
        
        except Exception as e:
            logger.log(f'\n In getIntentService exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)