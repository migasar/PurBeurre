"""Manage the flow of the program, and the interactions of its components."""

from Model.Manager.entity_manager import EntityManager
from Model.Manager.api_manager import APIManager
from View.cli_view import CLIView


class CLIController:
    """Pilot the flow of the program.

    It orchestrate the interactions between the main elements of the program:
     - the models
     - the views
     - the input of the user
    """

    # Class variable (register of all the possible phases in the flow of the program):
    steps = {
            'opening': 1,
            'category': 2,
            'product': 3,
            'substitute': 4,
            'saving': 5,
            'favorite': 6,
            'closing': 99
    }

    def __init__(self):

        self.entity_manager = EntityManager()
        self.api_manager = APIManager()
        self.view = CLIView()
        self.choice = None  # user input
        self.phase = self.steps['opening']  # the actual phase in the flow of the program

    def create_database(self):
        """Call the elements to create the database and to retrieve the data to fill it."""

        # build the database skeleton
        self.entity_manager.db.build_database()

        # call the API
        self.api_manager.get_load()

        # download the data (from the API to the DB)
        self.api_manager.download_data(self.entity_manager)

    def new_session(self):
        """Call the elements to start the program"""

        self.view.text_introduction()
        self.action_triage()

    def action_call(self, *args):
        """Ask for an action to the user, and treat its command.

        Verify which command was sent by the user, and call the related methods.
        """

        # print the text describing the step and the commands common to every step
        self.view.actions_explanation()
        self.view.action_closing()  # 'X'
        if self.phase == 1:  # opening step
            self.view.action_renew_db()  # '0'
        else:
            self.view.action_backstep()  # '0'

        # print the actions specific to the current step
        if self.phase == self.steps['opening']:  # 1-2 commands
            # 1. opening step
            self.view.action_opening()

        elif self.phase == self.steps['category']:  # n commands
            # 2. category step
            self.view.display_category(*args)

        elif self.phase == self.steps['product']:  # n commands
            # 3. product step
            self.view.display_product(*args)

        elif self.phase == self.steps['substitute']:  # n commands
            # 4. substitute step
            self.view.display_result(*args)
            self.view.action_substitute()

        elif self.phase == self.steps['saving']:  # 1-2 commands
            # 5. saving step
            self.view.action_saving()
            self.view.display_result(*args)

        elif self.phase == self.steps['favorite']:  # no specific commands for this step
            # 6. favorite step
            self.view.display_result(*args)

        # get the input from the user
        self.choice = None
        self.choice = self.view.input_request()
        return self.choice

    def action_triage(self, *args):
        """Orchestrate the flow of the program, by selecting the next methods to call.

        The methods are chosen in function
        of the current phase of the program
        and the command sent by the user.
        """

        # x. closing step
        if self.phase == self.steps['closing'] or (type(self.choice) is str and self.choice.lower() == 'x'):
            self.view.text_closing()
            exit()  # or something like this to close the program

        # 1. opening step
        elif self.phase == self.steps['opening']:

            self.action_call()

            # recreate the db
            if self.choice == 0:
                # TODO: method to create the new db, to be tested in the flow
                self.create_database()
                self.action_triage()

            # toward category step
            elif self.choice == 1:
                self.phase = self.steps['category']
                self.action_triage()

            # toward favorite step
            elif self.choice == 2:
                self.phase = self.steps['favorite']
                self.action_triage()

            # flag input failure
            else:
                self.view.input_failure()
                self.action_call()  # args = [products from favorite]
                self.action_triage()

        # 2. category step
        elif self.phase == self.steps['category']:

            # TODO: fetch a list of instances with all the categories in the table 'category'
            argus_category = self.entity_manager.select_row(table_anchor='category', selection=['id_category', 'name'])
            self.action_call(*args)  # args = [categories]

            # rollback to the previous step
            if self.choice == 0:
                self.phase -= 1
                self.action_triage(*args)

            # pick a category
            elif self.choice in 'id_categories_list':
                # id_categories_list -> with the ids of the categories in the list
                self.phase = self.steps['product']
                # TODO: how to pass the selected id_category in the next segment of the loop ?
                self.action_triage(*args)  # args = selected id_category

            # flag input failure
            else:
                self.view.input_failure()
                self.action_triage()

        # 3. product step
        elif self.phase == self.steps['product']:

            # TODO: fetch a list of instances with all the products in the table 'product' for the selected category
            self.action_call(*args)  # args = [products from one category]

            # rollback to the previous step
            if self.choice == 0:
                self.phase -= 1
                self.action_triage(*args)

            # pick a product
            elif self.choice in 'id_products_list':
                # id_products_list -> with the ids of the products in the list
                self.phase = self.steps['substitute']
                # TODO: how to pass the selected id_product in the next segment of the loop ?
                self.action_triage(*args)  # args = selected base id_product

            # flag input failure
            else:
                self.view.input_failure()
                self.action_triage(*args)  # args = [categories]

        # 4. substitute step
        elif self.phase == self.steps['substitute']:

            # TODO: fetch a list of instances with all the products in the table 'product' with at least one category in common with the selected product
            self.action_call(*args)  # args = [substitutes to the base product]

            # rollback to the previous step
            if self.choice == 0:
                self.phase -= 1
                self.action_triage(*args)

            # pick a substitute
            elif self.choice in 'id_substitutes_list':
                # id_substitutes_list -> with the ids of the substitutes in the list
                self.phase = self.steps['saving']
                # TODO: how to pass the selected id_substitute in the next segment of the loop ?
                self.action_triage(*args)  # args = selected substitute id_product

            # flag input failure
            else:
                self.view.input_failure()
                self.action_triage(*args)  # args = selected base id_product

        # 5. saving step
        elif self.phase == self.steps['saving']:

            # display the result and propose to save it in the favorites
            self.action_call(*args)  # args = selected substitute id_product

            # rollback to the previous step
            if self.choice == 0:
                self.phase -= 1
                self.action_triage(*args)

            # return to the main menu
            elif self.choice == 1:
                self.phase = self.steps['opening']
                self.action_triage()

            # save the substitute
            elif self.choice == 2:
                # TODO: update the table 'favorite' by adding the selected substitute id_product
                self.phase = self.steps['favorite']
                self.action_triage()

            # flag input failure
            else:
                self.view.input_failure()
                self.action_triage(*args)  # args = selected substitute id_product

        # 6. favorite step
        elif self.phase == self.steps['favorite']:

            # TODO: fetch a list of instances with all the products in the table 'favorite'
            self.action_call(*args)  # args = [products from favorite]

            # return to the main menu
            if self.choice == 0:
                self.phase = self.steps['opening']
                self.action_triage()

            # flag input failure
            else:
                self.view.input_failure()
                self.action_triage()

        # # rollback
        # if self.choice == 0:
        #
        #     # recreate the db
        #     if self.phase == self.steps['opening']:
        #         self.choice = None
        #         # recreate the db  ==> controller needs to have access to a manager
        #         self.action_triage()
        #
        #     # return to the main menu
        #     if self.phase == self.steps['favorite']:
        #         self.choice = None
        #         self.phase = self.steps['opening']
        #         self.action_triage()
        #
        #     # return to the previous step
        #     else:
        #         self.choice = None
        #         self.phase -= 1
        #         self.action_triage(*args)
