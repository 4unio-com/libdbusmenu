"""
main module contains the definition of the main Application class
that is used to wrap applications functionality
"""
import ldtp, ooldtp
import os

class Application:
    """
    Superclass for the rest of the applications

    Constants that should be defined in the classes that inherit from this class
    LAUNCHER: Argument to be passed when launching the application through ldtp.launchapp
    WINDOW: Top application frame pattern using ldtp syntax
    CLOSE_TYPE: Close object type (one of 'menu' or 'button')
    CLOSE_NAME: Close object name
    """
    CLOSE_TYPE = 'menu'
    CLOSE_NAME = 'mnuQuit'
    WINDOW     = ''
    TOP_PANEL = 'frmTopExpandedEdgePanel'


    def __init__(self, name = None, close_type= None, close_name= None):
        """
        @type close_type: string
        @param close_type: The type of close widget of the application. Types: menu, button.
        @type close_name: string
        @param close_name: The name of the close widget of the application. If not mentioned the default will be used ("Quit")
        """
        if name:
            self.name = name
        else:
            self.name = self.WINDOW

        if close_type:
            self.close_type = close_type
        else:
            self.close_type = self.CLOSE_TYPE

        if close_name:
            self.close_name = close_name
        else:
            self.close_name = self.CLOSE_NAME


    def set_name(self, name):
        if name is not None:
            self.name = name

    def set_close_type(self, close_type):
        if close_type is not None:
            self.close_type = close_type

    def set_close_name(self, close_name):
        if close_name is not None:
            self.close_name = close_name

    def remap(self):
        """
        It reloads the application map for the given ooldtp.context.
        """
        ldtp.remap(self.name)

    def open(self):
        """
        Given an application, it tries to open it.
         
        """
        self._enable_a11y(True)
        ldtp.launchapp(self.LAUNCHER)
        self._enable_a11y(False)

        ldtp.wait(2)
        response = ldtp.waittillguiexist(self.name, '', 20)
        
        if response == 0:
            raise ldtp.LdtpExecutionError, "The " + self.name + " window was not found."    

    def close(self):
        """
        Given an application, it tries to close it. 
        """
        try:
            app = ooldtp.context(self.name)
            try:
                close_widget = app.getchild(self.close_name)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "The " + self.close_name + " widget was not found."

            if self.close_type == 'menu':
                close_widget.selectmenuitem()
            elif self.close_type == 'button':
                close_widget.click()
            else:
                raise ldtp.LdtpExecutionError, "Wrong close item type."
            response = ldtp.waittillguinotexist(self.name, '', 20)
            if response == 0:
                raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application."
        except ldtp.LdtpExecutionError, msg:
            raise ldtp.LdtpExecutionError, "Mmm, something went wrong when closing the application: " + str(msg)

    def save(self, save_menu='mnuSave'):
        """
        Given an application, it tries to save the current document. 
        This method gives very basic functionality. Please, override this method in the subclasses for error checking.
         
        @type save_menu: string
        @param save_menu: The name of the Save menu of the application. If not mentioned the default will be used ("Save").
        """
        try:
            app = ooldtp.context(self.name)
            try:
                actualMenu = app.getchild(save_menu)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "The " + save_menu + " menu was not found."

            actualMenu.selectmenuitem()
        except ldtp.LdtpExecutionError:
            raise ldtp.LdtpExecutionError, "Mmm, something went wrong when saving the current document."

    def write_text(self, text, txt_field=''):
        """
        Given an application it tries to write text to its current buffer.
        """
        app = ooldtp.context(self.name)

        if txt_field == '':
            try:
                ldtp.enterstring(text)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "We couldn't write text."
        else:
            try:
                app_txt_field = app.getchild(txt_field)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "The " + txt_field + " text field was not found."
            try:
                app_txt_field.settextvalue(text)
            except ldtp.LdtpExecutionError:
                raise ldtp.LdtpExecutionError, "We couldn't write text."

    def _enable_a11y(self, enable):
        os.environ['NO_GAIL'] = str(int(not enable))
        os.environ['NO_AT_BRIDGE'] = str(int(not enable))
