import concurrent.futures
from typing import Union, List
import pandas as pd

from inegi_explorer.nodes.node import Node
from inegi_explorer.config import inegi_root, language, key, debug
from inegi_explorer.nodes.indicator_node import Indicator


class Subject(Node):
    type = "Tema"

    @classmethod
    def from_response(cls, response: dict) -> 'Node':
        # example reponse: {"claveSerie":"567","indicador":null,"orden":null,
        # "tema":{"BD":8,"color":"00918F","hijos":0,"infoComplementaria":null,"nombre":"Accesibilidad a servicios",
        # "nombreSuperior":null,"numeroIndica":3,"orden":1,"tema":"567","temaSuperior":null,"totalSubtemas":null,
        # "urlImagen":"\\/img\\/temas\\/servicios.png","urlTema":null},"tipoNodo":"TEMA","total":0}
        if subject_info := response.get('tema'):
            name = subject_info.get('nombre')
            series_key = response.get('claveSerie')
            database = subject_info.get('BD')
            return cls(name=name, series_key=series_key, database=database, data=response)

    @property
    def url_children(self) -> str:
        endpoint = "API.svc/NodosTemas"
        url = f"{inegi_root}/{endpoint}/{self.geographic_area}/{language}/" \
              f"{self.series_key}/null/null/null/{self.database}/true/null/null/json/{key}"
        return url

    def get_children(self) -> List[Union['Node', None]]:
        if self._children == []:
            # Example response Recieved: b'[{"claveSerie":"567","indicador":null,"orden":null,
            # "tema":{"BD":8,"color":"00918F","hijos":0,"infoComplementaria":null,"nombre":"Accesibilidad a servicios",
            # "nombreSuperior":null,"numeroIndica":3,"orden":1,"tema":"567","temaSuperior":null,"totalSubtemas":null,
            # "urlImagen":"\\/img\\/temas\\/servicios.png","urlTema":null},"tipoNodo":"TEMA","total":0},
            # {"claveSerie":"575","indicador":null,"orden":null,"tema":{"BD":8,"color":null,"hijos":0,
            # "infoComplementaria":null,"nombre":"Relaciones sociales en la comunidad","nombreSuperior":null,
            # "numeroIndica":1,"orden":2,"tema":"575","temaSuperior":null,"totalSubtemas":null,"urlImagen":null,
            # "urlTema":null},"tipoNodo":"TEMA","total":0},{"claveSerie":"569","indicador":null,"orden":null,
            # "tema":{"BD":8,"color":"F6551E","hijos":0,"infoComplementaria":null,"nombre":"Educaci\xc3\xb3n",
            # "nombreSuperior":null,"numeroIndica":3,"orden":3,"tema":"569","temaSuperior":null,"totalSubtemas":null,
            # "urlImagen":"\\/img\\/temas\\/educacion.png","urlTema":null},"tipoNodo":"TEMA","total":0},
            # ...]'
            response = self.request_url(self.url_children, debug)
            self._children = [
                Subject.from_response(resp) if resp.get('tipoNodo') == 'TEMA' else Indicator.from_response(resp)
                for resp in response]
        return self._children

    def fetch(self, raw: bool = False, *args, **kwargs) -> Union[pd.DataFrame, pd.Series, dict, List[dict]]:
        def fetch_child(child):
            return child.fetch(raw)

        with concurrent.futures.ThreadPoolExecutor(max_workers=None) as executor:
            children_list = self.get_children()
            futures = [executor.submit(fetch_child, child) for child in children_list]
            series_list = [future.result() for future in futures]
        if raw:
            return series_list
        else:
            df = pd.concat(series_list, axis=1)
            return df
