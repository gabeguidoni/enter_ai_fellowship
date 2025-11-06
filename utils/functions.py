import json, fitz
from pydantic import create_model
from datetime import datetime
from pathlib import Path


# TODO: fazer um pre-tratamento no texto removendo letras avulsas
def _get_file_text(file_name: str) -> str:

    path = f"data/files/{file_name}.pdf"
    return fitz.open(path).get_page_text(0)


def _preprocess_dataset_json():

    with open("data/dataset.json", "r", encoding="utf-8") as f:
        items = json.load(f)

    if isinstance(items, dict):
        items = [items]

    batatas = []
    for item in items:
        file_name: str = item["pdf_path"].rsplit(".")[0]

        extraction_keys = list(item["extraction_schema"].keys())
        SchemaClass = create_model(
            f"Schema{file_name.title().replace('_', '')}",
            **{k: (str, "") for k in extraction_keys},
        )
        batatas.append((file_name, SchemaClass))

    return batatas


def build_prompts() -> list[dict[str, str | object]]:
    batatas = _preprocess_dataset_json()
    prompts = []
    for batata in batatas:
        file_text = _get_file_text(batata[0])
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


def print_duration(inicio, fim, quant) -> str:
    print(10 * "=")
    duracao = round(fim - inicio, 2)
    print(f"Esse processamento analisou {quant} documentos e durou {duracao} segundos")
    media = round((fim - inicio) / quant, 5)
    print(f"Uma média de {media} segundos por documento")


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
