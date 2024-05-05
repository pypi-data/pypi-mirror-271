# BCRA-client-python
Consumo de datos de la API del Banco Central de la República Argentina (BCRA)

Esta librería está construida con base en la documentación presentada por la misma entidad en el siguiente [link](https://www.bcra.gob.ar/BCRAyVos/catalogo-de-APIs-banco-central.asp).

## Instalar

Debe usar pip para instalar o actualizar a la última versión estable.
```
pip install -U bcra-api-client
```

## Como usar
Su uso es simple, se debe crear primero un cliente a la API.

**Nota**: Hasta ahora la API tiene dos endpoints de estadísticas.

## Cliente API
```python
from bcra import Client

cliente = Client()
```

## Principales variables
Método para obtener la lista de todas las variables publicadas por el BCRA.
```python
variables_endpoint = cliente.statistics.variables
print(variables_endpoint.get())
```

## Datos de Variable
Método para obtener los valores para la variable y el rango de fechas indicadas.

se debe llamar a filter(id_variable, from_, to)

Donde: 

- id_variable : Int (Se obtiene de consultar a la lista de todas las variables)
- from_: String (yyyy-mm-dd)
- to: String (yyyy-mm-dd)






```python
variables_endpoint = cliente.statistics.variables
print(variables_endpoint.filter(5, '2024-01-01', '2024-05-01'))
```

