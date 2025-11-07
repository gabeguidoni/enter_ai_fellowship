# Enter AI Fellowship — Take Home Project  

Etapa do processo seletivo para a **Enter AI Fellowship**.  
Este repositório contém a ferramenta desenvolvida para o desafio técnico.


## Como instalar
1. Clone esse repositório no seu computador
2. Crie um venv e instale nele o requirements.txt
3. Pelo terminal, navegue até onde você clonou o repositório
4. Em seguida execute `streamlit run app.py`, isso irá abrir a ferramenta no seu navegador
4. Pronto!


## Progresso
### Abordagem zero - Ideia inicial
No primeiro momento pensei em criar uma ferramenta que usa-se **regex** para varrer arquivos com o mesmo label e key, caso ainda nao houvesse regex para um dado label e key, enviaria para o gpt criar, **armazenaria para uso futuro**, e voltaria a varrer os arquivos.
#### Desafios: 
1. Após ver os exemplos reparei que "tela_sistema_1" e "tela_sistema_2" tem o mesmo label "tela_sistema", mas sao completamente diferentes,
2. Dois arquivos "oab_n", apesar de terem o mesmo layout, ao ler o pdf, o os dados retornados no texto vieram em diferentes ordens.
3. ~~Tenho três provas essa semana, mas quero muito passar nesse processo seletivo~~
 

### Abordagem 1 - Garantir uma entrega
Irei criar uma ferramenta que extrai todo texto, e envia cada arquivo para o Gepeto. Assim garanto que terei alguma entrega dentro do prazo. Em seguida melhoro os custos e a performance.
- Obstáculo: Respostas muito lentas da API, um documento simples (carteira oab) demorava entre 9 e 19 segundos. Solução: descobri que o **reasoning** estava gastando muitos recursos, ajustei para _minimal_ e as respostas veem em menos de 4 segundos.
- Diferencial: Consigo fazer multiplas requisições assincronas, assim demoro o mesmo tempo para trazer 1 ou 10 respostas (não passar de 10 para não congestionar). O avaliador comentou sobre isso ser um grande diferencial!
- Para economizar recursos financeiros durante o desenvolvimento e também não deixar de fazer todos os testes necessários, criei um script clone do main.py (main_clone.py) com exatamente as mesmas funções, porém chamando uma API gratuita.
- Como UI irei criar uma pagina **Streamlit**, a ideia é que o usuário rode localmente mesmo.
- Obstaculo: a pagina streamlit deixa o sistema um pouco mais lento, e dificultou a atender a regra _"primeiro retorno em <10s"_


## Como ficou
- Foi criado um app de duas páginas para a entrega, sendo a primeira apresentação e documentação, e a segunda a ferramenta em sí.
- Na primeira página temos esse readme que inclui instruções de como começar a usar o app, ideias que foram aparecendo durante o desenvolvimento e documentações que foram consultadas durante o desenvolvimento.
- Na segunda página temos um app bem **user-friendly** e _resistente a mal uso_.
- Esse é o **passo a passo para o usuário final**:
    1. Cole no primeiro campo sua **API Key**. O sistema validará a autenticidade antes de continuar.
    2. No segundo campo, faça o upload de um **extraction_schema**, só é permitido envio de um arquivo json por vez.
    3. No ultimo campo, deposite **um ou mais documentos** em PDF.
    4. Serão feitas as seguintes validações antes que o botao **Executar Extração** seja disponibilizado:
        1. API Key preenchida e validada
        2. extraction_schema referencia o mesmo numero de PDFs que foram enviados
        3. Todos os nomes dos documentos carregados estão listados no extraction_schema enviado
    5. Quando uma validação não é aprovada, o sistema imprime alertas didáticos auxiliando o usuário a adequar seus inputs.
    6. Caso o usuário tenha dificuldades com o formato dos arquivos esperados, é oferecido download de exemplos para servir como referência.
    7. Após todos os envios e validações aprovadas, o botao _Executar Extração_ é desbloqueado e o usuário pode acionar a ferramenta.
    8. O primeiro resultado é impresso assim que fica pronto (o que tem demorado menos de 3s), os demais são impressos em lotes de 10, até um limite de 20 impressoes, para evitar lentidao no sistema.
    9. O resultado completo é salvo e pode ser baixado pelo usuário por um botão que aparece assim que o processo termina.
- No final das paginas do app temos um footer com algumas informações sobre o candidado.


## Estrutura do projeto
```
├── data/
│   ├── files/
│   ├── images/
│   ├── outputs/  # deposito de outputs
│   └── um_so.json  # arquivo enviado como exemplo
├── utils/
│   ├── __init__.py
│   ├── constants.py
│   ├── functions.py  # funcoes usadas pelo main.py
│   └── st_functions.py  # funcoes usadas pelo app.py
├── .gitignore
├── README.md
├── requirements.txt
├── main_clone.py  # adaptacao para economizar recursos durante desenvolvimento
├── main.py  # codigo principal da ferramenta
└── app.py  # script para criacao da UI
```


## Referências:
- https://www.blog.getenter.ai/en/posts/software-engineer-agents-are-coming-and-its-not-optional
- https://platform.openai.com/docs/guides/latest-model
- https://platform.openai.com/docs/guides/text
- https://platform.openai.com/docs/guides/structured-outputs
- https://platform.openai.com/docs/guides/prompt-caching
- OpenAI recommend using [python-dotenv ](https://pypi.org/project/python-dotenv/) to add API_KEY to your .env file
- https://github.com/openai/openai-python?tab=readme-ov-file#async-usage
- https://github.com/openai/openai-python?tab=readme-ov-file#handling-errors
- https://docs.streamlit.io/develop/api-reference/

