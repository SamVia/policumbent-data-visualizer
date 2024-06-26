import streamlit as st 
from google.cloud import firestore
import time
import pandas as pd
import json
from google.oauth2 import service_account
import sqlite3 as sq

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

if "current_name" not in st.session_state:
	#check if the current date is in the database
	from datetime import datetime
	current = datetime.now()
	st.session_state.current_name = f"_{current.year}_{current.month}_{current.day}"



#use caching to avoid establishing the connection every rerun of the app
@st.cache_resource
def connect_to_db():
	key_dict = json.loads(st.secrets["textkey"])
	creds = service_account.Credentials.from_service_account_info(key_dict,)
	credentials = firestore.Client(credentials=creds)
	t_names = credentials.collections()
	names = []
	for n in t_names:
		names.append(n.id)
	return credentials, names


def get_table_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names


#declaration of some state variables that will persists on reruns:
if "collection" not in st.session_state:
	#used to merge all the data extracted from the database
	st.session_state.collection = []
if "average" not in st.session_state:
	#used to sum all speed data which will be later divided by the number of data in the list
	st.session_state.average = 0
if "read_ids" not in st.session_state:
	#used to check the last window of reads, easier than running the whole list to search for a possible match
	st.session_state.read_ids = []
if "same_read" not in st.session_state:
	#counter to avoid making new queries if the data stream is over
	st.session_state.same_read = 0
if "First" not in st.session_state:
	st.session_state.First = True	

def firstRead(db):
	'''
	reads the db once at the start, prevents a loss of initial data streamed, it is added in bulk not real time.
	'''
	try:
		data = db.collection(st.session_state.current_name).order_by("id",direction=firestore.Query.ASCENDING).get()
		if len(data)>0:
			current_read = []
			
			for r in data:
				r_td = r.to_dict() #transform r object in data to a dict
				current_read.append(r_td["id"])

				if r_td["id"] not in st.session_state.read_ids:
					#only if the id is not yet in the list of the previously read ids it is then added to the list of known data
					st.session_state.collection.insert(0, r_td)
					st.session_state.average += r_td["velocity"]
		st.session_state.read_ids = [current_read[-1],current_read[-2],current_read[-3]]
		return current_read
	except:
		pass

def cleanDB(db):
	'''
	erases all data in the database, used for testing purposes
	'''
	try:
		doc_ref = db.collection(st.session_state.current_name)#use name of the current collection WARNING it will erase all data in that collection
		for doc in doc_ref.stream():
			doc_ref.document(doc.id).delete()
		#cleanup of variables
		st.session_state.collection = []
		st.session_state.average = 0
		st.session_state.read_ids = []
		st.session_state.same_read = 0
		return "cleaning done"
	except:
		pass

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


def updateDB(data, name):
	conn = sq.connect(r'/mount/src/policumbent-data-visualizer/database/new_db.db')
	if conn is not None:
		
		names = get_table_names(conn)
		if name in names:
			return #no need to update 
		else:
			if len(data)>0: #check if there are fields, if not it could be initialized for future uses only
				table = generate_str_table(name)
				create_table(conn, table)
				print("connection successful")
				for d in data:
					d_to_dict = d.to_dict()
					insert_create(conn, d_to_dict, name)
					print("Inserting element")

	else:
		print("no connection established")
	

def templateDB(db):
	'''
	create an instance in the database with temp data, can be used to test working conditions and see how data is represented.
	'''
	try:
		doc_ref = db.collection(st.session_state.current_name).document("template")
		doc_ref.set({
			"id":0,
			"velocity": 1,
			"day": 11,
			"timestamp": 123
		})
		return "template created"
	except:
		pass
def collection(delay):
	"""
	writes the table + current average and max speed if possible
	"""
	df = pd.DataFrame(st.session_state.collection)
	col1, col2 = st.columns(2)
	col1.dataframe(df, use_container_width=True, hide_index=True)
	if len(st.session_state.collection) > 1:
		#check if it possible to form an average and current velocity
		speed = st.session_state.collection[0]["velocity"]
		col2.write(f"current speed: {speed}m/s")
		col2.divider()
		col2.write(f"average speed: {round(st.session_state.average/len(st.session_state.collection),2)} km/h")
		col2.divider()
		col2.write(f'maximum speed: {max(st.session_state.collection, key=lambda x:x["velocity"])["velocity"]} km/h')

	if delay>0:
		time.sleep(delay)
		col1.empty()

db, names = connect_to_db() # establish connection
#buttons for testing purposes may be useful in the future.
# if st.button("delete"):
# 	#test
# 	st.write(cleanDB(db))

# if st.button("create"):
# 	#test
# 	st.write(templateDB(db))
st.header("Streaming Data:")

#check first if today's table name is in the database, then continue with normal execution	
if st.session_state.current_name in names:
	if st.session_state.First:
		first = firstRead(db)
		collection(0.2)
		
		st.session_state.First = False
		st.rerun()
	#if number of same instances is less than 100 (20s) execute queries else idle 
	while st.session_state.same_read < 30:
		#query for data: gets data from "insert_name" in descending order (Higher to Lower), then limited to 6
		#from testing 3 seems the right amount, with 2 there seems to be around 0.6% loss of ids, with 3 out of 5 tests there has been 0 loss
		data = db.collection(st.session_state.current_name).order_by("id",direction=firestore.Query.DESCENDING).limit(3).get()
		#check on data len -> if 0 there has been 0 matches

		if len(data)>0:
			current_read = []
			
			for r in data:
				r_td = r.to_dict() #transform r object in data to a dict
				current_read.append(r_td["id"])

				if r_td["id"] not in st.session_state.read_ids:
					#only if the id is not yet in the list of the previously read ids it is then added to the list of known data
					st.session_state.collection.insert(0, r_td)
					st.session_state.average += r_td["velocity"]
			if current_read == st.session_state.read_ids:
				st.session_state.same_read += 1 #match in the previously read and currently read increases +1
			else:
				st.session_state.read_ids = current_read
				st.session_state.same_read = 0

		collection(0.2)

		st.rerun()
	else:
		#when entering the final stage, current day data is being displayed for the whole day
		st.write("final stage")
		collection(-1)

		with st.spinner("updating database"):
			#for each name in the database collection checks, if there is already data saved, then updates the local db, readying it for commit
			for name in names:
				updateDB(name=name, data = db.collection(name).order_by("id",direction=firestore.Query.ASCENDING).get())
		st.success("updating done!")
else:
	st.header("No race today, we can rest!")
	if st.button("check if race started", key="clear_cache"):
		st.cache_resource.clear()