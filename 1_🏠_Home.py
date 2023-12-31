import streamlit as st

st.set_page_config(
  page_title="Policumbent",
  page_icon="https://blog.smartcae.com/admin/wp-content/uploads/2.png", 
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

st.write("home")