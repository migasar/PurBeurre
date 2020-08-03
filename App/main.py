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

    def renew_database(self):
        # create the database
        self.controller.create_database()

    def start_session(self):
        # launch the terminal interface
        self.controller.new_session()


if __name__ == "__main__":
    main = Main()
