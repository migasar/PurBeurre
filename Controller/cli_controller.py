"""Manage the flow of the program, and the interactions of its components."""

from Model.Manager.entity_manager import EntityManager
from View.cli_view import CLIView


class CLIController:
    """Pilot the flow of the program.

    It orchestrate the interactions between the main elements of the program:
     - the models
     - the views
     - the input of the user
    """

    # Class variable:
    steps = {
            'opening': 1,
            'category': 2,
            'product': 3,
            'substitute': 4,
            'favorite': 5,
            'closing': 99
    }
    # register of all the possible phases in the flow of the program

    def __init__(self):

        self.entity_manager = EntityManager()
        self.view = CLIView()
        self.choice = None  # user input
        self.phase = self.steps['opening']  # the actual phase in the flow of the program

    def new_session(self):
        """Call the elements to start the program"""

        self.view.introduction()
        self.action_call()
        self.action_triage()

    def action_call(self, *args):
        """Ask for an action to the user, and treat its command.

        Verify which command was sent by the user, and call the related methods.
        """

        # register of action methods specific to each phase of the program
        step_method = {
                1: self.view.actions_opening(),
                2: self.view.actions_on_category(*args),
                3: self.view.actions_on_product(*args),
                4: self.view.actions_on_substitute(*args),
                5: self.view.display_favorite(*args),
                6: self.view.display_result(*args),
                99: ''
        }

        # print the text for this step and call for the next action
        self.view.actions_explanation()
        self.view.action_close()

        # call the methods for the actions of this phase of the program
        if self.phase != self.steps['opening']:
            self.view.action_backstep()
        print(step_method[self.phase])

        # get the input of the user
        self.choice = self.view.action_input()

        return self.choice

    def action_triage(self, *args):
        """Orchestrate the flow of the program, by selecting the next methods to call.

        The methods are chosen in function
        of the actual phase of the program
        and the command sent by the user.
        """

        # opening step
        if self.phase == self.steps['opening']:

            # categories step
            if self.choice == 1:
                self.phase = self.steps['category']
                self.action_call(*args)
                self.action_triage(*args)

            # favorites step
            elif self.choice == 2:
                self.phase = self.steps['favorite']
                self.action_call(*args)
                self.action_triage(*args)

            # flag input failure
            else:
                self.view.action_input_failure()
                self.action_call()
                self.action_triage()

        # products step
        elif self.phase == self.steps['category']:

            if self.choice == 0:
                # rollback
                pass

            elif self.choice in 'id_products_list':  # id_products_list -> needs to be defined
                self.phase = self.steps['product']
                self.action_call(*args)
                self.action_triage(*args)

            # flag input failure
            else:
                self.view.action_input_failure()
                self.action_call()
                self.action_triage()

        # substitutes step
        elif self.phase == self.steps['product']:

            if self.choice == 0:
                # rollback
                pass

            elif self.choice in 'id_substitutes_list':  # id_products_list -> needs to be defined
                self.phase = self.steps['substitute']
                self.action_call(*args)
                self.action_triage(*args)

            else:  # flag input failure
                self.view.action_input_failure()
                self.action_call()
                self.action_triage()

        # saving step
        elif self.phase == self.steps['substitute']:

            if self.choice == 0:
                # rollback
                pass

            elif self.choice.lower() == 'y':
                self.phase = self.steps['saving']
                self.action_call(*args)
                self.action_triage(*args)

            else:  # flag input failure
                self.view.action_input_failure()
                self.action_call()
                self.action_triage()

        # closing step
        if self.phase == self.steps['closing'] or (type(self.choice) is str and self.choice.lower() == 'x'):
            self.view.close_program()
            exit()  # or something like this to close the program
