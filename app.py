from utils.st_functions import (
    check_api_key,
    header,
    ftab1,
    examples,
    footer,
    check_files,
    write_results,
    download_results,
)
from main import main
import streamlit as st
import asyncio, json

header()

# ====================== BODY


tab1, tab2 = st.tabs(["💡 Introdução", "🔧 Ferramenta"])

with tab1:
    ftab1()

with tab2:
    st.header("TAKE HOME PROJECT", divider="yellow")

    st.markdown("Cole sua **chave para a API** do gpt-5-mini")
    api_key = st.text_input("", label_visibility="collapsed", type="password")

    valid_key = False
    if api_key:
        valid_key = check_api_key(api_key)

    st.write("Coloque o **extraction_schema**, em formato .json")
    json_schema = st.file_uploader(
        "",
        label_visibility="collapsed",
        type="json",
        accept_multiple_files=False,
        help="O json deve conter uma lista de dicionarios",
    )

    st.write("Coloque os **Arquivos PDF**")
    pdf_files = st.file_uploader(
        "",
        label_visibility="collapsed",
        type="pdf",
        accept_multiple_files=True,
        help="Deve ser enviado o mesmo número de arquivos que dicionários no json_schema",
    )

    valid_files = False
    if (json_schema and not pdf_files) or (pdf_files and not json_schema):  # XOR?
        st.warning("Preencha todos os campos")
    elif json_schema and pdf_files:
        valid_files = check_files(json_schema, pdf_files)

    d = True
    if valid_key and valid_files:
        d = False

    h = "Preencha todos os campos para ativar esse botão."
    submitted = st.button("Executar Extração", type="primary", disabled=d, help=h)

    if submitted:
        results, d, m = asyncio.run(main(api_key, json.load(json_schema), pdf_files))
        write_results(results, d, m)
        download_results()

    # ====================== EXEMPLOS
    if not submitted:
        examples()

# ====================== RODAPE

footer()
