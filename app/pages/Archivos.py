import streamlit as st

st.set_page_config(layout='wide', page_title='Archivos - Basdonax AI RAG', page_icon='📁')

import chromadb, os
from langchain_community.embeddings import HuggingFaceEmbeddings
from chromadb.config import Settings
from common.chroma_db_settings import get_unique_sources_df
from common.ingest_file import ingest_file, delete_file_from_vectordb
from common.streamlit_style import hide_streamlit_style

hide_streamlit_style()

# Define the Chroma settings
CHROMA_SETTINGS = chromadb.HttpClient(host="host.docker.internal", port = 8000, settings=Settings(allow_reset=True, anonymized_telemetry=False))
collection = CHROMA_SETTINGS.get_or_create_collection(name='vectordb')
embeddings = HuggingFaceEmbeddings(model_name='all-MiniLM-L6-v2')

st.title('Archivos')

# Carpeta donde se guardarán los archivos en el contenedor del ingestor
container_source_directory = 'documents'

# Función para guardar el archivo cargado en la carpeta
def save_uploaded_file(uploaded_file):
    # Verificar si la carpeta existe en el contenedor, si no, crearla
    if not os.path.exists(container_source_directory):
        os.makedirs(container_source_directory)

    with open(os.path.join(container_source_directory, uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())
    return os.path.join(container_source_directory, uploaded_file.name)

# Widget para cargar archivos
uploaded_files = st.file_uploader("Cargar archivo", type=['csv', 'doc', 'docx', 'enex', 'eml', 'epub', 'html', 'md', 'odt', 'pdf', 'ppt', 'pptx', 'txt'], accept_multiple_files=False)

# Botón para ejecutar el script de ingestión
if st.button("Agregar archivo a la base de conocimiento") and uploaded_files:
    file_name = uploaded_files.name
    ingest_file(uploaded_files, file_name)
elif not uploaded_files:
    st.write("Por favor carga al menos un archivo antes agregar archivo a la base de conocimiento.")

st.subheader('Archivos en la base de conocimiento:')

files = get_unique_sources_df(CHROMA_SETTINGS)
files['Eliminar'] = False
files_df = st.data_editor(files, use_container_width=True)
if len(files_df.loc[files_df['Eliminar']]) == 1:
    st.divider()
    st.subheader('Eliminar archivo')
    file_to_delete = files_df.loc[files_df['Eliminar'] == True]
    filename = file_to_delete.iloc[0, 0]
    st.write(filename)
    st.dataframe(file_to_delete, use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
                
    with col2:
        if st.button('Eliminar archivo de la base de conocimiento'):
            try:
                delete_file_from_vectordb(filename)
                st.success('Archivo eliminado con éxito')
                st.rerun()
            except Exception as e:
                st.error(f'Ocurrió un error al eliminar el archivo: {e}')
    
elif len(files_df.loc[files_df['Eliminar']]) > 1:
    st.warning('Solo se permite eliminar un archivo a la vez.')
                


