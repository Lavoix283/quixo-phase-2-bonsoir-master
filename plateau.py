"""Module Plateau

Classes:
    * Plateau - Classe principale du plateau de jeu Quixo.
"""

from copy import deepcopy
from quixo_error import QuixoError


class Plateau:
    """
    Classe représentant le plateau de jeu Quixo.
    
    Elle permet de manipuler le plateau en insérant des cubes, récupérant l'état du plateau et vérifiant les positions des cubes.
    """

    def __init__(self, plateau=None):
        """Constructeur de la classe Plateau

        Vous ne devez rien modifier dans cette méthode.

        Args:
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.plateau = self.générer_le_plateau(deepcopy(plateau))

    def état_plateau(self):
        """Retourne une copie du plateau

        Retourne une copie du plateau pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            list[list[str]]: La représentation du plateau
            tel que retourné par le serveur de jeu.
        """
        return deepcopy(self.plateau)

    def __str__(self):
        """Retourne une représentation du plateau sous forme de chaîne de caractères."""
        lignes = []

        for i in range(5):
            ligne = f"{i + 1} | " + " | ".join(self.plateau[i]) + " |"
            lignes.append(ligne)

            if i < 4:
                lignes.append("  |---|---|---|---|---|")

        lignes.append("   -------------------")
        lignes.append("  | 1   2   3   4   5 |")

        return "\n".join(lignes)

    def __getitem__(self, position):
        """Récupère la valeur à la position spécifiée sur le plateau.

        Args:
            position (tuple): Coordonnées (x, y) de la position sur le plateau.

        Returns:
            str: La valeur à la position spécifiée sur le plateau.

        Raises:
            QuixoError: Si les coordonnées sont en dehors de la plage valide.
        """
        x, y = position

        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        return self.plateau[x - 1][y - 1]

    def __setitem__(self, position, valeur):
        """Modifie la valeur à la position spécifiée sur le plateau.

        Args:
            position (tuple): Coordonnées (x, y) de la position sur le plateau.
            valeur (str): La nouvelle valeur à insérer.

        Raises:
            QuixoError: Si les coordonnées sont en dehors de la plage valide ou la valeur est invalide.
        """
        x, y = position

        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        if valeur not in ["X", "O", " "]:
            raise QuixoError("Valeur du cube invalide.")

        self.plateau[x - 1][y - 1] = valeur

    def générer_le_plateau(self, plateau):
        """Génère le plateau en vérifiant la validité de sa structure.

        Args:
            plateau (list[list[str]] or None): La représentation du plateau ou None.

        Returns:
            list[list[str]]: Le plateau généré ou un plateau vide.

        Raises:
            QuixoError: Si le format du plateau est invalide.
        """
        if plateau is None:
            return [[" " for _ in range(5)] for _ in range(5)]

        if len(plateau) != 5 or any(len(ligne) != 5 for ligne in plateau):
            raise QuixoError("Format du plateau invalide.")

        for ligne in plateau:
            for valeur in ligne:
                if valeur not in ["X", "O", " "]:
                    raise QuixoError("Valeur du cube invalide.")

        return plateau

    def insérer_un_cube(self, cube, origine, direction):
        """Insère un cube sur le plateau selon la direction donnée.

        Args:
            cube (str): Le cube à insérer, soit "X" soit "O".
            origine (tuple): Les coordonnées (x, y) du cube à insérer.
            direction (str): La direction de l'insertion, soit "haut", "bas", "gauche" ou "droite".

        Raises:
            QuixoError: Si la direction est invalide.
        """
        if cube not in ["X", "O"]:
            raise QuixoError("Le cube à insérer ne peut pas être vide.")

        if direction not in ["haut", "bas", "gauche", "droite"]:
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

        if direction == "bas":
            self.insérer_par_le_bas(cube, origine)
        elif direction == "haut":
            self.insérer_par_le_haut(cube, origine)
        elif direction == "gauche":
            self.insérer_par_la_gauche(cube, origine)
        elif direction == "droite":
            self.insérer_par_la_droite(cube, origine)

    def insérer_par_le_bas(self, cube, origine):
        """Insère un cube dans le plateau en partant du bas.

        Args:
            cube (str): Le cube à insérer.
            origine (tuple): Les coordonnées (x, y) de l'emplacement du cube.

        Raises:
            QuixoError: Si les coordonnées sont en dehors de la plage valide.
        """
        x, y = origine
        if x < 1 or x > 5 or y < 1 or y > 5:
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        for i in range(4, 0, -1):
            self[x - 1, i] = self[x - 1, i - 1]

        self[x - 1, 0] = cube

    def insérer_par_le_haut(self, cube, origine):
        """Insère un cube dans le plateau en partant du haut.

        Args:
            cube (str): Le cube à insérer.
            origine (tuple): Les coordonnées (x, y) de l'emplacement du cube.

        Raises:
            QuixoError: Si les coordonnées sont en dehors de la plage valide.
        """
        x, y = origine
        if x < 1 or x > 5 or y < 1 or y > 5:
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        for i in range(1, 5):
            self[x - 1, i - 1] = self[x - 1, i]

        self[x - 1, 4] = cube

    def insérer_par_la_gauche(self, cube, origine):
        """Insère un cube dans le plateau en partant de la gauche.

        Args:
            cube (str): Le cube à insérer.
            origine (tuple): Les coordonnées (x, y) de l'emplacement du cube.

        Raises:
            QuixoError: Si les coordonnées sont en dehors de la plage valide.
        """
        x, y = origine
        if x < 1 or x > 5 or y < 1 or y > 5:
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        for i in range(1, 5):
            self[i - 1, y - 1] = self[i, y - 1]

        self[4, y - 1] = cube

    def insérer_par_la_droite(self, cube, origine):
        """Insère un cube dans la colonne spécifiée de droite à gauche dans le plateau de jeu.

        Args:
            cube (str): Le cube à insérer.
            origine (tuple): Les coordonnées (x, y) de l'emplacement où le cube doit être inséré.

        Raises:
            QuixoError: Si les coordonnées (x, y) ne sont pas dans la plage valide [1, 5].
        """
        x, y = origine
        if x < 1 or x > 5 or y < 1 or y > 5:
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        for i in range(4, 0, -1):
            self[i, y - 1] = self[i - 1, y - 1]

        self[0, y - 1] = cube

plateau = Plateau()