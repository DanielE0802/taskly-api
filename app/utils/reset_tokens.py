import random
import string


def generate_reset_code(length: int = 6) -> str:
    """
    Genera un código alfanumérico aleatorio para restablecimiento de contraseña.
    Por defecto, el código tiene una longitud de 6 caracteres.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
