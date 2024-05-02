import logging
from codigofacilito_vc import unreleased

"""
logging package

INFO -> 10
DEBUG -> 20
WARNING -> 30
ERROR -> 40
CRITICAL -> 50
"""

logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    logging.debug(">>> Ejecutando función __main__")

    # Es ideal que aquí se ejecuten las pruebas
    workshops = unreleased()
    print(workshops)
    print(unreleased.__doc__)
    print(__name__)

    logging.debug(">>> Finalizando función __main__")