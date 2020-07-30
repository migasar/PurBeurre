"""Manage the display of the program on the terminal."""


class CLIView:
    """Regroup methods to display elements of the program on a terminal."""

    # Input command
    @staticmethod
    def action_input():
        """Display the input to receive the command from the user."""

        command = input("Entrez le numéro de la prochaine action : ")

        return command

    @staticmethod
    def action_input_failure():
        """Display a text explaining to the user that its command didn't work, and inviting him to try again."""

        print("Désolé, nous ne comprenons pas votre commande. ")

    # Descriptions
    @staticmethod
    def introduction():
        """Display a text explaining the purpose of the program."""

        print("""
--------------------------------------
Bienvenue sur l'application Pur Beurre
--------------------------------------

Pour vous aider à améliorer votre alimentation, nous allons essayer de vous proposer 
un substitut plus sain à l'aliment que vous nous indiquerez. 
""")

    @staticmethod
    def close_program():
        """Display an anouncement indicating that the program is closing."""

        print("Merci d'avoir utilisé notre programme. ")

    @staticmethod
    def actions_explanation():
        """Display the actions available to the user."""

        print("Pour choisir une action, veuillez indiquer son numéro. ")

    # Actions options
    @staticmethod
    def action_close():
        """Display the command used to end the program. """

        print("x. Quitter le programme. ")

    @staticmethod
    def action_backstep():
        """Display the command used to return to the previous step."""

        print("0. Revenir à l'étape précédente. ")

    @staticmethod
    def actions_opening():
        """Display the commands available to the user."""

        print("1. Quel aliment souhaitez-vous remplacer ? ")
        print("2. Retrouver vos alments substitués. ")

    @staticmethod
    def actions_on_category(*args):
        """Display all the categories in the database."""

        for category in args:
            print(f"{category['id_category']}. {category['name']} ")

    @staticmethod
    def actions_on_product(*args):
        """Display the products associated to a variable.

        It can be all the products inside the selected category,
        or it can be all the substitutes of a specific product.
        """

        for product in args:
            print(f"{product['id_product']}. {product['name']} - {product['nutriscore']} - {product['url']}")

    @staticmethod
    def actions_on_substitute(*args):
        """Display the selectd substitute and the option to save is as favorite."""

        for product in args:
            print(f"{product['id_product']}. {product['name']} - {product['nutriscore']} - {product['url']}")

        print("1. Revenir au menu principal. ")
        print("2. Sauvegarder cet aliment dans vos favoris. ")

    @staticmethod
    def display_favorite(*args):
        """Display the products saved as favorites by the user."""

        for product in args:
            print(f"{product['id_product']}. {product['name']} - {product['nutriscore']} - {product['url']}")

    @staticmethod
    def display_result(*args):
        """Display the result from a query."""

        for argument in args:

            # headers
            headers = [(head.capitalize()).center(20) for head in argument[0].keys()]
            headers.insert(0, 'Number'.center(10))

            # results
            results = [[str(a).center(20) for a in arg.values()] for arg in argument]
            count = 0
            for result in results:
                count += 1
                result.insert(0, str(count).center(10))

            # lines
            s1 = [('=' * 20) for _ in range(len(headers))]
            s2 = '+'
            separation_line = s2.join(s1)
            table_line = '-' * len(separation_line)

            # prints
            print(table_line)
            print('|'.join(headers))
            print(separation_line)
            for result in results:
                print('|'.join(result))
            print(table_line)
