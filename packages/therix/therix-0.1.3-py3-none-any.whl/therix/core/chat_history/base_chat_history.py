from typing import Optional
import uuid
from langchain_core.messages import AIMessage
import psycopg
from requests import session
from sqlalchemy import Engine
from therix.db.session import SQLALCHEMY_DATABASE_URL,engine
import logging
from langchain_postgres import PostgresChatMessageHistory
logger = logging.getLogger(__name__)

class TherixChatMessageHistory(PostgresChatMessageHistory):
   
    def __init__(
        self,
        session_id,
        pipeline_id:str,
        engine,
        table_name: str,
        
    ): 
         self.sync_connection = psycopg.connect(SQLALCHEMY_DATABASE_URL)
         super().__init__(table_name,session_id,sync_connection=self.sync_connection)
         self.session_id = session_id
         self.table_name = table_name
         self.pipeline_id=pipeline_id
         
    
    def add_message(self,message_role, message,pipeline_id,session_id):
         try:
             id=uuid.uuid4()
             cursor=self.sync_connection.cursor()
             insert_query=f"""INSERT INTO {self.table_name} (id, message_role,  message, pipeline_id, session_id) VALUES (%s ,%s, %s, %s, %s);"""
             cursor.execute(insert_query,(id,message_role, message,pipeline_id,session_id))
             self.sync_connection.commit()
             cursor.close()
             
         except (Exception, psycopg.DatabaseError) as e:
             logging.error(e)
            

