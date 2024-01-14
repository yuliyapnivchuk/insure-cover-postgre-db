import pandas as pd
import requests
import json
from sqlalchemy import create_engine
from sqlalchemy import text

def insert_to_db(user: str, password: str, host: str, port: int, database: str, df: pd.DataFrame):
    connection_string = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(connection_string)
    with engine.connect() as conn:
        for index, row in df.iterrows():
            result = conn.execute(
                text("SELECT id FROM atc_classification WHERE code = :atc_code"),
                [{"atc_code": row["atc_code"]}]
            ).first()

            if result is not None:
                conn.execute(
                    text("INSERT INTO medicines (name, atc_code_id) SELECT :name, :atc_code_id "
                        + "WHERE NOT EXISTS (SELECT * FROM medicines WHERE name = :name AND atc_code_id = :atc_code_id)"),
                    [{"name": row["name"], "atc_code_id": result[0]}]
                )
            else:
                if row["atc_code"] is not None and len(row["atc_code"]) > 0:
                    print(row["atc_code"] + ' not found in ATC classifier')
                    conn.execute(
                        text("INSERT INTO medicines (name, atc_code_id, error) SELECT :name, :atc_code_id, :error "
                        + "WHERE NOT EXISTS (SELECT * FROM medicines WHERE name = :name)"),
                        [{"name": row["name"], "atc_code_id": None, 'error': row["atc_code"] + ' not found in ATC classifier'}]
                    )
                else:
                    conn.execute(
                        text("INSERT INTO medicines (name, atc_code_id) SELECT :name, :atc_code_id "
                        + "WHERE NOT EXISTS (SELECT * FROM medicines WHERE name = :name)"),
                        [{"name": row["name"], "atc_code_id": None}]
                    )
        conn.commit()


def get_data_from_api(api_endpoint: str, parameters: dict) -> pd.DataFrame:
    page_total = json.loads((requests.get(api_endpoint, params=parameters)).text)["page" ]["total"]
    df = pd.DataFrame(columns=["name", "atc_code"])
    for page_number in range(1, page_total + 1):
        page_param = {"page": page_number}
        parameters.update(page_param)
        response = requests.get(api_endpoint, params=parameters)
        data = json.loads(response.text)
        for elem_index in range(len(data["result"])):
            elem = data["result"][elem_index]
            atc_param = elem["atc"]
            if (atc_param is not None) and (' ' in atc_param):
                atc_list = atc_param.strip().replace(',', ' ').split()
                for atc in atc_list:
                    df.loc[len(df)] = [elem["title"], atc]
            elif (atc_param is None):
                df.loc[len(df)] = [elem["title"], atc_param]
            else:
                df.loc[len(df)] = [elem["title"], atc_param.strip()]
    return df


api_endpoint = "https://eliky.in.ua/api/medicament"
parameters = {"api_key": "dUGwPMTx-9aaHDXIjgN34Nt46QHvp1dv", "page": 0}

df = get_data_from_api(api_endpoint, parameters)
insert_to_db("ic", "ic", "localhost", 5432, "insure_cover", df)
