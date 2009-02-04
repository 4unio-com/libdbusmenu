from ldtp import log, LdtpExecutionError 
from time import time 

from desktoptesting.ubuntu import UpdateManager 

# Test:
# Unselect all the available updates if any
# After that, download size must be 0
# and the install button should be disabled

try:

    
    manager = UpdateManager()
    
    start_time = time()
    
    manager.open()
    size = manager.download_size()

    if size > 0:
        manager.unselect_all()
        manager.remap()

        size = manager.download_size()
        
        # Test size
        if size > 0:
            ldtp.log('After unselecting all elements download size should be 0.', 'error')
            ldtp.log('After unselecting all elements download size should be 0.', 'cause')
        
        # Test button
        if manager.test_install_state():
            ldtp.log('After unselecting all elements, install button should be disabled', 'error')
            ldtp.log('After unselecting all elements, install button should be disabled', 'cause')
 

    manager.close()
    stop_time = time()
    elapsed = stop_time - start_time
    ldtp.log ('elapsed_time: ' + str(elapsed), 'test')
    
except ldtp.LdtpExecutionError, msg:
    raise



