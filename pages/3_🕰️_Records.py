import streamlit as st
import sqlite3
import pandas as pd

st.set_page_config(
  page_title="Policumbent",
  page_icon="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLBnwH3bm6RwJvsl1-w4PDKxydP6wUIJNDs9pMaI1lpw&s",
  layout="centered" 
)
#code to hide streamlit normal view
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    </stile>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)
footer="""<style>
.footer {
-webkit-user-select: none; 
-moz-user-select: none; 
-ms-user-select: none; 
user-select: none; 
position: fixed;
right: -7vh;
bottom: 0;
width: 100%;
background-color: transparent;
color: rgba(128,128,128,0.6);
text-align: left;
}
</style>
<div class="footer">
<p>Version 1.0.0<a style='display: block; text-align: right;</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
# with st.sidebar:
#     st.sidebar.markdown("""<style>
# .reportview-container .main .block-container {
#     max-width: 120px;
#     padding-top: 2rem;
#     padding-right: 2rem;
#     padding-left: 2rem;
#     padding-bottom: 10rem;
# }
# .footer {
#     position: absolute;
#     bottom: -87vh;
#     width: 100%;
#     text-align: center;
#     color:rgba(128,128,128,0.6);
#     font-weight: bold;  
#     font-size: 2.5vh; 
# }
# </style>
# <p class="footer">Version 1.0.0</p>
# """, unsafe_allow_html=True)
def connect_to_db():
    """Connect to SQLite database

    Returns:
        sqlite3 connection: connection to database
    """
    return sqlite3.connect(r'/mount/src/policumbent-data-visualizer/database/new_db.db')

# List of tables in the database
def get_table_names(_conn):
    """extracts all names present in the database

    Args:
        _conn (sqlite3 connection)

    Returns:
        list: table names
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names

def convert_table_name(table_name):
    """converts table names from '_yyyy_mm_dd to dd/mm/yyyy
    """
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
average_velocity = round(df['velocity'].mean(),2)
max_velocity = df['velocity'].max()
# Display the retrieved data for debugging
st.write("DataFrame:")
st.dataframe(df, use_container_width=True, hide_index=True)

# Plot the data if DataFrame is not empty
if not df.empty:
    st.write(f'## Average velocity: {average_velocity} km/h')
    st.write(f'## Maximum velocity: {max_velocity} km/h')
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