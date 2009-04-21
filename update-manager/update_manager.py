import ldtp
import ldtputils

from desktoptesting.ubuntu import UpdateManager
from desktoptesting.test_suite import UpdateManagerTestSuite

class UpdateManagerTest(UpdateManagerTestSuite):
    def test_update_first(self, password):
        self.application.set_password(password)

        self.application.check_updates()
        list = self.application.get_available_updates()

        # If there is any update, select the first one
        if len(list) > 0:
            name = list[0]
            self.application.unselect_all()
            self.application.tick_update(name)
            self.application.install_updates()
     
        
        # Check again the list of updates
        list = self.application.get_available_updates()

        # If the updated package is still in the list of 
        # updates, the mark the test as failed.
        if name in list:
            raise AssertionError, 'The update ' + name + ' was not correctly installed.'

    def test_update_none(self, password):

        self.application.set_password(password)

        # Open the update manager and check the repositories
        self.application.check_updates()
        n_updates = self.application.number_updates()

        self.application.check_updates()
        n_updates2 = self.application.number_updates()


        # If the number of updates differ, the mark the test as failed.
        if n_updates != n_updates2:
           raise AssertionError, 'The number of updates should have been the same.'

    def test_unselect_all(self):

        size = self.application.download_size()

        if size > 0:
            self.application.unselect_all()
            self.application.remap()

            size = self.application.download_size()
            
            # Test size
            if size > 0:
                raise AssertionError, 'After unselecting all elements download size should be 0.'
            
            # Test button
            if manager.test_install_state():
                raise AssertionError, 'After unselecting all elements, install button should be disabled.'
     
    def test_install_updates(self, password):
    
        self.application.check_updates()
        self.application.install_updates()

        self.application.remap()
        n_updates = self.application.number_updates()
        
        if n_updates > 0:
            raise AssertionError, 'Not all the updates were installed.'
 
if __name__ == "__main__":
    test_update = UpdateManager()
    test_update.run()

