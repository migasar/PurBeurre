"""Manage the display of the program on the terminal."""


class CLIView:
    """Regroup methods to display elements of the program on a terminal."""

    # Input command
    @staticmethod
    def input_request():
        """Display the input to receive the command from the user."""

        command = input("Entrez le numéro de la prochaine action : ")
        print()

        return command

    @staticmethod
    def input_failure():
        """Display a text explaining to the user that its command didn't work,

        and offer him to try again.
        """
        print("Désolé, nous ne comprenons pas votre commande. ")

    # Descriptions
    @staticmethod
    def text_introduction():
        """Display a text explaining the purpose of the program."""
        print("""
--------------------------------------
Bienvenue sur l'application Pur Beurre
--------------------------------------

Pour vous aider à améliorer votre alimentation, 
nous allons essayer de vous proposer
un substitut plus sain à l'aliment que vous nous indiquerez.
""")

    @staticmethod
    def text_closing():
        """Display an anouncement indicating that the program is closing."""
        print("Merci d'avoir utilisé notre programme.")

    @staticmethod
    def text_new_db():
        """Display an anouncement indicating that the program is closing."""
        print("La base de donnée est relancée.")

    @staticmethod
    def text_category():
        """Display a text demanding to the user to choose a category."""
        print("Sélectionnez la catégorie.")

    @staticmethod
    def text_product():
        """Display a text demanding to the user to choose a product."""
        print("Sélectionnez un aliment.")

    @staticmethod
    def text_substitute():
        """Display the possibility to select one of the substitutes."""
        print("Sélectionnez le substitut qui vous intéresse. ")

    @staticmethod
    def text_no_favorite():
        """Display a text announcing that no product have been saved so far."""
        print("Vous n'avez pas encore sauvegardé d'aliments.")

    @staticmethod
    def commands_explanation():
        """Display the actions available to the user."""
        print("Pour choisir une action, indiquez son numéro.")

    # Commands for sidesteps
    @staticmethod
    def command_closing():
        """Display the command used to end the program."""
        print("X. Quitter le programme. ")

    @staticmethod
    def command_renew_db():
        """Display the command used to recreate the database."""
        print("0. Reconstruire la base de données. ")

    @staticmethod
    def command_backstep():
        """Display the commands used to return to the previous step."""
        print("0. Revenir à l'étape précédente. ")

    @staticmethod
    def command_newstep():
        """Display the commands used to return to the previous step."""
        print("0. Revenir au menu principal. ")

    # Commands pre-defined
    @staticmethod
    def command_opening():
        """Display the commands available to the user."""
        print("1. Quel aliment souhaitez-vous remplacer ? ")
        print("2. Retrouver vos alments substitués. ")

    @staticmethod
    def command_saving():
        """Display the option to save a substitute as favorite."""
        print("1. Revenir au menu principal. ")
        print("2. Sauvegarder cet aliment dans vos favoris. ")

    # Commands from selection
    @staticmethod
    def display_category(roster):
        """Display all the categories in the database."""

        for category in roster:
            print(f"{category.id_category}. {category.name} ")

    @staticmethod
    def display_product(roster):
        """Display the products associated to a variable.

        It can be all the products inside the selected category,
        or it can be all the substitutes of a specific product.
        """

        for product in roster:
            print(
                f"{product.id_product}. {product.name} - {product.nutriscore}"
            )

    @staticmethod
    def display_substitute(roster):
        """Display the product selected as substitute."""

        for product in roster:
            print(f"- {product.name} :")
            print(f"    nutriscore : {product.nutriscore}")
            print(f"    url : {product.url}")

    @staticmethod
    def display_favorite(roster):
        """Display the products saved as favorites by the user."""

        for product in roster:
            print(f"- {product.name} :")
            print(f"    nutriscore : {product.nutriscore}")
            print(f"    url : {product.url}")
            print(f"    catégories : {product.category}")
            print(f"    magasins : {product.store}")
            print()

    @staticmethod
    def display_result(roster):
        """Display the result from a list of instances."""

        # headers
        headers = [
                (key.capitalize()).center(20)
                for (key, value)
                in roster[0].get_items() if 'id' not in key
        ]
        headers.insert(0, 'Number'.center(20))

        # results
        results = [
                [
                        str(value).center(20)
                        for (key, value)
                        in entity.get_items() if 'id' not in key
                ] for entity in roster
        ]

        count = 0
        for result in results:
            count += 1
            result.insert(0, str(count).center(20))

        # table lines
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
