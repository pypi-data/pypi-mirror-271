
class PathIncomplete(Exception):
    """
        Faltan parámetros o datos de un path
    """


class TrafficLimit(Exception):
    """
        Límite máximo de tráfico, 100 requests por 1s
    """


class WrongDataType(Exception):
    """
        Tipo de datos incorrecto
    """