from sqlalchemy import create_engine
import pandas as pd
from openai import OpenAI
import os, re, textwrap, json, sys
from . import instructions

class TableTalk():
    def __init__(
            self,
            openai_api_key: str,
            data_directory: str,
            ) -> None:
        self.openai_api_key = openai_api_key
        self.data_directory = data_directory

    def _clean_query(
            self,
            query: str,
            ) -> str:
        cleaned_query = re.sub(r'[^\w\s?-]+', '', query)
        cleaned_query = re.sub(r'\s+', ' ', cleaned_query).strip().lower()
        return cleaned_query
    
    def query(
            self,
            query: str,
            generate_response: bool = True,
            save_filtered_data_to_csv: bool = False,
            save_sql_to_txt: bool = False,
            additional_sql_instructions: list = None,
            generative_instructions: str = None,
            additional_generative_instructions: list = None,
            ):
        # print('Scanning your data...')
        client = OpenAI(api_key=self.openai_api_key)
        engine = create_engine("sqlite:///:memory:")
        cleaned_query = self._clean_query(str(query).strip())

        sql_prompt_to_use = instructions._generate_query_intructions(cleaned_query) + '\n\n'
        sql_prompt_to_use += instructions._generate_data_sources_instructions(self.data_directory, engine) + '\n\n'
        sql_prompt_to_use += instructions._generate_base_sql_instructions() + '\n\n'
        if additional_sql_instructions:
            if not isinstance(additional_sql_instructions, list):
                raise ValueError('additional_sql_instructions must be a list of strings')
            else:
                sql_prompt_to_use += '\nADDITIONAL SQL INSTRUCTIONS:\n'
                for instruction in additional_sql_instructions:
                    sql_prompt_to_use += instruction + '\n\n'
        sql_prompt_to_use += instructions._generate_sql_response_instructions() + '\n\n'

        sql_generative_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": sql_prompt_to_use},
            ],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
        )
        result = sql_generative_response.choices[0].message.content
        if type(eval(result)) == dict:
            sql_dict = eval(result)
            sql_string = sql_dict.get('sql')
            pattern = r'```(?:\w+\n)?(.*?)```'
            sql = re.sub(pattern, r'\1', sql_string, flags=re.DOTALL)
            queried_df = pd.read_sql(sql, engine)

            if save_filtered_data_to_csv:
                if not os.path.exists('outputs'):
                    os.makedirs('outputs')
                queried_df.to_csv('outputs/queried_data.csv', index=False)
                print('Source table data saved: outputs/queried_data.csv')
            
            if save_sql_to_txt:
                if not os.path.exists('outputs'):
                    os.makedirs('outputs')
                with open('outputs/sql_query.txt', 'w') as f:
                    f.write(sql)
                print('SQL query saved: outputs/sql_query.txt')

            if generate_response:
                generative_prompt_to_use = instructions._generate_base_generative_instructions(cleaned_query, queried_df) + '\n\n'
                if additional_generative_instructions:
                    if not isinstance(additional_generative_instructions, list):
                        raise ValueError('additional_generative_instructions must be a list of strings')
                    else:
                        generative_prompt_to_use += '\nADDITIONAL GENERATIVE INSTRUCTIONS:\n'
                        for instruction in additional_generative_instructions:
                            generative_prompt_to_use += instruction + '\n\n'
                response = client.chat.completions.create(
                    model="gpt-4-turbo",
                    messages= [
                        {"role": "system", "content": "You are a helpful research assistant."},
                        {"role": "user", "content": generative_prompt_to_use}
                    ],
                    temperature=1,
                    max_tokens=1024,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0,
                )
                print('\n','-'*20, ' GENERATIVE RESPONSE', '-'*20)
                print(response.choices[0].message.content)
                print('-'*50, '\n')
            else:
                print('\n','-'*20, 'SQL RESPONSE', '-'*20)
                print(f'SQL: {sql}')
                print(f'{queried_df.head()}')
                print('-'*50, '\n')