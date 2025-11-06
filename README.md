# enter_ai_fellowship
Etapa Take Home Project do processo seletivo para a Enter Ai Fellowship

## Como usar


## Progresso
### Abordagem zero --- assim que vi o desafio
No primeiro momento pensei em criar uma ferramenta que usa-se regex para varrer arquivos com o mesmo label, e caso ainda nao houvesse regex para um dado label, enviaria para o gpt criar, salvaria e continuaria varrendo os arquivos.
#### Problemas: 
1. Após ver os exemplos reparei que "tela_sistema_1" e "tela_sistema_2" tem o mesmo label "tela_sistema", mas sao completamente diferentes,
2. Dois arquivos "oab_n", apesar de terem o mesmo layout, ao ler o pdf, o os dados retornados no texto vieram em diferentes ordens.


### Abordagem 1 --- garantir uma entrega
Irei criar uma ferramenta que extrai todo texto, e envia cada arquivo para o GPT. Assim garanto que terei alguma entrega a tempo. Em seguida melhoro a performance e os custos.

- Obstaculo: Respostas muito lentas do gpt-5-mini, um documento simples (carteira oab) demorava entre 9 e 19 segundos. Solução: descobri que o _reasoning_ estava tomando muitos recursos, agora ajustei para _minimal_ e as respostas veem em menos de 4 segundos.
- Diferencial: Consigo fazer multiplas requisições em paralelo, assim demoro o mesmo tempo para conseguir uma ou 10 respostas (nao passar de 10 para nao congestionar)
- Para economizar recursos financeiros do projeto e tbm nao deixar de fazer todos os testes necessarios para o desenvolvimento, criei um script clone do main.py (main_clone.py) com exatamente as mesmas funcoes, porém chama uma API gratuita.





## Referências:
- https://platform.openai.com/docs/guides/latest-model
- https://platform.openai.com/docs/guides/text
- https://platform.openai.com/docs/guides/structured-outputs
- https://platform.openai.com/docs/guides/prompt-caching
- we recommend using [python-dotenv](https://pypi.org/project/python-dotenv/) to add OPENAI_API_KEY="My API Key" to your .env file
- https://github.com/openai/openai-python?tab=readme-ov-file#async-usage
- https://github.com/openai/openai-python?tab=readme-ov-file#handling-errors
- https://github.com/openai/openai-python?tab=readme-ov-file#timeouts  <!-- Nao deixar alguma requisao bugada prejudicar de mais a media de tempo -->

