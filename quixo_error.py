"""Module définissant les erreurs spécifiques au jeu Quixo.

Ce module contient des classes d'erreur personnalisées pour le jeu Quixo.
"""

class QuixoError(Exception):
    """Classe d'erreur personnalisée pour le jeu Quixo.

    Cette classe hérite de la classe Exception et permet de lever des erreurs spécifiques
    au jeu Quixo, avec un message d'erreur par défaut.
    """

    def __init__(self, message="Une erreur s'est produite dans le jeu Quixo"):
        """Initialise l'erreur avec un message spécifique.

        Args:
            message (str, optional): Le message d'erreur à afficher. Par défaut, un message générique est utilisé.
        """
        super().__init__(message)
