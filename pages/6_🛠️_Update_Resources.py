import streamlit as st
import os
from github import Github
import base64


#removable
def fillDB():
    import sqlite3 as sq
    import random
    from datetime import datetime

    def create_connection(db_file):
        conn = None
        try:
            conn = sq.connect(db_file)
            print(sq.version)
        except sq.Error as e:
            print(e)
        return conn

    def create_table(conn, table_sql):
        try:
            c = conn.cursor()
            c.execute(table_sql)
        except sq.Error as e:
            print(e)
            
    def generate_str_table(name):
        sql_create_table = f"CREATE TABLE IF NOT EXISTS {name} (\n"
        sql_create_table += "id INTEGER PRIMARY KEY,\n"
        sql_create_table += "velocity REAL NOT NULL,\n"
        sql_create_table += "day INTEGER NOT NULL,\n"
        sql_create_table += "timestamp TEXT NOT NULL\n"
        sql_create_table += ");"
        return sql_create_table

    def insert_create(conn, element, name):
        sql_insert = f"INSERT INTO {name}(id, velocity, day, timestamp) VALUES(?, ?, ?, ?)"
        cur = conn.cursor()
        cur.execute(sql_insert, (element["id"], element["velocity"], element["day"], element["timestamp"]))
        conn.commit()
        return cur.lastrowid
    day = random.randint(0,31)
    timed = datetime.now()
    table_name =  f"_{timed.year+5000}_{timed.month+1}_{day}"
    db = r".\test.db"
    conn = create_connection(db)


    if conn is not None:
        table = generate_str_table(table_name)
        create_table(conn, table)
        print("connection successful")
        
        
        for i in range(3):
            element = {
                "id": i,
                "velocity": random.randint(0, 10) + random.randint(0, 10)/10,
                "day": day,
                "timestamp": f"{random.randint(0, 23)}:{random.randint(0, 59)}:{random.randint(0, 59)}"
            }
            insert_create(conn, element, table_name)
            print("Inserting element")
    else:
        print("no connection established")
    print("DONE")
    conn.close()
#removable






st.set_page_config(
  page_title="Policumbent",
  page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLBnwH3bm6RwJvsl1-w4PDKxydP6wUIJNDs9pMaI1lpw&s", 
)
#code to hide streamlit normal view
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </stile>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

#/mount/src/policumbent-data-visualizer/database/new_db.db

#establish github object
g = Github(st.secrets["pat"])
# Then get the specific repo
repo = g.get_user().get_repo("Policumbent-Database")

# Get the ref for the file
contents = repo.get_contents("new_db.db")

os.chdir("/mount/src/policumbent-data-visualizer/database/")



def updateDB():
    import git
    
    repo = git.Repo(r"/mount/src/policumbent-data-visualizer/database/")
    username= "SamVia"
    password = st.secrets["pat"]
    remote = f"https://{username}:{password}@github.com/SamVia/Policumbent-Database"
    
    repo.git.add(os.path.realpath("new_db.db"))
    repo.index.commit("pushed db")

    origin = repo.remote(name="origin")
    origin.push()



if st.button("commit"):
    try:
        with open("/mount/src/policumbent-data-visualizer/database/new_db.db", "rb") as file:
            content = file.read()
            content_encoded = base64.b64encode(content)
    except Exception as e:
        st.write(e)
    try:
        repo.update_file(path=contents.path, message="updated database", content=content_encoded.decode(), sha=contents.sha)
        print("File updated successfully.")
    except Exception as e:
        st.write(e)
os.chdir("//mount/src/policumbent-data-visualizer/")

g.close()

if st.button("add row to db:"):
    fillDB()
    st.write("entry added")

st.write("update database:")
if st.button("update"):
    updateDB()