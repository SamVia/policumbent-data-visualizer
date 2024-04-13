import streamlit as st 
from google.cloud import firestore
import time
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

@st.cache_resource
def connect_to_db():
	return firestore.Client.from_service_account_json("firestone-key.json")
#use caching to avoid establishing the connection every rerun of the app

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
    
    
def cleanDB(db):
    '''
    erases all data in the database, used for testing purposes
    '''
    try:
        doc_ref = db.collection("test1")#use name of the current collection WARNING it will erase all data in that collection
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
    	
def templateDB(db):
    '''
    create an instance in the database with temp data, can be used to test working conditions and see how data is represented.
    '''
    try:
        doc_ref = db.collection("test1").document("template")
        doc_ref.set({
            "id":0,
            "velocity": 1,
            "day": 11,
            "timestamp": 123
        })
        return "template created"
    except:
        pass

db = connect_to_db() # establish connection


#if number of same instances is less than 10 execute queries else idle 
if st.session_state.same_read < 10:
    #query for data: gets data from "insert_name" in descending order (Higher to Lower), then limited to 6
    #from testing 6 seems the right amount, with 5 there seems to be around 0.6% loss of ids with 6 out of 3 tests there has been 0 loss
	data = db.collection("test1").order_by("id",direction=firestore.Query.DESCENDING).limit(6).get()
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
else:
    print(f"{st.session_state.same_read}:max number of same query done!")   

	

if st.button("delete"):
    #temp
    st.write(cleanDB())

if st.button("create"):
    #temp
    st.write(templateDB())

df = pd.DataFrame(st.session_state.collection)
col1, col2 = st.columns(2)
col1.dataframe(df, use_container_width=True, hide_index=True)
if len(st.session_state.collection) > 0:
    #check if it possible to form an average and current velocity
    speed = st.session_state.collection[0]["velocity"]
    col2.write(f"current speed: {speed}m/s")
    col2.divider()
    col2.write(f"average speed: {round(st.session_state.average/len(st.session_state.collection),2)}m/s")
time.sleep(1)

col1.empty()
st.rerun()


