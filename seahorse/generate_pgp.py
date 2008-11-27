from ooldtp import *
from ldtp import *
from ldtputils import *
from time import *

from ubuntutesting.gnome import *

try:
  
    #dataXml  = LdtpDataFileParser(datafilename)    
    #password = dataXml.gettagvalue("password")[0]
    
    #updateManager = UpdateManager(password)
    
    seahorse = Seahorse()
    
    start_time = time()
    
    # Open the update manager and check the repositories
    seahorse.open()
    seahorse.new_pgp_key("Ara Tester", "tester@tester.org", "This is a test", "passphrase")
    seahorse.exit()
        
    stop_time = time()
 
    elapsed = stop_time - start_time
    
    log ('elapsed_time: ' + str(elapsed), 'comment')
    
except LdtpExecutionError, msg:
    raise



