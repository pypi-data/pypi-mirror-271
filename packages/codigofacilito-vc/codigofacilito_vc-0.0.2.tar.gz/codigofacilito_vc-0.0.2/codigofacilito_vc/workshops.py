import requests

print("El valor de main para workshops es : ", __name__)

def unreleased():
    """Retorna los próximos talleres en Código Facilito
    
    >>> type(unreleased()) == type(dict())
    True
    """
    url = "https://codigofacilito.com/api/v2/workshops/unreleased"
    response = requests.get(url)
    
    if response.status_code == 200:
        payload = response.json()
        return payload["data"]