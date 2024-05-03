import streamlit as st

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
position: fixed;
right: 7vh;
bottom: 0;
width: 100%;
background-color: transparent;
color: rgba(128,128,128,0.6);
text-align: right;
}
</style>
<div class="footer">
<p>Version 1.0.0<a style='display: block; text-align: right;</p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)


# st.sidebar.markdown("""<style>
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




"""settings will be added in future release
"""