import requests, json, os
import streamlit as st


def check_api_key(api_key: str) -> bool:
    """
    Confere se a chave enviada é valida no site da OpenAi
    """
    url = "https://api.openai.com/v1/models"
    headers = {"Authorization": f"Bearer {api_key}"}
    r = requests.get(url, headers=headers)

    if r.status_code == 200:
        st.success("Chave válida")
        return True
    else:
        st.error("Chave inválida")
        return False


def check_files(json_schema, pdf_files: list[object]) -> bool:
    """
    Confere se:
    - O numero de PDFs é o mesmo que o de dicionarios no json_schema
    - Os arquivos nomeados no schema sao os mesmos que foram enviados
    """
    try:
        dicis = json.load(json_schema)
        json_schema.seek(0)  # retorna o ponteiro para o inicio
        num_dicts = len(dicis)
        num_pdfs = len(pdf_files)

        pdf_names = [pdf_file.name for pdf_file in pdf_files]
        json_names = [dici["pdf_path"] for dici in dicis]

        if num_pdfs != num_dicts:
            st.error(f"{num_pdfs} PDFs enviados para {num_dicts} extraction_schemas")
            return False
        elif set(pdf_names) != set(json_names):
            st.error(f"Arquivos no json_schema sao diferentes dos enviados.")
            return False
        else:
            st.success("Arquivos válidos")
            return True
    except:
        st.error(f"Algum arquivo fora do padrão, confira os exemplos.")
        return False


def write_results(results, d, m):
    st.subheader("", divider="yellow")
    st.subheader("Resultados")

    n = len(results)
    with st.container(height=500):
        # Só imprime os 20 primeiros para reduzir custo de processamento
        st.code(json.dumps(results[:20], ensure_ascii=False, indent=4), language="json")
    st.write((f"Esse processamento analisou {n} documentos e durou {d} segundos"))
    st.write(f"Uma média de {m} segundos por documento")


def download_results():

    pasta = "data/outputs"
    arquivos = [f"{pasta}/{f}" for f in os.listdir(pasta)]
    if arquivos:
        arquivo = max(arquivos, key=os.path.getmtime)
        with open(arquivo, "rb") as f:
            result_file = f.read()

        st.download_button(
            label="Baixe o resultado completo",
            data=result_file,
            file_name="result_file.json",
            mime="application/json",
            icon=":material/download:",
            help="Baixe o resultado completo em arquivo .json",
        )


def header():
    st.set_page_config(
        page_title="Projeto - Kadem Gabriel Aidar",
        layout="centered",
        page_icon="data/images/logo_enter.png",
    )
    st.logo("data/images/logo_enter.png", size="large")
    st.title("ENTER AI FELLOWSHIP")
    st.text("Candidato: Kadem Gabriel Aidar - gabeguidoni@gmail.com")


def ftab1():
    st.header("README.md", divider="yellow")

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    st.markdown(content, unsafe_allow_html=False)


def footer():
    st.subheader("", divider="yellow")
    st.markdown(
        "Desenvolvido em novembro de 2025  \n[Meu Github](https://github.com/gabeguidoni)"
    )
