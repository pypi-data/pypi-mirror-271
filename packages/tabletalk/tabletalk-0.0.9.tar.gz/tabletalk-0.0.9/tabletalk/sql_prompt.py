SQL_PROMPT = f"""
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
"""

            # sql_prompt_to_use += 'award_amount is not a column you can use.\n'
            # sql_prompt_to_use += 'Write a SQL query using only existing columns from the specified tables. Do not create or infer new columns.\n'
            # sql_prompt_to_use += 'The SQL query should be general enough for use on any dataset with similar structure.\n'
            # sql_prompt_to_use += 'Use only one SQL statement per query and ensure all SQL syntax is compatible with SQLite.\n'
            # sql_prompt_to_use += 'All string comparisons should be in lowercase. For example, use WHERE LOWER(column_name) LIKE \'%value%\' instead of WHERE column_name LIKE \'%Value%\'.\n'
            # sql_prompt_to_use += 'Use WHERE column_name IN (\'value1\', \'value2\') for multiple specific values, rather than multiple LIKE clauses.\n'
            # sql_prompt_to_use += 'Include only necessary columns in your SELECT statement to minimize data extraction.\n'
            # sql_prompt_to_use += 'Use SQL functions like DISTINCT, WHERE, GROUP BY, ORDER BY, LIMIT, JOIN, and UNION as needed to refine the data return.\n'
            # sql_prompt_to_use += 'Structure the response as a Python dictionary with the key \'sql\' leading to the SQL query string.\n\n'
            # sql_prompt_to_use += 'RESPONSE INSTRUCTIONS:\n'
            # sql_prompt_to_use += 'The response should only include the Python dictionary. Exclude code block markers like \'```\'.\n'
            # sql_prompt_to_use += 'The output dictionary should validate as a dictionary type in Python: type(eval(response)) == dict.'

