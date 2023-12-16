import pandas as pd
import requests
import json
from sqlalchemy import create_engine

def get_data_json() -> list:
  # code_list = ['a', 'b', 'c', 'd', 'g', 'h', 'j', 'l', 'm', 'n', 'p', 'r', 's']
  code_list = ['a']

  result = []
  for code in code_list:
      api_url = f'https://rx.ua/api/classifications/atc-levels-tree?code={code}&onlyTree=true'
      response = requests.get(api_url)
      data = json.loads(response.text)
      result.append(data)
  return result

def parse_json(json_data_list: list) -> pd.DataFrame:
  df = pd.DataFrame(columns=['id', 'code', 'name', 'parent_id'])
  for elem in json_data_list:
    level1 = elem['data']['atcTree'][0]
    row1 = read_elem_values(level1)
    df = pd.concat([df, pd.DataFrame([row1])], ignore_index=True)
    for level2 in level1['children']:
      row2 = read_elem_values(level2)
      df = pd.concat([df, pd.DataFrame([row2])], ignore_index=True)
      for level3 in level2['children']:
        row3 = read_elem_values(level3)
        df = pd.concat([df, pd.DataFrame([row3])], ignore_index=True)
        for level4 in level3['children']:
          row4 = read_elem_values(level4)
          df = pd.concat([df, pd.DataFrame([row4])], ignore_index=True)
          for level5 in level4['children']:
            row5 = read_elem_values(level5)
            df = pd.concat([df, pd.DataFrame([row5])], ignore_index=True)
  return df

def read_elem_values(elem) -> pd.Series:
  return pd.Series({
          'id': elem['_id'], 
          'code': elem['code'], 
          'name': elem['name_ua'], 
          'parent_id': elem['parent_id']
        })

def transform_ids_to_int(df: pd.DataFrame) -> pd.DataFrame:
  id_mapping = dict(zip(df['id'], range(1, len(df) + 1)))
  df['id'] = df['id'].map(id_mapping)
  df['parent_id'] = df['parent_id'].map(id_mapping).astype(pd.Int64Dtype())
  return df

def insert_to_db(user, password, host, port, database, df, table_name):
  connection_string = f'postgresql://{user}:{password}@{host}:{port}/{database}'
  engine = create_engine(connection_string)
  df.to_sql(name=table_name, con=engine, if_exists='replace', index=False)


json_data_list = get_data_json()
dataframe = parse_json(json_data_list)
df_id_as_int = transform_ids_to_int(dataframe)
df_id_as_int.head()
insert_to_db('user', 'password', 'localhost', 5432, 'ic', df_id_as_int, 'atc_classification')

# docker cp ./atc_script.py isure-cover:tmp
# apt install python3.11-venv
# python3 -m venv /venv
# export PATH="/venv/bin:$PATH"
# apt-get install -y python3 python3-pip libpq-dev && rm -rf /var/lib/apt/lists/*
# pip install sqlalchemy psycopg2
