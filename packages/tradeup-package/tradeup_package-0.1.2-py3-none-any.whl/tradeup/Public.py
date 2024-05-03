import pymsteams
import awswrangler as wr
import pandas as pd
import numpy as np
import sqlalchemy
import datetime
import os
import ast
import boto3
from botocore.exceptions import ClientError
import redshift_connector
import pymysql
import calendar
from sqlalchemy import create_engine, MetaData, text


def onError(title, destination, assignee, error_message, script_name, script_location):
    myTeamsMessage = pymsteams.connectorcard(destination)
    # create the section
    myMessageSection = pymsteams.cardsection()
    # Activity Elements
    myMessageSection.activityTitle(title)
    myMessageSection.activitySubtitle("production pipeline alert")
    myMessageSection.activityImage("https://teamsnodesample.azurewebsites.net/static/img/image4.png")
    # Facts are key value pairs displayed in a list.
    myMessageSection.addFact("Assignning to", assignee)
    myMessageSection.addFact("Error Message", error_message)
    myMessageSection.addFact("Script Name", script_name)
    myMessageSection.addFact("Script Location", script_location)
    # Add your section to the connector card object before sending
    myTeamsMessage.addSection(myMessageSection)
    myTeamsMessage.summary(title)
    myTeamsMessage.send()



def clear_table(date, table_name=None, db_name=None, user=None, password=None, IP_address=None, port=None):
    db = pymysql.connect(host = IP_address, user = user, passwd = password, database = db_name, port = port, charset='utf8')
    try:
        cursor = db.cursor()
        cursor.execute(f'''
            delete FROM {table_name}
            where Date = '{date}';
                                
        ''')
        db.commit()
        print(f'clear table {table_name}: 1')
    except Exception as e:
        print(e)
    finally:
        db.close()

def insert_db(df=None, table_name=None, db_name=None, user=None, password=None, IP_address=None, port=None):
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{IP_address}:{port}/{db_name}")  
    try:
        df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f'{table_name} ingestion: 1')
    except Exception as e:
        raise ValueError(e)
    finally:
        engine.dispose()
        
        
def last_business_day(year, month):
    last_day = calendar.monthrange(year, month)[1]
    day = datetime.date(year, month, last_day)
    while day.weekday() > 4:
        day -= datetime.timedelta(days=1)
    return day


def data_pull(user=None, password=None, IP_address=None, port=None, db_name=None, SQL_query=None):
    try:
        # Create the SQLAlchemy engine
        engine = create_engine(f"mysql+pymysql://{user}:{password}@{IP_address}:{port}/{db_name}") 

        # Execute the SQL query
        query = f"{SQL_query}"
        df = pd.read_sql_query(query, engine)
        return df    
    except Exception as e:
        raise ValueError(e)
    finally:
        engine.dispose()
        



def to_float(series):
    new_lst = []
    lst = list(series)
    for i in lst:
        if i == "" or type(i) == float:
            new_lst.append(np.nan)
        else:
            if "-" in i:
                i = i.replace(",","").replace("-","").replace(" ","")
                i = float(i) * (-1)
                new_lst.append(i)
            else:
                i = i.replace(",","").replace(" ","")
                new_lst.append(float(i))
    return new_lst




    

class amazon():
    @staticmethod
    def get_secret(secret_name, region_name):
        # Create a Secrets Manager client
        session = boto3.session.Session()
        client = session.client(service_name='secretsmanager',region_name=region_name)
        try:
            get_secret_value_response = client.get_secret_value(
                SecretId=secret_name
            )
        except ClientError as e:
            raise e
    
        password = get_secret_value_response['SecretString']
        return password    
    
    @staticmethod
    def check_holiday(date_obj, con, which='NYSE_Holiday'):
        date_str = date_obj.strftime("%Y-%m-%d")
        df = wr.redshift.read_sql_query(
            sql=f"""
                SELECT "{which}" FROM Holiday.Holiday WHERE "Date" ='{date_str}'
                """,
            con=con
        )
        
        # not in holiday list
        if len(df) == 0:
            return False
        
        # in holiday list and decide
        if df.iloc[0,0] == 1:
            return True
        else:
            return False
        
    @staticmethod
    def data_pull(sql_query, con, indicator):
        data = wr.redshift.read_sql_query(
            sql=sql_query,
            con=con
        )

        print(indicator)
        return data
    
    @staticmethod
    def sql_execute(sql_query, con, indicator):
        cursor: redshift_connector.Cursor = con.cursor()
        cursor.execute(sql_query)
        
        print(indicator)     

    @staticmethod
    def insert_table(db_params, data, con, method, mode, dtype, schema = None, table=None):
        if schema is None:
            schema = db_params['schema_name']
        if table is None:
            table=db_params['table_name']
        if method == 'copy':
            wr.redshift.copy(
                df = data,
                path =f's3://tradeup-it/parquet/{schema}/{table}',
                schema=schema,
                table=table,
                con=con,
                mode=mode, #  Append, overwrite or upsert
                use_column_names = True,
                index=False,
                dtype=dtype # Optional: specify column data types
            )
            print(f'insert: 1')
        elif method == 'to_sql':
            wr.redshift.to_sql(
                df = data,
                schema=schema,
                table=table,
                con=con,
                mode=mode, #  Append, overwrite or upsert
                use_column_names = True,
                index=False # Typically, you don't want DataFrame indexes in your database table
                #dtype={"column1": "INTEGER", "column2": "VARCHAR(255)"} # Optional: specify column data types
            )             
            print('insert: 1')   