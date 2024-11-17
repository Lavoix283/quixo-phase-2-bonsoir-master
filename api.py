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

            if data.get('gagnant'):
                return data['gagnant']

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
        elif response.status_code == 401:
            message = response.json().get("message", "Erreur non spécifiée.")
            raise PermissionError(message)
        else:
            raise ConnectionError()
    
    except requests.exceptions.RequestException as e:
        raise ConnectionError from e
