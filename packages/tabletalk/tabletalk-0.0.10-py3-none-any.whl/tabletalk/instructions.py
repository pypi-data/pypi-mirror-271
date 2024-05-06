import os, json
import pandas as pd

def _generate_query_intructions(
        query: str
        ) -> str:
    return f'Based on this question or request:\n\n** {query} **\n\nuse the following data sources to answer the question:'

def _generate_data_sources_instructions(
        data_directory: str, 
        data_engine,
        ) -> str:
    data_source_str = ""
    if not os.path.exists(data_directory) or not os.path.isdir(data_directory):
        raise FileNotFoundError(f'File not found: {data_directory}')
    else:
        files = os.listdir(data_directory)
        if len(files) == 0:
            raise FileNotFoundError(f'No files found in directory: {data_directory}')
        else:
            file_count = 0
            for file in files:
                ext = os.path.splitext(file)[1]
                if ext.lower() in ['.csv', '.xlsx']:
                    file_count += 1
            if file_count == 0:
                raise FileNotFoundError(f'No CSV or Excel files found in directory: {data_directory}')
            else:
                data_source_str += f"""
There are {file_count} database tables available to answer this question. Here is the JSON data containing objects containing the database table number as the key and the table name, table columns and table head as the values.
DATA SOURCES:\n"""

                table_dict = {}
                for idx, file in enumerate(files):
                    if os.path.splitext(file)[1] in ['.csv', '.xlsx']:
                        df = pd.read_csv(f'{data_directory}/{file}') if file.endswith('.csv') else pd.read_excel(f'{data_directory}/{file}')
                        cleaned_cols = [col.strip().lower().replace(' ','_').replace(':','').replace('?','') for col in df.columns]
                        df.columns = cleaned_cols
                        table_name = file.split('.')[0].lower().strip().replace(' ','_')
                        df.to_sql(table_name, data_engine, if_exists='replace', index=False)
                        table_dict[str(idx)] = {'table_name': table_name, 'columns': df.columns.to_list(), 'head': df.head().to_dict(orient='records')}
                data_source_str += json.dumps(table_dict)
    return data_source_str

def _generate_base_sql_instructions() -> str:
    base_sql_instructions = f"""
SQL INSTRUCTIONS:
- Write a SQL query that retrieves data relevant to the query while adhering to general SQL standards. Ensure the query is adaptable to any dataset with the same schema.
- Only generate a single SQL statement. Avoid creating new columns or misaligning table columns.
- Use parameterized queries to prevent SQL injections. Do not allow SQL injections or use unsafe SQL practices.
- Consider SQLite's specific limitations, as all queries will run on a SQLite database.
- Implement case-insensitive comparisons. For example, use 'WHERE LOWER(pi_name) LIKE '%john%smith%' instead of 'WHERE pi_name LIKE '%John Smith%'.
- Use the 'IN' operator for multiple fixed values instead of multiple 'LIKE' clauses. Example: 'WHERE pi_name IN ('john smith', 'jane doe')'.
- Include wildcard placeholders to accommodate variations in data spacing, e.g., 'WHERE LOWER(pi_name) LIKE '%john%smith%' for 'John Smith'.
- Optimize the query to return only the necessary data. Utilize SQL clauses like 'DISTINCT', 'WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT', 'JOIN', 'UNION', etc., to refine the data retrieval.
- In cases of long string comparisons involving multiple keywords, use 'OR' for non-stop-words to cover any of the conditions. Example: 'WHERE LOWER(text) LIKE '%anti-jamming%' OR LOWER(text) LIKE '%gps%' OR LOWER(text) LIKE '%navigation%'.
- Aim to return comprehensive and relevant information by defaulting to broader, lowercase comparisons.
    """
    return base_sql_instructions

def _generate_response_instructions() -> str:
    response_instructions = f"""
RESPONSE INSTRUCTIONS:
- Return ONLY the following key-value pairs: 'sql': 'your sql query here'.
- Only include the dictionary in the response. Don't include '```python' or '```' in the response.
- The response should be a python dictionary that returns 'dict' when evaluated: type(eval(response)) == dict.
    """
    return response_instructions