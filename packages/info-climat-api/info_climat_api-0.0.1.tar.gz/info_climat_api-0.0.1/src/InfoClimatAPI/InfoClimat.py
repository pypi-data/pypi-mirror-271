import json
import os
import requests


def get_json_request(path) -> dict:
    req = requests.get(path)
    if req.status_code != 200:
        raise
    try:
        return json.loads(req.text)
    except ValueError:
        raise


class InfoClimat:
    INFOCLIMAT_API_KEY = "INFOCLIMAT_API_KEY"

    def __init__(self):
        self._base = "https://www.infoclimat.fr/opendata/"
        self._url_stations = "https://www.infoclimat.fr/opendata/stations_xhr.php"

    @property
    def api_key(self):
        return os.environ.get(self.INFOCLIMAT_API_KEY)

    @api_key.setter
    def api_key(self, api_key):
        os.environ[self.INFOCLIMAT_API_KEY] = str(api_key)

    def get_data(self, stations: list[str], start, end, data_format="json", method="get"):
        """
        Récupération des données pour une liste de stations
        :param stations: liste des id de station (ex: ["000OG", "000DD"])
        :param start: date de départ (ex: "2024-04-29")
        :param end: date de fin (ex: "2024-05-01")
        :param data_format:
        :param method:
        :return:
        """
        if self.api_key is None or self.api_key == "":
            raise Exception("No API key found.")

        url = (f"{self._base}?method={method}"
               f"&format={data_format}"
               f"&start={start}"
               f"&end={end}"
               f"&token={self.api_key}"
               )
        for station in stations:
            url += f"&stations[]={station}"

        if data_format == "json":
            return get_json_request(url)
        elif data_format == "csv":
            raise Exception("No yet implemented")
        else:
            raise Exception("Unknown format")

    def get_stations(self):
        """
        Récupération de la liste des stations
        Pas de clé api requise
        :return:
        """
        return get_json_request(self._url_stations)


if __name__ == '__main__':

    api = InfoClimat()
    api.api_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

    # Test requete api
    result = api.get_data(["000OG", "000DD"], "2024-04-01", "2024-05-01")
    print(result)

    # Test liste des stations
    result_stations = api.get_stations()
    print(result_stations)
