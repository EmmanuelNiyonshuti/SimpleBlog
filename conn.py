# testing connection to postgresql  hosted on render 
import psycopg2

try:
    conn = psycopg2.connect(
        dbname="blog_dev_db",
        user="blog_dev",
        password="lzlcp1Xtm47s6TdzkFTDYQ2TXt81YE1R",
        host="dpg-cqagrllds78s739s3040-a.oregon-postgres.render.com"
    )
    print("Connection successful")
except Exception as e:
    print(f"Connection failed: {e}")

