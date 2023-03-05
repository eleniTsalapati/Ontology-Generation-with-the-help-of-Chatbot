from modules.UI import UI
import modules.chatbotTalks as talk
import modules.ontologyManager as manager
import modules.chatbotHears as hear
import modules.utility as utility
from modules.mainFunction import *
from modules.application import C4OApplication
import sys
import modules.log as log
import threading
# -------------------------------------------------------
#                       main
# -------------------------------------------------------
from modules.shared_data import *
def UI_(lock):
    app = C4OApplication()
    app.run(sys.argv)
    log.closeLog()

def server(lock):
    global data,dangerArea,hearServer,answerUI,thePath
    while(True):
        hearServer.acquire()
        dangerArea.acquire()
        manager.SaveOntology(data[2],thePath)

        theList=answerUI.split(";")
        answer=theList[0]
        sentence=" ".join(theList[1:])
        dangerArea.release()
        print(answer,sentence)
        # if answer == "Sentence":
        #     Sentence(data,sentence)
        # elif answer == "Generalized":
        #     generalized(data,sentence)
        # elif answer == "Specialize":
        #     specialize(data,sentence)
        # elif answer == "Destroy Entity":
        #     destroy(data,sentence)

if __name__ =="__main__":
    lock = threading.Lock()
    t1 = threading.Thread(target=UI_, args=(lock,))
    t2 = threading.Thread(target=server, args=(lock,))
 
    # starting thread 1
    t1.start()
    # starting thread 2
    t2.start()
 
    # wait until thread 1 is completely executed
    t1.join()
    # wait until thread 2 is completely executed
    t2.join()
 
    # both threads completely executed
    print("Done!")