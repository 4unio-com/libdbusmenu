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
    updateManger.check_updates()
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
        log('The update ' + name + ' was not correctly installed.', 'ERROR')
        log('The update ' + name + ' was not correctly installed.', 'CAUSE')
        
    stop_time = time()
 
    elapsed = stop_time - start_time
    
    log ('elapsed_time: ' + str(elapsed), 'comment')
    
except LdtpExecutionError, msg:
    raise



