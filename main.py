from utils.constants import MODEL, TAMANHO_LOTE
from utils.functions import build_prompts, print_results, print_duration, save_results
from openai import AsyncOpenAI
from dotenv import load_dotenv
import os, time, asyncio

load_dotenv()
API_KEY = os.getenv("API_KEY")


async def _call(async_client: AsyncOpenAI, p: dict):
    """Chama o modelo de forma assincrona"""
    response = await async_client.responses.parse(
        model=MODEL,
        reasoning={"effort": "minimal"},
        input=p["texto_doc"],
        text_format=p["schema"],
    )

    return response.output_parsed.model_dump()


# ===========================


async def _multiple_calls(client, prompts: list[dict]) -> list[object | BaseException]:
    """
    Executa várias chamadas concorrentes e imprime os resultados
    """

    tasks = [_call(client, p) for p in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    # print_results(results)
    return results


async def _throttle_responses(
    api_key: str, prompts: list[dict[str, str | object]], tamanho_lote: int
) -> list[object | BaseException]:
    """
    Controla a cadencia das requisicoes
    A primeira faz e ja entrega, a seguir faz em lotes
    """

    async with AsyncOpenAI(api_key=api_key) as async_client:  # ATENCAO
        # async with aiohttp.ClientSession() as async_client:  # ATENCAO
        all_results = await _multiple_calls(async_client, [prompts[0]])
        if len(prompts) > 1:
            for i in range(1, len(prompts), tamanho_lote):
                lote_prompts = prompts[i : i + tamanho_lote]
                lote_results = await _multiple_calls(async_client, lote_prompts)
                all_results.extend(lote_results)
    return all_results


async def main(api_key: str, json_schemas: list[dict], pdf_files: list[object]):
    inicio = time.time()
    prompts = build_prompts(json_schemas, pdf_files)
    results = await _throttle_responses(api_key, prompts, TAMANHO_LOTE)
    d, m = print_duration(inicio, time.time(), len(prompts))
    save_results(results)
    return results, d, m


# if __name__ == "__main__":
#     asyncio.run(main())
