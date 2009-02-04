import ldtp 
import ldtputils
from time import time

from desktoptesting.ubuntu import time

try:

    dataXml  = ldtputils.LdtpDataFileParser(datafilename)    
    password = dataXml.gettagvalue("password")[0]
    
    test = UpdateManager(password)
    
    start_time = time()
    
    test.open()
    test.check_updates()
    test.install_updates()
    test.close()

    stop_time = time()
    
    elapsed = stop_time - start_time
    
    ldtp.log ('elapsed_time: ' + str(elapsed), 'time')
    
except ldtp.LdtpExecutionError, msg:
    raise



