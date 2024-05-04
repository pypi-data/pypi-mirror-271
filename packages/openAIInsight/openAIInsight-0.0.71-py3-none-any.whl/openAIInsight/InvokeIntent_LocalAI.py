import requests, json, traceback, openai
from flask import request
import loggerutility as logger
import commonutility as common
import os
from datetime import datetime
from openai import OpenAI
import threading


class InvokeIntentLocalAI:

    uuid            =  ""
    userId          =  "" 
    localAIURL      =  ""  
    historyCount    =  ""
    
    def getInvokeIntent(self, intentJson, invokeIntentModel):
        try:
            logger.log(f"\n\nInside InvokeIntentLocalAI getInvokeIntent()","0")
            jsonData = request.get_data('jsonData', None)
            intentJson = json.loads(jsonData[9:])
            logger.log(f"\njsonData openAI class::: {intentJson}")  
            
            finalResult     =  {}
            read_data_json  =  []
            openAI_APIKey   =  intentJson['openAI_APIKey'] 
            intent_input    =  intentJson['intent_input']
            enterprise      =  intentJson['enterprise']
            intent_args     =  intentJson['INTENT_LIST']

            if 'uuid' in intentJson.keys():
                self.uuid         = intentJson['uuid']
            
            if 'user_id' in intentJson.keys():
                self.user_id      = intentJson['user_id']
            
            if 'LOCAL_AI_URL' in intentJson.keys():
                self.localAIURL   =  intentJson['LOCAL_AI_URL'] 
                
            if 'history_count' in intentJson.keys():
                self.historyCount = intentJson['history_count']
            logger.log(f"\n\n UUID LocalAI class::: {self.uuid} \n user_id LocalAI class::: {self.user_id} \n localAIURL LocalAI class::: {self.localAIURL} \n history_Count LocalAI class::: {self.historyCount}\n\n","0") 

            concatenated_value = f"{self.user_id}_{self.uuid}"
            logger.log(f"\nConcatenated value: {concatenated_value}","0") 

            fileName        = "Intent_Instructions_Local.txt"
            openai.api_key  = openAI_APIKey
            
            logger.log(f"\n\njsonData getIntentService fileName::: \t{fileName}\n","0")
            
            if os.path.exists(fileName):
                intent_trainingData = open(fileName,"r").read()
                intent_trainingData = intent_trainingData.replace("<intent_args>", intent_args).replace("<current_date>", datetime.now().strftime("%d-%b-%Y").upper()).replace("<year>",  datetime.now().strftime("%Y"))
                logger.log(f"\n\nintent_trainingData after replacment ::: {intent_trainingData}  \n","0")  
            else:
                logger.log(f"\n\n{fileName}  does not exist.\n","0")  
                message = f"The Intent API service could not be requested due to missing '{fileName}' file. "
                return message
                
            userPrompt = "Chat Input: "+intent_input+""
            
            fileData, read_data_json = self.read_json_file(self.user_id, concatenated_value+'.json', invokeIntentModel)

            if len(read_data_json) == 0:
                logger.log(f"json data empty in '{concatenated_value}.json' file")
                message = [
                    {"role": "system", "content": intent_trainingData},
                    {"role": "user", "content"  : userPrompt}  
                ]
                logger.log(f"\n\n final messageList  line 139 :::::: {message}","0")

            else:
                message = [
                    {"role": "system", "content": intent_trainingData},
                    *read_data_json,
                    {"role": "user", "content"  : userPrompt}  
                ]
                logger.log(f"\n\n final messageList line 80 :::::: {message}\n\n","0")

            logger.log(f'\n Print time on start : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            
            client = OpenAI(base_url=self.localAIURL, api_key="lm-studio")        
            completion = client.chat.completions.create(
                                                            model           =  "mistral" ,        
                                                            messages        =  message ,
                                                            temperature     =  0 ,
                                                            stream          =  False,
                                                            max_tokens      =  4096
                                                        )

            finalResult = str(completion.choices[0].message.content)
            logger.log(f"\n\nLocalAI endpoint finalResult ::::: {finalResult} \n{type(finalResult)}","0")
            finalResult = json.loads(str(finalResult).replace("\\",""))
            logger.log(f"\n\nLocalAI endpoint finalResult filtered ::::: {finalResult} \n{type(finalResult)}","0")
            logger.log(f'\n Print time on end : {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', "0")
            logger.log(f"\n\nLocalAI endpoint finalResult ::::: {finalResult} \n{type(finalResult)}","0")
 
            thread = threading.Thread(target=common.write_JsonFile, args = [concatenated_value+'.json', intent_input, fileData, invokeIntentModel, finalResult])
            thread.start()
            thread.join()

            return finalResult
        
        except Exception as e:
            logger.log(f'\n In getIntentService exception stacktrace : ', "1")
            trace = traceback.format_exc()
            descr = str(e)
            returnErr = common.getErrorXml(descr, trace)
            logger.log(f'\n Exception ::: {returnErr}', "0")
            return str(returnErr)
    
    def read_json_file(self, user_id, user_filename, invokeIntentModel):
        '''
        This function is used to read JSON file with stored history count of each input query and resultant output. 
        Params  :
            user_filename     : str  --> userId_uuid.json
            user_id           : str  --> SWAPNIL
            requireAllData    : bool 
            invokeIntentModel : str  --> LocalAI / OpenAI
        '''
        
        file_data_history   = ""
        directory_fileList  = []
        directoryPath       = f"{invokeIntentModel}_Instruction"
        fileName            = directoryPath + "/" + user_filename
        
        if os.path.exists(directoryPath):
            logger.log(f"Folder LocalAI_Instruction is present:::  {directoryPath}")
            
            if os.path.exists(fileName):
                with open(fileName, "r") as f:
                    fileData = f.read()
                    logger.log(f"\nfileData line 25 ::: {fileData} \t {type(fileData)}\n\n")
                    if type(fileData) == str:
                        fileData = json.loads(fileData)
                    
                    self.historyCount = int(self.historyCount) if self.historyCount != "" else -6
                    file_data_history = fileData[self.historyCount : ]

                    logger.log(f"\n\nfile_data_history::: {file_data_history}\n\n")
                    return fileData, file_data_history
            else:
                logger.log(f"userId_uuid File not present ::: {fileName}")
                directory_fileList = os.listdir(directoryPath)
                filesHaving_UserId =[file for file in directory_fileList if user_id in file]
                if len(filesHaving_UserId) != 0:
                    for file in filesHaving_UserId :
                        os.remove(directoryPath + "/" + file)
                        logger.log(f"File with userId deleted::: {file}\n")
                        return [], []
                else:
                    logger.log(f"Directory is empty. line 44")
                    return [], []
        else:
            logger.log(f"Directory not  present ::: {directoryPath}")
            return [], []
    
        
        




        

