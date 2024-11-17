"""
Module pour interagir avec l'API Quixo.

Ce module contient des fonctions permettant d'interagir avec l'API de jeu Quixo. 
Les fonctions incluent l'initialisation d'une partie, le jeu d'un coup, et 
la récupération des informations d'une partie.
"""

import requests

URL = "https://pax.ulaval.ca/quixo/api/a24/"

def initialiser_partie(idul, secret):
    """Initialise une nouvelle partie en envoyant une requête POST à l'API Quixo.

    Args:
        idul (str): L'identifiant de l'utilisateur.
        secret (str): Le secret pour l'authentification.

    Returns:
        tuple: Un tuple contenant l'id de la partie, les joueurs et l'état du plateau.

    Raises:
        PermissionError: Si l'authentification échoue (code 401).
        RuntimeError: Si le serveur renvoie une erreur 406.
        ConnectionError: Si la connexion échoue.
    """
    try:
        response = requests.post(
            f"{URL}partie/",
            auth=(idul, secret)
        )

        if response.status_code == 200:
            data = response.json()
            return data['id'], data['état']['joueurs'], data['état']['plateau']

        if response.status_code == 401:
            message = response.json().get('message', 'Erreur 401')
            raise PermissionError(message)

        if response.status_code == 406:
            message = response.json().get('message', 'Erreur 406')
            raise RuntimeError(message)

        raise ConnectionError()

    except requests.RequestException as e:
        raise ConnectionError(f"Erreur lors de la connexion: {e}") from e


def jouer_un_coup(id_partie, origine, direction, idul, secret):
    """Joue un coup dans une partie existante.

    Args:
        id_partie (str): L'identifiant de la partie.
        origine (tuple): Les coordonnées de l'origine du coup.
        direction (str): La direction du coup (haut, bas, gauche, droite).
        idul (str): L'identifiant de l'utilisateur.
        secret (str): Le secret pour l'authentification.

    Returns:
        tuple: Un tuple contenant l'id de la partie, les joueurs et l'état du plateau, 
               ou un identifiant du gagnant si un gagnant est trouvé.

    Raises:
        PermissionError: Si l'authentification échoue (code 401).
        RuntimeError: Si le serveur renvoie une erreur 406.
        ConnectionError: Si la connexion échoue.
    """
    try:
        response = requests.put(
            f"{URL}partie/{id_partie}/",
            auth=(idul, secret),
            json={
                "origine": origine,
                "direction": direction
            }
        )

        if response.status_code == 200:
            data = response.json()

            if data.get('gagnant'):
                return data['gagnant']

            return data['id'], data['état']['joueurs'], data['état']['plateau']

        if response.status_code == 401:
            message = response.json().get('message', 'Erreur 401')
            raise PermissionError(message)

        if response.status_code == 406:
            message = response.json().get('message', 'Erreur 406')
            raise RuntimeError(message)

        raise ConnectionError(f"Erreur de connexion: {response.status_code}")

    except requests.RequestException as e:
        raise ConnectionError(f"Erreur lors de la connexion: {e}") from e


def récupérer_une_partie(id_partie, secret):
    """Récupère les informations d'une partie en cours.

    Args:
        id_partie (str): L'identifiant de la partie.
        secret (str): Le secret pour l'authentification.

    Returns:
        tuple: Un tuple contenant l'id de la partie, les joueurs, l'état du plateau et le gagnant.

    Raises:
        PermissionError: Si l'authentification échoue (code 401).
        ConnectionError: Si la connexion échoue.
    """
    url = f"{URL}partie/{id_partie}/"

    headers = {"Authorization": f"Bearer {secret}"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            return (
                data["id"],
                data["état"]["joueurs"],
                data["état"]["plateau"],
                data["gagnant"],
            )

        if response.status_code == 401:
            message = response.json().get("message", "Erreur non spécifiée.")
            raise PermissionError(message)

        raise ConnectionError()

    except requests.exceptions.RequestException as e:
        raise ConnectionError(f"Erreur lors de la connexion: {e}") from e
