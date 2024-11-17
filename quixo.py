"""Module Quixo

Classes:
    * Quixo - Classe principale du jeu Quixo.
    * QuixoError - Classe d'erreur pour le jeu Quixo.

Functions:
    * interpréter_la_commande - Génère un interpréteur de commande.
"""

import argparse

from quixo_error import QuixoError

from plateau import Plateau


class Quixo:
    def __init__(self, joueurs, plateau=None) -> None:
        """Constructeur de la classe Quixo

        Vous ne devez rien modifier dans cette méthode.

        Args:
            joueurs (list[str]): La liste des deux joueurs.
                Le premier joueur possède le symbole "X" et le deuxième "O".
            plateau (list[list[str]], optional): La représentation du plateau
                tel que retourné par le serveur de jeu ou la valeur None par défaut.
        """
        self.joueurs = joueurs
        self.plateau = Plateau(plateau)

    def état_partie(self):
        """Retourne une copie du jeu

        Retourne une copie du jeu pour éviter les effets de bord.
        Vous ne devez rien modifier dans cette méthode.

        Returns:
            dict: La représentation du jeu tel que retourné par le serveur de jeu.
        """
        return {
            "joueurs": self.joueurs,
            "plateau": self.plateau.état_plateau(),
        }

    def __str__(self):
        joueur_X, joueur_O = self.joueurs
        legende = f"Légende:\n   X={joueur_X}\n   O={joueur_O}"

        lignes = []
        lignes.append("   -------------------")

        for i in range(5):
            ligne = f"{i + 1} | " + " | ".join(self.plateau[i]) + " |"
            lignes.append(ligne)

            if i < 4:
                lignes.append("  |---|---|---|---|---|")

        lignes.append("   -------------------")
        lignes.append("    1   2   3   4   5   ")

        return f"{legende}\n{''.join(lignes)}"


    def déplacer_pion(self, pion, origine, direction):
        if pion not in ["X", "O"]:
            raise QuixoError(f"Le pion '{pion}' n'est pas valide. Il doit être 'X' ou 'O'.")

        x, y = origine
        if not (1 <= x <= 5 and 1 <= y <= 5):
            raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

        if direction not in ["haut", "bas", "gauche", "droite"]:
            raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

        self.plateau.insérer_un_cube(pion, origine, direction)


    def choisir_un_coup():
        while True:
            try:
                position_str = input("Donnez la position d'origine du cube (x,y) : ")
                origine = [int(coord) for coord in position_str.split(",")]

                if not (1 <= origine[0] <= 5 and 1 <= origine[1] <= 5):
                    raise QuixoError("Les positions x et y doivent être entre 1 et 5 inclusivement.")

                direction = input("Quelle direction voulez-vous insérer? ('haut', 'bas', 'gauche', 'droite') : ").lower()

                if direction not in ["haut", "bas", "gauche", "droite"]:
                    raise QuixoError("La direction doit être 'haut', 'bas', 'gauche' ou 'droite'.")

                return origine, direction
        
            except ValueError:
                print("Erreur : veuillez entrer des coordonnées valides au format x,y (par exemple, 2,3).")
            except QuixoError as e:
                print(e)


def interpréter_la_commande():
    parser = argparse.ArgumentParser()

    parser.add_argument('idul', type=str, help="L'idul du joueur")

    parser.add_argument('--parties', action='store_true', help="Indique si on doit afficher les parties en cours")

    return parser.parse_args()
