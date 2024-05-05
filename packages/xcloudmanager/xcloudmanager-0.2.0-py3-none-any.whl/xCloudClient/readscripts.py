def read_multi_sql_file(file_path):
    """
    Read a SQL file containing multiple scripts separated by colons,
    and return a list of the scripts.
    """
    # Read SQL file and split scripts by colon
    with open(file_path, 'r',encoding= 'utf -8') as file:
        sql_content = file.read()

    # Split SQL scripts by colon and remove empty strings
    sql_scripts = [script.strip() for script in sql_content.split('\n;') if script.strip()]

    return sql_scripts

#if __name__ == "__main__":
    ## Example usage
    #file_path = 'multi_script.sql'
    #scripts = read_multi_sql_file(file_path)
    #for idx, script in enumerate(scripts, start=1):
        #print(f'Script {idx}:')
        #print(script)
        #print('-' * 20)
