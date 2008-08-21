from ooldtp import *
from ldtp import *
from ldtputils import *
from time import *

from ubuntutesting.ubuntu import *

try:

    dataXml  = LdtpDataFileParser(datafilename)    
    password = dataXml.gettagvalue("password")[0]
    
    test = UpdateManager(password)
    
    start_time = time()
    
    test.open()
    test.check_updates()
    test.install_updates()
    test.close()

    stop_time = time()
    
    elapsed = stop_time - start_time
    
    log ('elapsed_time: ' + str(elapsed), 'comment')
    
except LdtpExecutionError, msg:
    raise



