from ooldtp import *
from ldtp import *
from ldtputils import *
from time import *

from ubuntutesting.ubuntu import *

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
            log('After unselecting all elements download size should be 0.', 'ERROR')
            log('After unselecting all elements download size should be 0.', 'CAUSE')
        
        # Test button
        if manager.test_install_state():
            log('After unselecting all elements, install button should be disabled', 'ERROR')
            log('After unselecting all elements, install button should be disabled', 'CAUSE')
 

    manager.close()
    stop_time = time()
    elapsed = stop_time - start_time
    log ('elapsed_time: ' + str(elapsed), 'comment')
    
except LdtpExecutionError, msg:
    raise



