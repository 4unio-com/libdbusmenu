"""
This is the "ubuntu" module.

The ubuntu module provides wrappers for LDTP to make the write of Ubuntu tests easier. 
"""
import ooldtp 
import ldtp 
import ubuntu_constants
from desktoptesting.gnome import Application, PolicyKit, open_and_check_app
import re

def open_and_check_menu_item(menu_item_txt, window_title_txt):
    """
    Given a menu item, it tries to open the application associated with it.
     
    @type menu_item_txt: string
    @param menu_item_txt: The name of the menu item that the user wants to open.
    
        The naming convention is the following:
        
        E{-} Prepend 'mnu' to the menu item
        
        E{-} Append the menu item with no spaces.
             
        Example: For the menu Disk Usage Analyzer, the menu name would be mnuDiskUsageAnalyzer.
        
    @type window_title_txt: string 
    @param window_title_txt: The name of the window to recognize once opened.
        
        The naming convention is the following:
        
        E{-} Prepend 'frm' if the window is a form, or 'dlg' if the window is a dialog.
        
        E{-} Append the window name with no spaces.
              
        Example: For the window Disk Usage Analyzer, the window name would be frmDiskUsageAnalyzer.
    
    """
    
    topPanel = ooldtp.context(ubuntu_constants.TOP_PANEL)
    
    try:
        actualMenu = topPanel.getchild(menu_item_txt)
    except ldtp.LdtpExecutionError:
        raise ldtp.LdtpExecutionError, "The " + menu_item_txt + " menu was not found: " 
  
    actualMenu.selectmenuitem()

    ldtp.wait(2)
    response = ldtp.waittillguiexist(window_title_txt, '', 20)
    
    if response == 0:
        raise ldtp.LdtpExecutionError, "The " + window_title_txt + " window was not found."    


 
class UpdateManager(Application):
    """
    UpdateManager class manages the Ubuntu Update Manager application.
    
    If the test is going to need admin permissions, you need to provide the su password
    when creating an instance of the class.
    
    i.e. C{updateManager = UpdateManager("my_password")}
    """
    
    def __init__(self, password = ""):
        """
        UpdateManager class init method
        
        If the test is going to need admin permissions, you need to provide the su password
        when creating an instance of the class.
        
        i.e. C{updateManager = UpdateManager("my_password")}
        
        @type password: string
        @param password: User's password for administrative tasks.

        """
        Application.__init__(self, ubuntu_constants.UM_WINDOW)
        self.password = password
        
    def open(self, dist_upgrade=False):
        """
        It opens the update-manager application and raises an error if the application
        didn't start properly.

        """

        if dist_upgrade:
            ldtp.launchapp(ubuntu_constants.UM_LAUNCHER, ['-d'], 0)
            response = ldtp.waittillguiexist(ubuntu_constants.UM_WINDOW, '', 20)
    
            if response == 0:
                raise ldtp.LdtpExecutionError, "The " + ubuntu_constants.UM_WINDOW + " window was not found."    

        else:
            open_and_check_app(ubuntu_constants.UM_LAUNCHER, ubuntu_constants.UM_WINDOW)

        # Wait the population of the list
        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)

        populating = True

        try:
            while populating:
                populating = False
                self.remap()

                label = updateManager.getchild(role = 'label')
                for i in label:
                    label_name = i.getName()
                    if label_name == ubuntu_constants.UM_LBL_WAIT:
                        populating = True
        
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager description label was not found."
    
    def close(self):
        """
        It closes the update-manager window using the close button.
        """

        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)
    
        try:
            closeButton = updateManager.getchild(ubuntu_constants.UM_BTN_CLOSE)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager Close button was not found."
          
        closeButton.click()
        ldtp.waittillguinotexist (ubuntu_constants.UM_WINDOW)
           
    def number_updates(self):
        """
        With the available repositories, it returns the number of available
        updates for the system. 

        @return: An integer with the number of available updates.
        
        """
        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)

        try:
            label = updateManager.getchild(role = 'label')
            for i in label:
                label_name = i.getName()
                if label_name == ubuntu_constants.UM_LBL_UPTODATE:
                    return 0
                else:
                    groups = re.match(ubuntu_constants.UM_LBL_N_UPDATES, label_name)
                    if groups:
                        number = groups.group(1)
                        return int(number)

        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Error getting number of updates"

        return 0

    def download_size(self):
        """
        It returns the download size of the selected updates.

        @return: A float with the download size in bytes 
        """
        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW) 

        try:
            label = updateManager.getchild(role = 'label')
            for i in label:
                label_name = i.getName()
                groups = re.match(ubuntu_constants.UM_LBL_DOWNLOADSIZE, label_name)
                
                if groups:
                    # Calculate size based on the tag after the number
                    tag_size = groups.group(6)
                    if tag_size == 'B':
                        size = 1
                    elif tag_size == 'KB':
                        size = 1024
                    elif tag_size == 'MB':
                        size = 1048576
                    elif tag_size == 'GB':
                        size = 1073741824
                    else:
                        size = 0

                    total_size = float(groups.group(1)) * size
                    return total_size

        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Error getting the download size."

        return 0.0

    def select_all(self):
        """
        It selects all the available updates 
        """
        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW) 

        try:
            table  = updateManager.getchild(ubuntu_constants.UM_TBL_UPDATES, role = 'table')
            updates_table = table[0]

            for i in range(0, updates_table.getrowcount(), 1):
                updates_table.checkrow(i)
                ldtp.wait(1)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Error getting the updates table."

        return 0

    def unselect_all(self):
        """
        It unselects all the available updates 
        """
        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW) 

        try:
            table  = updateManager.getchild(ubuntu_constants.UM_TBL_UPDATES, role = 'table')
            updates_table = table[0]

            # TODO: When table admits right click, use the context menu
            self.remap()
            size_updates = self.download_size()
            while size_updates > 0:
                for i in range(0, updates_table.getrowcount(), 1):
                    updates_table.uncheckrow(i)
                    ldtp.wait(1)
                self.remap()
                size_updates = self.download_size()
 
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Error getting the updates table."

        return 0

    def get_available_updates(self):
        """
        It gets the name of the packages of the available updates 

        @return: A list with the available updates
        """

        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)

        available_updates = []

        try:
            table  = updateManager.getchild(ubuntu_constants.UM_TBL_UPDATES, role = 'table')
            updates_table = table[0]

            for i in range(0, updates_table.getrowcount(), 1):
                text = updates_table.getcellvalue(i, 1)
                candidate = text.split('\n')[0]
                if candidate.find(ubuntu_constants.UM_BAN_LIST) == -1:
                    available_updates.append(candidate)
                ldtp.wait(1)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Error getting the updates table."

        return available_updates

    def select_update(self, name):
        """
        It selects a particular package in the list (not for update, just the list).

        @type name: string
        @param name: The name of the package to select
        """

        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)

        try:
            table  = updateManager.getchild(ubuntu_constants.UM_TBL_UPDATES, role = 'table')
            updates_table = table[0]

            for i in range(0, updates_table.getrowcount(), 1):
                text = updates_table.getcellvalue(i, 1)
                candidate = text.split('\n')[0]
                if candidate == name:
                    updates_table.selectrowindex(i)
                    break
                ldtp.wait(1)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Error getting the updates table."

    def tick_update(self, name):
        """
        It selects a particular package for update.

        @type name: string
        @param name: The name of the package to select
        """

        updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)

        try:
            table  = updateManager.getchild(ubuntu_constants.UM_TBL_UPDATES, role = 'table')
            updates_table = table[0]

            for i in range(0, updates_table.getrowcount(), 1):
                text = updates_table.getcellvalue(i, 1)
                candidate = text.split('\n')[0]
                if candidate == name:
                    updates_table.checkrow(i)
                    break
                ldtp.wait(1)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Error getting the updates table."

    def check_updates(self):
        """
        It checks the repositories for new updates in the update-manager application.
        
        This action requires administrative permissions, therefore this method will
        raise an error if the UpdateManager instance was created without password.
        """

        try:
            updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager window was not found."
        
        if self.password == "":
            raise ldtp.LdtpExecutionError, "Checking for updates requires administrative permissions."

        
        # We will need administrative permission
        polKit = PolicyKit(self.password)

        try:
            checkButton = updateManager.getchild(ubuntu_constants.UM_BTN_CHECK)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager Check button was not found."
          
        checkButton.click()
 
        # Administrative permissions
        if polKit.wait():
            # HACK
            ldtp.wait(2)
            polKit.set_password()
        
        # HACK to wait for repositories
        ldtp.wait(20)

    def install_updates(self):
        """
        It installs the selected updates. 
        
        If no updates are available, it won't do anything.
        """

        try:
            updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager window was not found."

        # If there is any update available, install it
        if self.number_updates() > 0:
            
            try:
                btnInstall = updateManager.getchild(ubuntu_constants.UM_BTN_INSTALL)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "The Update Manager install button was not found."
            
            if btnInstall.stateenabled():
                btnInstall.click()

                # We will need administrative permission
                polKit = PolicyKit(self.password)

               # Administrative permissions
                if polKit.wait():
                    # HACK
                    ldtp.wait(2)
                    polKit.set_password()
        
        # Wait for the the close button to be ready
        try:
            btnClose = updateManager.getchild(ubuntu_constants.UM_BTN_CLOSE)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager Close button was not found."
        
        while not btnClose.stateenabled():
            ldtp.wait(5)
            
    def test_install_state(self):
        """
        It checks if the install button is enabled or not

        @return: True if the install button is enabled. False, otherwise.
        """

        try:
            updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager window was not found."
        
        try:
            btnTest = updateManager.getchild(ubuntu_constants.UM_BTN_INSTALL)
            state = btnTest.stateenabled()
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The install button was not found."
        
        return state

    def show_changes(self):
        """
        It shows the Description of the updates 
        """
        self.toggle_changes(True)

    def hide_changes(self):
        """
        It hides the Description of the updates 
        """
        self.toggle_changes(False)

    def get_description(self, name=''):
        """
        It returns the description of a package for a given update.
        If no update is mentioned, then the description for the
        selected application is returned.

        @type name: string
        @param name: The package to show the description. If left blank, the current
        selection will be chosen.

        @return: The decription of the packages, as shown in the application
        """
        try:
            updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager window was not found."
        
        try:
            if name != '':
                self.select_update(name)

            # Get the description text field 
            text_field = updateManager.getchild(ubuntu_constants.UM_TXT_DESCRIPTION, role='text')
             # Get the text 
            text = ldtp.gettextvalue(ubuntu_constants.UM_WINDOW, text_field[0].getName())
            return text
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The description text was not found."
        
        return '' 

    def get_changes(self, name=''):
        """
        It returns the changes description for a given update.
        If no update is mentioned, then the changes description for the
        selected application is returned.

        @type name: string
        @param name: The package to show changes. If left blank, the current
        selection will be chosen.

        @return: The decription of the changes
        """
        try:
            ooldtp.context(ubuntu_constants.UM_WINDOW)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager window was not found."
        
        try:
            if name != '':
                self.select_update(name)

            # Get the filler tab
            filler = ldtp.getobjectproperty(ubuntu_constants.UM_WINDOW , ubuntu_constants.UM_TAB_CHANGES, 'children')
            # Get the scroll pane
            scroll_pane = ldtp.getobjectproperty(ubuntu_constants.UM_WINDOW , filler, 'children')
            # Get the text field
            text_field = ldtp.getobjectproperty(ubuntu_constants.UM_WINDOW , scroll_pane, 'children')
            text_field = text_field.split(' ')[0]
            # Get the text
            text = ldtp.gettextvalue(ubuntu_constants.UM_WINDOW, text_field)
            return text
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Changes tab was not found."
        
        return '' 

    def toggle_changes(self, show):
        """
        It shows or hides the Description of the updates 

        @type show: boolean
        @param show: True, to show the description; False, to hide the description.
        """
        try:
            updateManager = ooldtp.context(ubuntu_constants.UM_WINDOW)
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The Update Manager window was not found."
        
        try:
            toggle_button = updateManager.getchild(role='toggle button')
            state = toggle_button[0].verifytoggled()

            if state != show:
                toggle_button[0].click()
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "The description button was not found."
        
        return state
    
   
