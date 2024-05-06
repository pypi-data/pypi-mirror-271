from .connection import APIConnection


def generate_average_value(high, low):
    return round(((float(high) + float(low)) / 2), 5)


def dolar_comercial() -> dict[str, str]:
    """
    Retorna a cotação do dólar comercial em BRL.

    Returns:
        Um dicionário com o valor da cotação. Ex.: {'value': 5.00000}

    Raises:
        ConnectionError: Caso não seja possível conectar com a API que nos daria o resultado.
        MissingSchema: Caso a url da API terceira esteja equivocada.

    Examples:
        >>> type(dolar_comercial())
        <class 'dict'>
    """
    api = APIConnection('https://economia.awesomeapi.com.br/json/last')
    response = api.get('/USD-BRL')
    data = response['USDBRL']
    average = generate_average_value(data['high'], data['low'])
    return {'value': average}


def dolar_turismo() -> dict[str, str]:
    """
    Retorna a cotação do dólar turismo em BRL.

    Returns:
        Um dicionário com o valor da cotação. Ex.: {'value': 5.00000}

    Raises:
        ConnectionError: Caso não seja possível conectar com a API que nos daria o resultado.
        MissingSchema: Caso a url da API terceira esteja equivocada.

    Examples:
        >>> type(dolar_turismo())
        <class 'dict'>
    """
    api = APIConnection('https://economia.awesomeapi.com.br/json/last')
    response = api.get('/USD-BRLT')
    data = response['USDBRLT']
    average = generate_average_value(data['high'], data['low'])
    return {'value': average}
