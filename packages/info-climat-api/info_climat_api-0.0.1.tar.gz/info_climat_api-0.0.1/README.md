# InfoClimatAPI

## Exemple

```python
from InfoClimatAPI import InfoClimat

api = InfoClimat()
api.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

# données pour une liste de stations
result = api.get_data(["000OG", "000DD"], "2024-04-01", "2024-05-01")
print(result)

# liste des stations
result_stations = api.get_stations()
print(result_stations)
```