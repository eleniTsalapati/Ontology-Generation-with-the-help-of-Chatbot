import os
log=open(os.getcwd()+"/log",mode="w")

def addToLog(txt):
    log.write(txt+"\n")
def closeLog():
    log.close()