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


# Connect to SQLite database
conn = sqlite3.connect('test.db')

# List of tables in the database
def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names

# Retrieve table names
tables = get_table_names(conn)

# Select a table
option = st.selectbox(
    'Which table do you want to visualize?',
    tables
)

# Query the database for the selected columns
query = f"SELECT id, velocity, timestamp FROM {option}"
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
