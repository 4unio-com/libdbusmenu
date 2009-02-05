import ldtp
import ldtputils
from time import time

from desktoptesting.ubuntu import UpdateManager

try:
  
    dataXml  = ldtputils.LdtpDataFileParser(datafilename)    
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
        ldtp.log('The number of updates should have been the same.', 'error')
        ldtp.log('The number of updates should have been the same.', 'cause')

    stop_time = time()
 
    elapsed = stop_time - start_time
    
    ldtp.log (str(elapsed), 'time')
    
except ldtp.LdtpExecutionError, msg:
    raise



