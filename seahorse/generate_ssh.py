import ldtp 
import ldtputils 
from time import time 

from desktoptesting.gnome import Seahorse

try:
  
    dataXml     = ldtputils.LdtpDataFileParser(datafilename)    
    description = dataXml.gettagvalue("description")[0]
    set_up      = dataXml.gettagvalue("set_up")[0]
    passphrase  = dataXml.gettagvalue("passphrase")[0]
    computer    = ''
    login       = ''

    if set_up == 'True':
        computer    = dataXml.gettagvalue("computer")[0]
        login       = dataXml.gettagvalue("login")[0]
    
    seahorse = Seahorse()
    
    start_time = time()
    
    # Open the update manager and check the repositories
    seahorse.open()
    seahorse.new_ssh_key(description, passphrase, set_up, computer, login)
    
    # Check that the key was successfully created
    if seahorse.assert_exists_key(description) == False:
        seahorse.exit()
        raise ldtp.LdtpExecutionError, "The key was not successfully created."

    seahorse.exit()
        
    stop_time = time()
 
    elapsed = stop_time - start_time
    
    ldtp.log (str(elapsed), 'time')
    
except ldtp.LdtpExecutionError, msg:
    raise



