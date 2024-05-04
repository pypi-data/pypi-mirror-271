from sqlalchemy import create_engine
import pandas as pd
from openai import OpenAI
import os, re, textwrap, json, sys

class TableTalk():
    def __init__(
            self,
            openai_api_key: str,
            data_directory: str,
            generate_response: bool = True,
            ) -> None:
        self.openai_api_key = openai_api_key
        self.data_directory = data_directory
        self.generate_response = generate_response

    def _clean_query(
            self,
            query: str,
            ) -> str:
        cleaned_query = re.sub(r'[^\w\s?-]+', '', query)
        cleaned_query = re.sub(r'\s+', ' ', cleaned_query).strip().lower()
        return cleaned_query
    
    def _create_data_sources_prompt_string(
            self, 
            data_engine,
            ) -> str:
        data_source_str = ""
        if not os.path.exists(self.data_directory) or not os.path.isdir(self.data_directory):
            raise FileNotFoundError(f'File not found: {self.data_directory}')
        else:
            files = os.listdir(self.data_directory)
            if len(files) == 0:
                raise FileNotFoundError(f'No files found in directory: {self.data_directory}')
            else:
                file_count = 0
                for file in files:
                    ext = os.path.splitext(file)[1]
                    if ext.lower() in ['.csv', '.xlsx']:
                        file_count += 1
                if file_count == 0:
                    raise FileNotFoundError(f'No CSV or Excel files found in directory: {self.data_directory}')
                else:
                    print(f'Found {file_count} files in directory: {self.data_directory}')
                    data_source_str += textwrap.dedent(f"""There are {file_count} database tables available to answer this question. Here is the JSON containing objects that has the database table number as the key and the table name, table columns and table head as the values.
                    DATA SOURCES:\n""")

                    table_dict = {}
                    for idx, file in enumerate(files):
                        if os.path.splitext(file)[1] in ['.csv', '.xlsx']:
                            df = pd.read_csv(f'{self.data_directory}/{file}') if file.endswith('.csv') else pd.read_excel(f'{self.data_directory}/{file}')
                            table_name = file.split('.')[0].lower()
                            df.to_sql(table_name, data_engine, if_exists='replace', index=False)
                            table_dict[str(idx)] = {'table_name': table_name, 'columns': df.columns.to_list(), 'head': df.head().to_dict(orient='records')}
                    data_source_str += json.dumps(table_dict)
        return data_source_str

    def query_table(
            self,
            query: str,
            save_source_data_as_csv: bool = False,
            save_sql_to_txt: bool = False,
            sql_prompt: str = None,
            generative_prompt: str = None,
            ):
        print('Scanning your data...')
        client = OpenAI(api_key=self.openai_api_key)
        engine = create_engine("sqlite:///:memory:")
        cleaned_query = self._clean_query(str(query).strip())
        query_string = f'Based on this question or request:\n\n** {cleaned_query} **\n\nuse the following data sources to answer the question:'
        data_sources_string = self._create_data_sources_prompt_string(engine)
        # print(data_sources_string)

        if sql_prompt:
            sql_prompt_to_use = query_string + '\n\n'
            sql_prompt_to_use += data_sources_string + '\n\n'
            sql_prompt_to_use += sql_prompt
        else:
            sql_prompt_to_use = query_string + '\n\n'
            sql_prompt_to_use += data_sources_string + '\n\n'
            sql_prompt_to_use += f"""
            SQL INSTRUCTIONS:
            - Write a SQL query that retrieves data relevant to the query while adhering to general SQL standards. Ensure the query is adaptable to any dataset with the same schema.
            - Only generate a single SQL statement. Avoid creating new columns or misaligning table columns.
            - Consider SQLite's specific limitations, as all queries will run on a SQLite database.
            - Implement case-insensitive comparisons. For example, use 'WHERE LOWER(pi_name) LIKE '%john smith%' instead of 'WHERE pi_name LIKE '%John Smith%'.
            - Use the 'IN' operator for multiple fixed values instead of multiple 'LIKE' clauses. Example: 'WHERE pi_name IN ('john smith', 'jane doe')'.
            - Include wildcard placeholders to accommodate variations in data spacing, e.g., 'WHERE LOWER(pi_name) LIKE '%john%smith%' for 'John Smith'.
            - Optimize the query to return only the necessary data. Utilize SQL clauses like 'DISTINCT', 'WHERE', 'GROUP BY', 'ORDER BY', 'LIMIT', 'JOIN', 'UNION', etc., to refine the data retrieval.
            - In cases of long string comparisons involving multiple keywords, use 'OR' for non-stop-words to cover any of the conditions. Example: 'WHERE LOWER(text) LIKE '%anti-jamming%' OR LOWER(text) LIKE '%gps%' OR LOWER(text) LIKE '%navigation%'.
            - Aim to return comprehensive and relevant information by defaulting to broader, lowercase comparisons.

            RESPONSE INSTRUCTIONS:
            - Return ONLY the following key-value pair: 'sql': 'your sql query here'.
            - Only include the dictionary in the response. Don't include '```python' or '```' in the response.
            - The response should be a python dictionary that returns 'dict' when evaluated: type(eval(response)) == dict.
            """

        sql_generative_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": sql_prompt_to_use},
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        result = sql_generative_response.choices[0].message.content
        if type(eval(result)) == dict:
            sql_dict = eval(result)
            sql_string = sql_dict.get('sql')
            print(f'SQL Query: {sql_string}\n')
            pattern = r'```(?:\w+\n)?(.*?)```'
            sql = re.sub(pattern, r'\1', sql_string, flags=re.DOTALL)
        new_df = pd.read_sql(sql, engine)

        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages= [
                {"role": "system", "content": "You are a helpful research assistant."},
                {"role": "user", "content": f"""
                    Based on the question: {cleaned_query}, the following data was found:\n
                    SQL Data in JSON format: {json.dumps(new_df.to_dict())}\n

                    Do not make reference the data sources themselves, only reference the data. For example, don't mention 'SQL data', 'Vector data', 'databases', etc.\n
                    
                    **This is a retrieval-augmented generation task, so it is critical that you only generate the answer based on the data provided in this prompt and the chat history.**
                """
                }
            ],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        print(response.choices[0].message.content)




        # stream = client.chat.completions.create(
        #     model="gpt-4-turbo",
        #     messages= [
        #         {"role": "system", "content": "You are a helpful research assistant."},
        #         {"role": "user", "content": f"""
        #             Based on the question: {cleaned_query}, the following data was found:\n
        #             SQL Data in JSON format: {json.dumps(new_df.to_dict())}\n

        #             Do not make reference the data sources themselves, only reference the data. For example, don't mention 'SQL data', 'Vector data', 'databases', etc.\n
                    
        #             **This is a retrieval-augmented generation task, so it is critical that you only generate the answer based on the data provided in this prompt and the chat history.**
        #         """
        #         }
        #     ],
        #     temperature=1,
        #     max_tokens=1024,
        #     top_p=1,
        #     frequency_penalty=0,
        #     presence_penalty=0,
        #     stream=True
        # )
        # full_response = ""
        # try:
        #     for completion in stream:
        #         delta_content = completion.choices[0].delta.content
        #         if delta_content:
        #             full_response += delta_content
        #             sys.stdout.write(delta_content)
        #         if completion.choices[0].finish_reason == 'stop':
        #             break
        # except Exception as e:
        #     print(e)
