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
    list = updateManager.get_available_updates()

    # If there is any update, select the first one
    if len(list) > 0:
        name = list[0]
        updateManager.unselect_all()
        updateManager.tick_update(name)
        updateManager.install_updates()
    
    # Close the update manager and reopen
    updateManager.close()
    updateManager.open()
    # Check again the list of updates
    list = updateManager.get_available_updates()

    updateManager.close()

    # If the updated package is still in the list of 
    # updates, the mark the test as failed.
    if name in list:
        ldtp.log('The update ' + name + ' was not correctly installed.', 'error')
        ldtp.log('The update ' + name + ' was not correctly installed.', 'cause')
        
    stop_time = time()
 
    elapsed = stop_time - start_time
    
    ldtp.log (str(elapsed), 'time')
    
except ldtp.LdtpExecutionError, msg:
    raise



