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

    # Class variable (register of all the phases in the flow of the program):
    steps = {
            'closing': 0,
            'opening': 1,
            'category': 2,
            'product': 3,
            'substitute': 4,
            'saving': 5,
            'favorite': 6
    }

    def __init__(self):

        self.entity_manager = EntityManager()
        self.api_manager = APIManager()
        self.view = CLIView()

        self.phase = self.steps['opening']  # the actual phase in the program
        self.input = None  # user input
        self.choices = {
                'catalog_category': [],
                'opt_category': [],
                'roster_product': [],
                'opt_product': [],
                'roster_substitute': [],
                'opt_substitute': [],
                'roster_favorite': []
        }  # results based on user input

    # structure
    def create_database(self):
        """Call the elements to create the database,

        and to retrieve the data to fill it.
        """

        # build the database skeleton
        self.entity_manager.db.build_database()

        # call the API
        self.api_manager.get_load()

        # download the data (from the API to the DB)
        self.api_manager.download_data(self.entity_manager)

    def fulfill_database(self):
        """Replenish the db if it is empty."""

        # interrogate the db to see if it is empty
        production = [
            p for p in self.entity_manager.select_row(
                table_anchor='product',
                selection=['id_product', 'name']
            )
        ]

        # replenish the db
        if not production:
            # call the API
            self.api_manager.get_load()
            # download the data (from the API to the DB)
            self.api_manager.download_data(self.entity_manager)

    def new_session(self):
        """Call the elements to start the program"""

        self.fulfill_database()
        self.view.text_introduction()
        self.action_triage()

    # flow
    def action_call(self):
        """Ask for an action to the user, and treat its command.

        Verify which command was sent by the user, and call its methods.
        """

        # print the text describing the step
        self.view.commands_explanation()

        # 1. opening step
        if self.phase == self.steps['opening']:
            self.view.command_closing()  # 'X' command
            self.view.command_renew_db()  # '0' command
            self.view.command_opening()  # 1-2 commands

        # 2. category step
        elif self.phase == self.steps['category']:
            self.view.text_category()
            self.view.command_closing()  # 'X' command
            self.view.command_backstep()  # '0' command
            self.view.display_category(self.choices['catalog_category'])  # n commands

        # 3. product step
        elif self.phase == self.steps['product']:
            self.view.text_product()
            self.view.command_closing()  # 'X' command
            self.view.command_backstep()  # '0' command
            self.view.display_product(self.choices['roster_product'])  # n commands

        # 4. substitute step
        elif self.phase == self.steps['substitute']:
            self.view.text_substitute()
            self.view.command_closing()  # 'X' command
            self.view.command_backstep()  # '0' command
            self.view.display_product(self.choices['roster_substitute'])  # n commands

        # 5. saving step
        elif self.phase == self.steps['saving']:
            self.view.command_closing()  # 'X' command
            self.view.command_backstep()  # '0' command
            self.view.command_saving()  # 1-2 commands
            self.view.display_substitute(self.choices['opt_substitute'])

        # 6. favorite step
        elif self.phase == self.steps['favorite']:
            self.view.command_closing()  # 'X' command
            self.view.command_newstep()  # '0' command
            self.view.display_favorite(self.choices['roster_favorite'])

        # get the input from the user and test if it is a valid option
        self.input = None
        self.input = self.view.input_request()

        self.check_input()

        # flag input failure
        if self.input is None:
            self.view.input_failure()
            return self.action_triage()
        else:
            return self.input

    def action_triage(self):
        """Orchestrate the flow of the program.

        It selects the next methods to call.
        The methods are chosen in function
        of the current phase of the program
        and the command sent by the user.
        """

        # 0. closing step:
        if self.phase == self.steps['closing']:
            self.step_closing()

        # 1. opening step
        elif self.phase == self.steps['opening']:
            self.step_opening()

        # 2. category step
        elif self.phase == self.steps['category']:
            self.step_category()

        # 3. product step
        elif self.phase == self.steps['product']:
            self.step_product()

        # 4. substitute step
        elif self.phase == self.steps['substitute']:
            self.step_substitute()

        # 5. saving step
        elif self.phase == self.steps['saving']:
            self.step_saving()

        # 6. favorite step
        elif self.phase == self.steps['favorite']:
            self.step_favorite()

    # input
    def check_input(self):

        if type(self.input) is str:

            try:
                # check if the input can be coerced in an integer
                int(self.input)

            except ValueError:
                # check if the input is the closure command
                if self.input.lower() == 'x':
                    # close the program
                    self.phase = self.steps['closing']
                    self.action_triage()

                # concludes that the input is a wrong command
                else:
                    self.input = None

            else:
                # coerce the input in an integer if possible
                self.input = int(self.input)

        else:
            # concludes that the input is of the wrong type
            self.input = None

        return self.input

    def clear_choices(self):
        """Restore the default values in the dictionnary self.choices"""

        for key, value in self.choices.items():
            self.choices[key] = []

        return self.choices

    # steps
    def step_closing(self):

        # announce the end of the program and close it
        self.view.text_closing()
        exit()

    def step_opening(self):

        # reset the dictionnary self.choices
        self.clear_choices()

        # call the user input for this step
        self.action_call()

        # recreate the db
        if self.input == 0:
            self.view.text_new_db()
            self.create_database()
            self.action_triage()

        # go to category step
        elif self.input == 1:
            self.phase = self.steps['category']
            self.action_triage()

        # go to favorite step
        elif self.input == 2:
            self.phase = self.steps['favorite']
            self.action_triage()

        # flag input failure
        else:
            self.view.input_failure()
            return self.action_triage()

    def step_category(self):

        # interrogate the db to get a list of all the categories
        claims_category = {
                'order': 'id_category'
        }
        self.choices['catalog_category'] = self.entity_manager.select_row(
            table_anchor='category',
            selection=['id_category', 'name'],
            **claims_category
        )

        # create a list of id numbers to test if the input is an error
        register_id_category = [
                c.id_category for c in self.choices['catalog_category']
        ]

        # display the categories and propose to select one
        self.action_call()

        # rollback to the previous step
        if self.input == 0:
            self.phase -= 1
            self.action_triage()

        # pick a category and go to product step
        elif self.input in register_id_category:

            for cat in self.choices['catalog_category']:
                if self.input == cat.id_category:
                    self.choices['opt_category'].append(cat)

            self.phase = self.steps['product']
            self.action_triage()

        # flag input failure
        else:
            self.view.input_failure()
            return self.action_triage()

    def step_product(self):

        # interrogate the db to get the products in the category
        claims_product = {
                'order': 'id_product',
                'join': {
                        'table_adjunct': 'category_product',
                        'row_key_adjunct': 'id_product',
                        'row_key_anchor': 'id_product'
                },
                'where': {
                        'table_adjunct': 'category_product',
                        'row_key': 'id_category',
                        'row_value': self.choices['opt_category'][0].id_category
                }
        }

        self.choices['roster_product'] = self.entity_manager.select_row(
            table_anchor='product',
            selection=['id_product', 'name', 'nutriscore', 'url'],
            **claims_product
        )

        # create a list of id numbers to test if the input is an error
        register_id_product = [
                p.id_product for p in self.choices['roster_product']
        ]

        # display the products and propose to select one
        self.action_call()

        # rollback to the previous step
        if self.input == 0:
            self.phase -= 1
            self.action_triage()

        # pick a product and go to substitute step
        elif self.input in register_id_product:

            for prod in self.choices['roster_product']:
                if self.input == prod.id_product:
                    self.choices['opt_product'].append(prod)

            self.phase = self.steps['substitute']
            self.action_triage()

        # flag input failure
        else:
            self.view.input_failure()
            return self.action_triage()

    def step_substitute(self):
        """Interrogate the db to get a list of all the substitutes
        of the selected product
        by getting the products sharing at least one category.
        """

        # get all the categories of the selected product
        claims_roster_cat = {
                'order': 'id_category',
                'join': {
                        'table_adjunct': 'category_product',
                        'row_key_adjunct': 'id_category',
                        'row_key_anchor': 'id_category'
                },
                'where': {
                        'table_adjunct': 'category_product',
                        'row_key': 'id_product',
                        'row_value': self.choices['opt_product'][0].id_product
                }
        }
        roster_category = self.entity_manager.select_row(
                table_anchor='category',
                selection=['id_category', 'name'],
                **claims_roster_cat
        )

        # create a list of id numbers to use as value for the next method
        register_id_roster_cat = [r.id_category for r in roster_category]

        # get all the products of the roster of categories
        claims_substitute = {
                'order': 'id_product',
                'join': {
                        'table_adjunct': 'category_product',
                        'row_key_adjunct': 'id_product',
                        'row_key_anchor': 'id_product'
                },
                'where': {
                        'table_adjunct': 'category_product',
                        'row_key': 'id_category',
                        'row_value': register_id_roster_cat
                }
        }
        self.choices['roster_substitute'] = self.entity_manager.select_row(
                table_anchor='product',
                selection=['id_product', 'name', 'nutriscore', 'url'],
                **claims_substitute
        )

        # create a list of id numbers to test if the input is an error
        register_id_substit = [
                s.id_product for s in self.choices['roster_substitute']
        ]

        # display the substitutes and propose to select one
        self.action_call()

        # rollback to the previous step
        if self.input == 0:
            self.phase -= 1
            self.action_triage()

        # pick a substitute and go to saving step
        elif self.input in register_id_substit:

            for sub in self.choices['roster_substitute']:
                if self.input == sub.id_product:
                    self.choices['opt_substitute'].append(sub)

            self.phase = self.steps['saving']
            self.action_triage()

        # flag input failure
        else:
            self.view.input_failure()
            return self.action_triage()

    def step_saving(self):

        # get an instance of the selected product

        # display the result and offer to save it in the favorites
        self.action_call()

        # rollback to the previous step
        if self.input == 0:
            self.phase -= 1
            self.action_triage()

        # return to the main menu
        elif self.input == 1:
            self.phase = self.steps['opening']
            self.action_triage()

        # save the substitute and go to favorite step
        elif self.input == 2:
            self.entity_manager.insert_row(
                    table_anchor='favorite_product',
                    row_keys=['id_base_product', 'id_substitute_product'],
                    row_values=[
                        self.choices['opt_product'][0].id_product,
                        self.choices['opt_substitute'][0].id_product
                    ]
            )

            self.phase = self.steps['favorite']
            self.action_triage()

        # flag input failure
        else:
            self.view.input_failure()
            return self.action_triage()

    def step_favorite(self):

        # self.choices['roster_favorite'] = [
        #     fav for fav in self.entity_manager.select_row(
        #         table_anchor='favorite_product',
        #         selection=['id_substitute_product']
        #     )
        # ]

        # interrogate the db to get the id of the favorites
        roster_id_fav = [
            fav for fav in self.entity_manager.select_row(
                table_anchor='favorite_product',
                selection=['id_substitute_product']
            )
        ]
        register_id_roster_fav = [r.id_product for r in roster_id_fav]

        # test if there is no favorite yet
        if not register_id_roster_fav:

            self.view.text_no_favorite()
            self.phase = self.steps['opening']
            self.action_triage()

        else:
            # interrogate the db to get the instances of the favorites
            claims_favorite = {
                'order': 'id_product',
                'where': {
                    'table_adjunct': 'product',
                    'row_key': 'id_product',
                    'row_value': register_id_roster_fav
                }
            }
            self.choices['roster_favorite'] = self.entity_manager.select_row(
                table_anchor='product',
                selection=['id_product', 'name', 'nutriscore', 'url'],
                **claims_favorite
            )

        # display the substitutes saved as favorites
        self.action_call()

        # return to the main menu
        if self.input == 0:
            self.phase = self.steps['opening']
            self.action_triage()

        # flag input failure
        else:
            self.view.input_failure()
            return self.action_triage()
