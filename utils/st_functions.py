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

    n = len(results)
    if n > 1:
        with st.container(height=500):
            # Só imprime os 20 primeiros para reduzir custo de processamento
            st.code(
                json.dumps(results[1:20], ensure_ascii=False, indent=4), language="json"
            )
    st.write((f"Esse processamento analisou {n} documentos e durou {d} segundos"))
    st.write(f"Uma média de {m} segundos por documento")


def write_fisrt_result(results):
    st.subheader("", divider="yellow")
    st.subheader("Resultados")
    st.code(json.dumps(results[0], ensure_ascii=False, indent=4), language="json")


def download_results():

    st.warning(
        "Atenção: Está impresso na tela apenas uma amostra inicial, para conferir o resultado completo:"
    )
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


def examples():
    st.subheader("", divider="yellow")
    st.subheader("Exemplos de arquivos para upload")

    # Download de mais de um arquivo complica a UX (envolve .zip)
    # portanto enviarei apenas o exemplo do Dr. Kakaroto
    col1, col2, _ = st.columns(3)
    with col1:
        with open("data/um_so.json", "r") as f1:
            dataset_exemple = f1.read()

        st.download_button(
            label="extraction_schema",
            data=dataset_exemple,
            file_name="dataset_exemplo.json",
            mime="application/json",
            icon=":material/download:",
        )

    with col2:

        with open("data/files/oab_3.pdf", "rb") as f2:
            pdf_exemple = f2.read()

        st.download_button(
            label="Arquivos PDF",
            data=pdf_exemple,
            file_name="exemplo_oab_3.pdf",
            mime="application/pdf",
            icon=":material/download:",
        )

    st.warning(
        "Use esses arquivos como referencia de como devem ser os inputs desse sistema"
    )


def footer():
    st.subheader("", divider="yellow")
    st.markdown("Desenvolvido em novembro de 2025")
    st.markdown("Mais projetos [meu Github](https://github.com/gabeguidoni)")
    st.markdown("Contato [gabeguidoni@gmail.com](mailto:gabeguidoni@gmail.com)")
    st.markdown(
        "Saba mais [sobre mim](https://www.linkedin.com/in/gabriel-guidoni-7b3b27208/)"
    )
