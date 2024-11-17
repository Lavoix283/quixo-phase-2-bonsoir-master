import requests


URL = "https://pax.ulaval.ca/quixo/api/a24/"


def initialiser_partie(idul, secret):
    try:
        response = requests.post(
            f"{URL}partie/",
            auth=(idul, secret)
        )

        if response.status_code == 200:
            data = response.json()
            # Accéder aux données à l'intérieur de la clé 'état'
            return data['id'], data['état']['joueurs'], data['état']['plateau']
        
        elif response.status_code == 401:
            message = response.json().get('message', 'Erreur 401')
            raise PermissionError(message)
        
        elif response.status_code == 406:
            message = response.json().get('message', 'Erreur 406')
            raise RuntimeError(message)
        
        else:
            raise ConnectionError()
    
    except requests.RequestException as e:
        raise ConnectionError(f"Erreur lors de la connexion: {e}")


def jouer_un_coup(id_partie, origine, direction, idul, secret):
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

            # Vérifie si un gagnant est présent et le renvoie
            if data.get('gagnant'):
                return data['gagnant']  # Retourne le nom du gagnant

            # Retourne l'état mis à jour du jeu
            # Utilise la structure correcte pour accéder aux données du plateau et des joueurs
            return data['id'], data['état']['joueurs'], data['état']['plateau']
        
        elif response.status_code == 401:
            message = response.json().get('message', 'Erreur 401')
            raise PermissionError(message)
        
        elif response.status_code == 406:
            message = response.json().get('message', 'Erreur 406')
            raise RuntimeError(message)
        
        else:
            raise ConnectionError(f"Erreur de connexion: {response.status_code}")
    
    except requests.RequestException as e:
        raise ConnectionError(f"Erreur lors de la connexion: {e}")


def récupérer_une_partie(id_partie, idul, secret):
    url = f"{URL}partie/{id_partie}/"
    
    # Définir l'en-tête pour l'authentification
    headers = {"Authorization": f"Bearer {secret}"}

    try:
        # Effectuer la requête GET
        response = requests.get(url, headers=headers)
        
        # Gérer les codes de réponse HTTP
        if response.status_code == 200:
            # Si la requête a réussi, traiter la réponse JSON
            data = response.json()
            return (
                data["id"],  # Identifiant de la partie
                data["état"]["joueurs"],  # Liste des joueurs
                data["état"]["plateau"],  # État du plateau
                data["gagnant"],  # Gagnant ou None si pas encore de gagnant
            )
        elif response.status_code == 401:
            # Si erreur de permission (401), lever une exception PermissionError
            message = response.json().get("message", "Erreur non spécifiée.")
            raise PermissionError(message)
        else:
            # Pour d'autres erreurs HTTP, lever une exception ConnectionError
            raise ConnectionError()
    
    except requests.exceptions.RequestException as e:
        # Si une exception se produit pendant la requête (timeouts, etc.)
        raise ConnectionError from e
