import os
import sys
import yaml

directory_path = sys.argv[1]

os.chdir(f'{directory_path}')

os.system(f'snow snowpark build')
os.system(f'snow snowpark deploy --replace --temporary-connection --account $SNOWFLAKE_ACCOUNT\
             --user $SNOWFLAKE_USER --password $SNOWFLAKE_PASSWORD --database $SNOWFLAKE_DATABASE\
             --warehouse $SNOWFLAKE_WAREHOUSE --role $SNOWFLAKE_ROLE')
