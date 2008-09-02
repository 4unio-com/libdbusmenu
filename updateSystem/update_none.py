from ooldtp import *
from ldtp import *
from ldtputils import *
from time import *

from ubuntutesting.ubuntu import *

try:
  
    dataXml  = LdtpDataFileParser(datafilename)    
    password = dataXml.gettagvalue("password")[0]
    
    updateManager = UpdateManager(password)
    
    start_time = time()
    
    # Open the update manager and check the repositories
    updateManager.open()
    updateManager.check_updates()
    n_updates = updateManager.number_updates()

    updateManager.check_updates()
    n_updates2 = updateManager.number_updates()

    updateManager.close()

    # If the number of updates differ, the mark the test as failed.
    if n_updates != n_updates2:
        log('The number of updates should have been the same.', 'ERROR')
        log('The number of updates should have been the same.', 'CAUSE')

    stop_time = time()
 
    elapsed = stop_time - start_time
    
    log ('elapsed_time: ' + str(elapsed), 'comment')
    
except LdtpExecutionError, msg:
    raise



