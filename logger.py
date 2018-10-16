import logging
import uuid

logging.basicConfig(filename="system.log",
                    format='%(message)s on %(asctime)s ',
                    filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def writeLog(category, message, gennedID):
    if category == 1:
        category = 'Info   '
    elif category == 2:
        category = 'Start  '
    elif category == 3:
        category = 'Finish '
    elif category == 4:
        category = 'Error  '
    else:
        category = 'Warning'
    message = category + ':'+' id: '+str(gennedID)+' : '+message
    logger.info(message)

def queryLog(text):
    messages = []
    file = open('system.log', 'r')
    lines = file.readlines()
    for line in lines:
        if text in line:
            messages.append(line)
    queryFile = open('result.txt', 'w')
    result = 'found: '+str(len(messages))+' matches \n'
    queryFile.write(result)
    queryFile.writelines(messages)

def genID():
    return uuid.uuid1()

""" writeLog(1, 'asaasa', genID())
writeLog(2, 'asaasa', genID())
writeLog(3, 'asaasa', genID())
writeLog(1, 'asaasa', genID())
writeLog(4, 'asaasa', genID())
writeLog(1, 'asaasa', genID()) """
  
queryLog('6e8f2ea5-d18b-11e8-9e13-4c3488d6805d')
