import ldtp
import ldtputils

from desktoptesting.ubuntu import UpdateManager

class UpdateManagerTest(UpdateManager):
    def test_update_first(self, password):

        self.set_password(password)

        self.check_updates()
        list = self.get_available_updates()

        # If there is any update, select the first one
        if len(list) > 0:
            name = list[0]
            self.unselect_all()
            self.tick_update(name)
            self.install_updates()
     
        
        # Check again the list of updates
        list = self.get_available_updates()

        # If the updated package is still in the list of 
        # updates, the mark the test as failed.
        if name in list:
            raise AssertionError, 'The update ' + name + ' was not correctly installed.'

    def test_update_none(self, password):

        self.set_password(password)

        # Open the update manager and check the repositories
        self.check_updates()
        n_updates = self.number_updates()

        self.check_updates()
        n_updates2 = self.number_updates()


        # If the number of updates differ, the mark the test as failed.
        if n_updates != n_updates2:
           raise AssertionError, 'The number of updates should have been the same.'

    def test_unselect_all(self):

        size = self.download_size()

        if size > 0:
            self.unselect_all()
            self.remap()

            size = self.download_size()
            
            # Test size
            if size > 0:
                raise AssertionError, 'After unselecting all elements download size should be 0.'
            
            # Test button
            if manager.test_install_state():
                raise AssertionError, 'After unselecting all elements, install button should be disabled.'
     
    def test_install_updates(self, password):
    
        self.check_updates()
        self.install_updates()

        self.remap()
        n_updates = self.number_updates()
        
        if n_updates > 0:
            raise AssertionError, 'Not all the updates were installed.'
 
if __name__ == "__main__":
    test_update = UpdateManager()
    test_update.run()

