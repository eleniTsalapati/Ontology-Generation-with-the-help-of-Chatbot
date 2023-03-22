from modules.application import C4OApplication
import sys
import modules.log as log

app = C4OApplication()
app.run(sys.argv)
log.closeLog()
