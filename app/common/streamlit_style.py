import streamlit as st


def hide_streamlit_style():
    """Oculta los estilos por defecto de Streamlit."""
    hide_st_style = """
        <style>
            .reportview-container {
                margin-top: -2em;
            }
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)