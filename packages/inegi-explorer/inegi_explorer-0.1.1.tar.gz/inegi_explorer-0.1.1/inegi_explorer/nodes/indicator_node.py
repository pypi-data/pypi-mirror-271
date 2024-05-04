from typing import Union, List
import pandas as pd
from inegi_explorer.nodes.node import Node
from inegi_explorer.config import inegi_root, language, key, debug


class Indicator(Node):
    type = "Indicador"

    @classmethod
    def from_response(cls, response: dict) -> 'Indicator':
        # example response: {'claveSerie': '', 'indicador': {'BD': 8, 'area_geografica': '0700', 'bmapa': False,
        # 'descPeriodo': '2020', 'descripcionExcepcion': None, 'desglose': 2, 'entidad': '0', 'factor': None,
        # 'familia': None, 'frecuencia': 'Quinquenal', 'indicador': 6200029291, 'localidad': '0', 'municipio': '0',
        # 'nombre': 'Habitaciones por persona', 'nombreFamilia': '',
        # 'nombre_area_geografica': 'Estados Unidos Mexicanos', 'orden': 1, 'periodoCorto': '2020', 'posicion': 0,
        # 'serie': '', 'unidad': 'Promedio', 'valor': '1.0'}, 'orden': None, 'tema': None, 'tipoNodo': 'INDICADOR',
        # 'total': 0}

        # example 2: {'claveSerie': '101700400010002000380070', 'indicador': {'BD': None, 'area_geografica': None,
        # 'bmapa': False, 'descPeriodo': '2023  4T', 'descripcionExcepcion': '', 'desglose': 1, 'entidad': '0',
        # 'factor': None, 'familia': None, 'frecuencia': 'Trimestral', 'indicador': 793096, 'localidad': None,
        # 'municipio': '0', 'nombre': 'Índice', 'nombreFamilia': None, 'nombre_area_geografica': None, 'orden': None,
        # 'periodoCorto': '2023/04', 'posicion': None, 'serie': '101700400010002000380070',
        # 'unidad': 'Índice base 2018=100', 'valor': '94.9'}, 'orden': None, 'tema': None, 'tipoNodo': 'INDICADOR',
        # 'total': 0}

        if indicator_info := response.get('indicador'):

            params = {'name': f"{indicator_info.get('nombre')} - {indicator_info.get('unidad')}",
                      'series_key': indicator_info.get('indicador'),
                      'data': response}

            if database := indicator_info.get('BD'):
                params.update({'database': database})
            else:
                # database 0 returns None
                params.update({'database': 0})

            if geographic_area := indicator_info.get('area_geografica'):
                params.update({'geographic_area': geographic_area})

            if geographic_area_name := indicator_info.get('nombre_area_geografica'):
                params.update({'geographic_area_name': geographic_area_name})

            return cls(**params)
        else:
            raise ValueError(f"Invalid response to parse: {response}")

    @property
    def url_children(self):
        endpoint = "API.svc/CatalogoAreaGeograficaV3"
        form = "json"
        url = f"{inegi_root}/{endpoint}/" \
              f"{self.geographic_area}/{self.series_key}/null/null/{self.database}/null/{form}/{key}"
        return url

    def get_children(self) -> Union[List['Indicator'], None]:
        if self._children == []:
            response = self.request_url(self.url_children, debug)
            # example response: [{'AREAS_GEOGRAFICAS_DEPENDIENTES': [{'AREA_GEOGRAFICA': '0700', 'DESGLOSE_GEOGRAFICO': 1, 'HIJOS': 0, 'NOMBRE': 'Estados Unidos Mexicanos', 'NOMBRE_DESGLOSE_GEOGRAFICO': 'Nacional', 'UBICACION_GEOGRAFICA': 1, 'UBICACION_GEOGRAFICA_SUPERIOR': 0}], 'AREA_GEOGRAFICA': '', 'DESGLOSE_GEOGRAFICO': 0, 'HIJOS': 0, 'NOMBRE': '', 'NOMBRE_DESGLOSE_GEOGRAFICO': '', 'UBICACION_GEOGRAFICA': 0}]
            response = response[0]
            if isinstance(response, dict):
                if areas := response.get("AREAS_GEOGRAFICAS_DEPENDIENTES"):
                    if len(areas) > 1:
                        children = [
                            Indicator(self.name + " - " + self.geographic_area_name, self.series_key, self.database,
                                      self.data,
                                      area.get("AREA_GEOGRAFICA"), area.get("NOMBRE")) for area in areas]
                        self._children = children
        return self._children

    @property
    def url_data(self) -> str:
        endpoint = "indicador"
        url = f"{inegi_root}/{endpoint}/{self.series_key}/" \
              f"{self.geographic_area}/{language}/false/{self.database}/json/{key}"
        return url

    @staticmethod
    def _parse_data(response) -> pd.Series:
        # Example response: {'Data': {'GeneralNote': 'Metadato generado con base en la metodología elaborada y propuesta por la OCDE.', 'GeneralSource': None, 'Serie': [{'CurrentValue': '77.26', 'DescriptionPeriod': '2014', 'NotesPeriod': '', 'SourcesPeriod': 'Módulo de Bienestar Autorreportado 2012.', 'TimePeriod': '2014', 'ValueStatus': 'Definitiva'}, {'CurrentValue': '72.2', 'DescriptionPeriod': '2021', 'NotesPeriod': '', 'SourcesPeriod': 'Módulo de Bienestar Autorreportado 2012.', 'TimePeriod': '2021', 'ValueStatus': 'Definitiva'}]}, 'MetaData': {'CreationDate': '03/05/2024 04:42:25 p. m.', 'Factor': None, 'Freq': 'No establecida', 'Indicator': 6200108755, 'LastUpdate': '24/01/2022 12:00:00 a. m.', 'Name': 'Calidad de la red social de soporte', 'NoOfDecimals': '1', 'Unit': 'Porcentaje', 'Region': 'Estados Unidos Mexicanos'}}
        try:
            metadata = response.get('MetaData')
            name = f"{metadata.get('Name')} - {metadata.get('Unit')} - {response.get('MetaData').get('Region').split('>')[-1].strip()}"
            data = response["Data"]["Serie"]
            serie = pd.Series(
                {entry['TimePeriod']: pd.to_numeric(entry['CurrentValue'], errors='coerce') for entry in data},
                name=name)
            serie.index = pd.to_datetime(serie.index)
            return serie
        except Exception as e:
            print(f"\033[91m{e}: {response} \033[0m")
            return pd.Series()

    def fetch_this(self, raw: bool = False, debug: bool = False) -> Union[tuple, pd.Series]:
        url = self.url_data
        response = self.request_url(url, debug)
        if raw:
            return response, url
        else:
            return self._parse_data(response)

    def fetch_children(self, raw: bool = False, debug: bool = False) -> Union[list, pd.DataFrame]:
        urls = [child.url_data for child in self.get_children()]
        if raw:
            responses = self.request_urls(urls, debug)
            return responses
        else:
            try:
                responses = self.request_urls(urls, debug, self._parse_data)
                df = pd.concat(responses, axis=1)
                return df
            except ValueError:
                raise ValueError("No available aggregations")

    def fetch(self, agg: bool = False, *args, **kwargs) -> Union[pd.DataFrame, pd.Series, dict, List[dict]]:
        if agg:
            return self.fetch_children(*args, **kwargs)
        else:
            return self.fetch_this(*args, **kwargs)
