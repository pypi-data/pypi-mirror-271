import requests, json, traceback
from flask import request
import loggerutility as logger
import commonutility as common
import os
from datetime import datetime
from openai import OpenAI
import threading

class InvokeIntentOpenAI:

    uuid            =  ""
    user_id         =  ""
    historyCount    =  ""

    def getInvokeIntent(self, intentJson, invokeIntentModel):
        try:
            logger.log(f"\n\nInside InvokeIntentOpenAI getInvokeIntent()","0")
            jsonData    = request.get_data('jsonData', None)
            intentJson  = json.loads(jsonData[9:])
            logger.log(f"\njsonData openAI class::: {jsonData}","0")
            
            finalResult     =  {}
            openAI_APIKey   =  intentJson['openAI_APIKey'] 
            intent_input    =  intentJson['intent_input']
            enterprise      =  intentJson['enterprise']
            self.user_id    =  intentJson['user_id']
            self.uuid       =  intentJson['uuid']

            if 'user_id' in intentJson.keys():
                self.user_id = intentJson['user_id']
                logger.log(f"\n localAIURL openAI class::: {self.user_id}","0")

            if 'uuid' in intentJson.keys():
                self.uuid = intentJson['uuid']
                logger.log(f"\n UUID openAI class::: {self.uuid}","0") 
            
            if 'history_count' in intentJson.keys():
                self.historyCount = intentJson['history_count']
                logger.log(f"\n history_Count openAI class::: {self.historyCount}","0") 

            fileName        = "intent_Instructions.txt"
            client = OpenAI(
                                api_key = openAI_APIKey,
                            )
            
            logger.log(f"\n\njsonData getIntentService fileName::: \t{fileName}\n","0")

            current_datetime = datetime.now()
            logger.log(f"\n\current_datetime datatype ::: \t{type(current_datetime)} \t {current_datetime}\n","0")
        
            formatted_datetime = current_datetime.strftime("%d-%b-%Y, %H:%M:%S")
            logger.log(f"\n\ndateteme datatype ::: \t{type(formatted_datetime)}\n","0")
            logger.log(f"\n\njsonData openAI class datetime::: \t{formatted_datetime}\n","0")
            
            if os.path.exists(fileName):
                intent_trainingData = open(fileName,"r").read()
            else:
                logger.log(f"\n\n{fileName}  does not exist.\n","0")  
                message = f"The Intent API service could not be requested due to missing '{fileName}' file. "
                return message
                
            logger.log(f"\n\ngetIntentService before conversion :::::: {type(intent_trainingData)} \n{intent_trainingData}\n","0")
            replaced_trainingData = intent_trainingData.replace("<intent_input>", intent_input)
            logger.log(f"\n\ngetIntentService after replacing <intent_input> :::::: \n{replaced_trainingData} \n{type(replaced_trainingData)}","0")
            
            logger.log(f"\n\nopenAI_trainingData before conversion date:::::: {type(intent_trainingData)} \n{intent_trainingData}\n","0")
            replaced_trainingData = replaced_trainingData.replace("<Current_date_time>", formatted_datetime)
            logger.log(f"\n\nopenAI_trainingData after replacing date <Current_date_time> :::::: \n{replaced_trainingData} \n{type(replaced_trainingData)}","0")
            
            messageList = json.loads(replaced_trainingData)
            logger.log(f"\n\nmessageList after conversion :::::: {messageList} \n{type(messageList)}","0")
            
            concatenated_value = f"{self.user_id}_{self.uuid}"
            logger.log(f"\nConcatenated value: {concatenated_value}","0") 

            fileData, read_data_json = self.read_json_file(self.user_id, concatenated_value+'.json', invokeIntentModel)
            logger.log(f"\n\n  read_data_json line 76 :::::: {read_data_json}","0")

            if len(read_data_json) == 0:
                logger.log(f"json data empty in '{concatenated_value}.json' file")
                logger.log(f"\n\n final messageList  line 80 :::::: {messageList}","0")

            else:
                messageList.insert(-1,read_data_json)
                logger.log(f"\n\n final messageList line 84 :::::: {messageList}","0")
            logger.log(f"\n\nfinal messageList :::::: {messageList}","0")
            
            if self.user_id and self.user_id != "":
                response = client.chat.completions.create(
                                                            model               = "gpt-3.5-turbo",
                                                            messages            = messageList,
                                                            temperature         = 0,
                                                            max_tokens          = 1800,
                                                            top_p               = 1,
                                                            frequency_penalty   = 0,
                                                            presence_penalty    = 0,
                                                            user                = self.user_id,
                                                        )
            else:
                response = client.chat.completions.create(
                                                            model               = "gpt-3.5-turbo",
                                                            messages            = messageList,
                                                            temperature         = 0,
                                                            max_tokens          = 1800,
                                                            top_p               = 1,
                                                            frequency_penalty   = 0,
                                                            presence_penalty    = 0,
                                                        )
            logger.log(f"\n\nResponse openAI endpoint::::: {response} \n{type(response)}","0")
            finalResult= str(response.choices[0].message.content) 
            logger.log(f"\n\nOpenAI endpoint finalResult ::::: {finalResult} \n{type(finalResult)}","0")

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
