class UserNotFoundError(Exception):
    """El usuario de la transacción no existe"""


class TransactionNotFoundError(Exception):
    """La transacción pedida no existe"""


class ModelNotAvailableError(Exception):
    """El modelo de IA no está cargado, por eso no se puede evaluar ninguna transacción"""
