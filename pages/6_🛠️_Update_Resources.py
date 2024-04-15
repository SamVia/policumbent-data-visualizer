import streamlit as st
import os
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
def updateDB():
    import git
    
    repo = git.Repo(r"/mount/src/policumbent-data-visualizer/")
    username= "SamVia"
    password = "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"
    remote = f"https://{username}:{password}@github.com/SamVia/test_python"
    
    repo.git.add(os.path.realpath("test.db"))
    repo.index.commit("pushed db")

    origin = repo.remote(name="origin")
    origin.push()


st.markdown(hide_st_style, unsafe_allow_html=True)
st.write("update database:")
if st.button("update"):
    updateDB()
st.write(os.path.realpath("test.db"))