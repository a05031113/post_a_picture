import boto3
from pydantic import *
from botocore.client import Config
from dotenv import load_dotenv
import mysql.connector as connector
import os
load_dotenv()


class r2:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            region_name="us-east-1",
            aws_access_key_id=os.getenv("s3_access_key_id"),
            aws_secret_access_key=os.getenv("s3_secret_access_key"),
            config=Config(signature_version='s3v4')
        )

    def get_put_url(self, file_name):
        response = self.s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": "season3-for-wehelp-homework",
                "Key": file_name,
            },
            ExpiresIn=3600
        )
        return {"url": response}


class rds:
    def __init__(self):
        self.db = connector.connect(
            pool_name="mypool",
            pool_size=5,
            host="database.cntj9qhawnrn.us-east-1.rds.amazonaws.com",
            user="admin",
            password=os.getenv("sql_password"),
            database="RDS"
        )

    def select(self):
        cursor = self.db.cursor(buffered=True, dictionary=True)
        cursor.execute("""
            SELECT msg, imgURL, time 
            FROM season3
            order by time DESC 
            """)
        output = cursor.fetchall()
        cursor.close()
        self.db.close()
        return output

    def select_new(self):
        cursor = self.db.cursor(buffered=True, dictionary=True)
        cursor.execute("""
            SELECT msg, imgURL, time 
            FROM season3
            order by time DESC 
            LIMIT 1
            """)
        output = cursor.fetchone()
        cursor.close()
        self.db.close()
        return output

    def insert(self, msg, imgURL):
        cursor = self.db.cursor()
        insert = """
            INSERT INTO season3
            (msg, imgURL)
            VALUE (%s, %s)
            """
        value = (msg, imgURL)
        cursor.execute(insert, value)
        self.db.commit()
        cursor.close()
        self.db.close()
        return True


class Data(BaseModel):
    msg: str
    imgName: str
