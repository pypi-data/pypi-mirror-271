from inegi_explorer.nodes import Subject, Indicator


class Explorer(Subject):
    def __init__(self):
        super().__init__("Origen", "0", -1, {})
        BI = Subject("Banco de Indicadores", "0000", 6, {})
        BIE = Subject("Banco de Indicadores Económicos (BIE)", "999999999999", 0, {})
        IPEF = Subject("Indicadores por Entidad Federativa", "0000", 7, {})
        IBPEF = Subject("Indicadores de Bienestar por Entidad Federativa", "0000", 8, {})
        self._children = [BI, BIE, IPEF, IBPEF]

    @staticmethod
    def from_id(id_: str, name: str = "", geographic_area_name=""):
        cls = None
        type_, geographic_area, series_key, database = id_.split("-")

        if type_ == "I":
            cls = Indicator
        elif type_ == "T":
            cls = Subject

        if cls:
            return cls(name, series_key, database, {}, geographic_area, geographic_area_name)
        else:
            raise ValueError(f"Invalid ID: {id_}")
