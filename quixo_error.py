# quixo_error.py

class QuixoError(Exception):
    def __init__(self, message="Une erreur s'est produite dans le jeu Quixo"):
        super().__init__(message)
