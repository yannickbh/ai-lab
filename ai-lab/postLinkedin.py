from dotenv import load_dotenv
load_dotenv()

from crewai_tools import SerperDevTool, ScrapeWebsiteTool
from crewai import Agent, Crew, Task

search_tool = SerperDevTool()
website_tool = ScrapeWebsiteTool()

buscador = Agent(
    role="Buscador",
    goal="Buscar conteudo online sobre o tema {tema}",
    backstory=("Voce esta trabalhando na criacao de artigos para o LinkedIn sobre o {tema}. "
               "Voce deve buscar o conteudo online sobre o tema {tema} e retornar o conteudo encontrado. "
               "seu trabalho ira ajudar o nosso redator a criar um artigo para o LinkedIn sobre o {tema}"),
    tools=[search_tool, website_tool],
    verbose=True
)

redator = Agent(
    role="Redator de Conteudo",
    goal="Escrever um artigo atual sobre as ultimas noticias e tendencias para o LinkedIn sobre o tema {tema}",
    backstory=("Voce esta trabalhando na redacao de um artigo para o LinkedIn sobre o {tema}. "
               "voce devera utilizar o conteudo encontrado pelo buscador para criar um artigo atual sobre as ultimas noticias e tendencias para o LinkedIn sobre o {tema}, "
               "de opinioes de especialistas e de fontes confiaveis, mas sempre destaque as fontes de informacao e as referencias"),
    tools=[search_tool, website_tool],
    verbose=True
)

editor = Agent(
    role="Editor de Conteudo",
    goal="Editar o artigo para o LinkedIn sobre o {tema}",
    backstory=("Voce esta trabalhando na edicao de um artigo para o LinkedIn sobre o {tema}. "
               "voce devera editar o conteudo redigido pelo redator, garantindo gramatica e ortografia corretas, "
               "com um tom de voz de um especialista no assunto"),
    tools=[search_tool, website_tool],
    verbose=True
)

buscar=Task(
    description=("1. busque as ultima tendencias e noticias sobre o {tema} no Google .\n"
                "2. identifique o publico alvo para o artigo, seus interesses e necessidades.\n"
                "3. crie um titulo atraente e relevante para o artigo.\n"
                "4. inclua palavras chave relevantes para o artigo.\n"
                "5. busque informacoes relevantes sobre o {tema} em sites de noticias e de especialistas no assunto.\n"
                "6. compile as informacoes encontradas em um resumo claro e objetivo.\n"
                "7. crie um plano de redacao para o artigo, com os pontos principais que serao abordados.\n"
                "8. crie um esqueleto de artigo, com os titulos e subtitulos que serao abordados."),
    expected_output="Um plano de tendencias sobre o {tema} com os pontos principais que serao abordados, o titulo do artigo, as palavras chave relevantes e as fontes de informacao.",
    agent=buscador 
)

redigir=Task(
    description=("Redacao do artigo para o LinkedIn sobre o {tema}. "
                "Utilize o plano de tendencias e as informacoes encontradas pelo buscador para criar o artigo."),
    expected_output="Um artigo redigido para o LinkedIn sobre o {tema}, o texto devera ser escrito em paragrafos e devera ser claro e objetivo, com fontes de informacao e referencias",
    agent=redator,
    context=[buscar]
)

editar=Task(
    description="Editar o artigo para o LinkedIn sobre o {tema} quanto a gramatica e a ortografia, com tom de voz de um especialista no assunto, garanta que as referencias sejam de 2026",
    expected_output="Um artigo editado pronto para ser publicado no LinkedIn sobre o {tema}, o texto devera ser escrito em paragrafos e devera ser claro e objetivo, com fontes de informacao e referencias",
    agent=editor,
    context=[redigir]
)

equipe = Crew(
    agents=[buscador, redator, editor],
    tasks=[buscar, redigir, editar],
    verbose=True
)

tema_artigo = "IA Generativa 2026"

entrada = {"tema": tema_artigo}

print(equipe.kickoff(inputs=entrada))