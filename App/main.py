"""In charge of the launch of the program.

Call all the elements of the program in an orchestrated manner.
"""

from Model.Manager.db_manager import DBManager
from Model.Manager.entity_manager import EntityManager
from Model.Manager.api_manager import APIManager

from Controller.cli_controller import CLIController
from View.cli_view import CLIView


class Main:

    def __init__(self):

        # create the managers
        self.db_manager = DBManager()
        self.entity_manager = EntityManager(self.db_manager)
        self.api_manager = APIManager()

        # create the controllers
        self.controller = CLIController()
        self.view = CLIView()

    def create_database(self):

        # build the database skeleton
        self.db_manager.build_database()

        # call the API
        self.api_manager.get_load()

        # download the data (from the API to the DB)
        self.api_manager.download_data(self.entity_manager)

    def start_session(self):
        pass


if __name__ == "__main__":
    main = Main()
