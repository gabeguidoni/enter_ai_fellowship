import json, fitz
from pydantic import create_model
from datetime import datetime
from pathlib import Path


# TODO: fazer um pre-tratamento no texto removendo letras avulsas
# TODO: alertar de alguma forma se nao for extraido texto algum
def _get_file_text(file_name: str, pdf_files: list[object] = None) -> str:

    if not pdf_files:
        path = f"data/files/{file_name}.pdf"
        return fitz.open(path).get_page_text(0)

    pdf_file = next((f for f in pdf_files if f.name == file_name), None)

    if pdf_file:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            return doc[0].get_text()
    else:
        return ""


def _preprocess_dataset_json(json_schemas=None) -> list[tuple[str, object]]:

    if not json_schemas:
        with open("data/dataset.json", "r", encoding="utf-8") as f:
            json_schemas = json.load(f)

    if isinstance(json_schemas, dict):
        json_schemas = [json_schemas]

    batatas = []
    for item in json_schemas:
        file_name: str = item["pdf_path"]
        class_name = file_name.title().replace("_", "").rsplit(".")[0]
        extraction_keys = list(item["extraction_schema"].keys())
        SchemaClass = create_model(
            f"Schema{class_name}",
            **{k: (str, "") for k in extraction_keys},
        )
        batatas.append((file_name, SchemaClass))

    return batatas


def build_prompts(
    json_schemas, pdf_files: list[object]
) -> list[dict[str, str | object]]:
    batatas = _preprocess_dataset_json(json_schemas)

    prompts = []
    for batata in batatas:
        file_text = _get_file_text(batata[0], pdf_files)

        prompts.append(
            {
                "texto_doc": file_text,
                "schema": batata[1],
            }
        )
    return prompts


def print_results(results: list[str]) -> None:
    for result in results:
        print(json.dumps(result, ensure_ascii=False, indent=4))


def print_duration(inicio, fim, quant) -> tuple[float, float]:
    """
    Retorna:
    - duração de todo o processamento
    - media de tempo para cada arquivo
    """
    print(10 * "=")
    duracao = round(fim - inicio, 2)
    # print(f"Esse processamento analisou {quant} documentos e durou {duracao} segundos")
    media = round((fim - inicio) / quant, 5)
    # print(f"Uma média de {media} segundos por documento")
    return (duracao, media)


def save_results(results, folder_path="data/outputs"):

    folder_path = Path(folder_path)  # vai que...
    folder_path.mkdir(parents=True, exist_ok=True)

    # esse desafio só deve rodar por poucos dias, nao precisa salvar mes e ano
    now = datetime.now().strftime("%d-%H-%M-%S")
    file_name = f"output-{now}.json"
    file_path = folder_path / file_name
    with file_path.open("w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=4)

    print(f"--- Output salvo em {file_path}")
