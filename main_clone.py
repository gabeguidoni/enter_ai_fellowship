import aiohttp
import time
import asyncio
from utils.constants import TAMANHO_LOTE
from utils.functions import print_duration, save_results, print_results


def build_prompts():
    # fmt: off
    ceps = [
        "01001000", "01311000", "01532001", "02011000", "02233000", "02515000", "03047000", "03309010", "04094001", "04265000", 
        "04543011", "04715000", "04836000", "05010000", "05347000", "05525000", "05858000", "06018000", "06233000", "06454000",
        "06730000", "06813200", "07021000", "07111000", "07232000", "08090000", "08215000", "08557000", "08710150", "09010000",
        "09175100", "09220000", "09340000", "09520000", "09715000", "09910000", "11013000", "11740000", "12010000", "13010000",
        "13201000", "13300100", "13465000", "13560000", "13601000", "13720000", "13800000", "13910000", "14010000", "15015000",
        "16010000", "17010000", "18010000", "19010000", "20040002", "20230000", "20540000", "21010000", "21310000", "22021001",
        "22410030", "22710000", "23040000", "24010000", "25010000", "26010000", "26510000", "28010000", "29010000", "29100000",
        "29210000", "30010000", "30140071", "30220000", "30310000", "30410000", "30510000", "31010000", "31210000", "31310000",
        "31510000", "32600000", "33010000", "35680000", "36010000", "37010000", "38010000", "38400000", "40010000", "40301000",
        "40410000", "40710000", "41010000", "41210000", "41710000", "44010000", "45600000", "49010000", "50010000", "52010000",
        "60010000", "64000000", "69010000", "70040900", "01001000", 
        "01311000"
    ]
    # fmt: on
    return ceps


async def _call(async_client, cep: str) -> tuple[float, float]:

    # await asyncio.sleep(6)  # Essa chamada eh muito rapida
    await asyncio.sleep(0.1)  # Essa chamada eh muito rapida

    url = f"https://cep.awesomeapi.com.br/json/{cep}"

    async with async_client.get(url, timeout=5) as resp:
        coords = await resp.json()

        if "lat" in coords and "lng" in coords:
            return {"cep": cep, "lat": coords["lat"], "lng": coords["lng"]}
        else:
            return {"cep": cep, "lat": "", "lng": ""}


# ===========================
# CODIGO CLONE:
# ===========================


async def _multiple_calls(client, prompts: list[dict]) -> list[object | BaseException]:
    """
    Executa várias chamadas concorrentes e imprime os resultados
    """

    tasks = [_call(client, p) for p in prompts]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print_results(results)
    return results


async def _throttle_responses(
    prompts: list[dict[str, str | object]], tamanho_lote: int
) -> list[object | BaseException]:
    """
    Controla a cadencia das requisicoes
    A primeira faz e ja entrega, a seguir faz em lotes
    """

    # async with AsyncOpenAI(api_key=API_KEY) as async_client:  # ATENCAO
    async with aiohttp.ClientSession() as async_client:  # ATENCAO
        all_results = await _multiple_calls(async_client, [prompts[0]])
        if len(prompts) > 1:
            for i in range(1, len(prompts), tamanho_lote):
                lote_prompts = prompts[i : i + tamanho_lote]
                lote_results = await _multiple_calls(async_client, lote_prompts)
                all_results.extend(lote_results)
    return all_results


async def main():
    inicio = time.time()
    prompts = build_prompts()
    results = await _throttle_responses(prompts, TAMANHO_LOTE)
    print_duration(inicio, time.time(), len(prompts))
    save_results(results)


if __name__ == "__main__":
    asyncio.run(main())


# # 100 req
# 7.9s sincrono
# 0.3s assincrono

# # 100k req
# quebra se for direto
# com semaforo = 10, 208s  ---> muda a ordem
# com lotes = 10, 256s
# com lotes = 100, 36s
