import streamlit as st
import sqlite3
import pandas as pd

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

def connect_to_db():
# Connect to SQLite database
  return sqlite3.connect(r'/mount/src/policumbent-data-visualizer/test.tb')

# List of tables in the database
@st.cache_data()
def get_table_names(_conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names

def convert_table_name(table_name):
    parts = table_name.split("_")
    year = int(parts[1])
    month = int(parts[2])
    day = int(parts[3])
    date = f"{day}/{month}/{year}"
    return date
# Retrieve table names
conn = connect_to_db()
tables = get_table_names(conn)
formatted_table_names = [convert_table_name(table_name) for table_name in tables]
# Select a table
option =  st.selectbox('Select a table', range(len(formatted_table_names)), format_func=lambda i: formatted_table_names[i])

# Query the database for the selected columns
query = f"SELECT id, velocity, timestamp FROM {tables[option]}"
df = pd.read_sql_query(query, conn)

# Display the retrieved data for debugging
st.write("DataFrame:")
st.dataframe(df, use_container_width=True, hide_index=True)

# Plot the data if DataFrame is not empty
if not df.empty:
    st.write(f'## Plot of velocity over ID')
    st.line_chart(df.set_index('id')['velocity'])
    "-------"
    st.scatter_chart(df, x='id', y='velocity')
    "-------"
    st.area_chart(df.set_index('id')['velocity'])
    "-------"
    st.bar_chart(df.set_index('id')['velocity'])

else:
    st.write("DataFrame is empty.")

# Close the connection
conn.close()
