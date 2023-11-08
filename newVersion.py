import random
import copy

# Configurações Gerais
from collections import defaultdict

tamanho_populacao = 100
quantidade_geracoes = 100
taxa_sobrevivencia = 0.40
taxa_cruzamento = 0.60
taxa_mutacao = 0.1

parametros = {
    "cor": ["amarela", "azul", "branca", "verde", "vermelha"],
    "nacionalidade": ["alemao", "dinamarques", "noruegues", "ingles", "sueco"],
    "bebida": ["agua", "cha", "cafe", "leite", "cerveja"],
    "cigarro": ["dunhill", "blends", "pall mall", "prince", "blue master"],
    "animal": ["gatos", "passaros", "cavalos", "peixes", "cachorros"]
}


# Cria uma solução válida escolhendo aleatoriamente
# uma cor, nacionalidade, bebida, cigarro e animal.
def create():
    parametros_copy = copy.deepcopy(parametros)
    solucao = []

    for i in range(5):
        casa = {}
        for parametro in parametros_copy:
            atributo = random.choice(parametros_copy[parametro])
            parametros_copy[parametro].remove(atributo)
            casa[parametro] = atributo
        solucao.append(casa)
    return solucao


# Avalia a solução com base nos critérios estabelecidos.
def fitness(solucao):
    pontuacao = 0
    for i in range(len(solucao)):
        casa = solucao[i]

        # O Norueguês vive na primeira casa
        if (casa["nacionalidade"] == "norueguês" and i == 0):
            pontuacao += 1

        # O Inglês vive na casa Vermelha.
        if (casa["cor"] == "vermelha" and casa["nacionalidade"] == "ingles"):
            pontuacao += 1

        # O Sueco tem Cachorros como animais de estimação.
        if (casa["nacionalidade"] == "sueco" and casa["animal"] == "cachorros"):
            pontuacao += 1

        # O Dinamarquês bebe Chá.
        if (casa["nacionalidade"] == "dinamarques" and casa["bebida"] == "cha"):
            pontuacao += 1

        # A casa Verde fica do lado esquerdo da casa Branca.
        if (i + 1 < len(solucao) and solucao[i]["cor"] == "verde" and solucao[i + 1]["cor"] == "branca"):
            pontuacao += 1

        # O homem que vive na casa Verde bebe Café.
        if (casa["cor"] == "verde" and casa["bebida"] == "cafe"):
            pontuacao += 1

        # O homem que fuma cigarro cria pássaros
        if (casa["cigarro"] == "pall mall" and casa["animal"] == "passaros"):
            pontuacao += 1

        # O homem que mora na casa amarela fuma dunhill
        if (casa["cor"] == "amarela" and casa["cigarro"] == "dunhill"):
            pontuacao += 1

        # O homem que vive na casa do meio bebe Leite
        if (i == 2 and casa["bebida"] == "leite"):
            pontuacao += 1

        # O homem que fuma Blends vive ao lado do que tem Gatos
        if (casa["cigarro"] == "blends"):
            if ((i - 1 >= 0 and solucao[i - 1]["animal"] == "gatos") or (
                    i + 1 < len(solucao) and solucao[i + 1]["animal"] == "gatos")):
                pontuacao += 1

        # O homem que cria Cavalos vive ao lado do que fuma Dunhill
        if (casa["animal"] == "cavalos"):
            if ((i - 1 >= 0 and solucao[i - 1]["cigarro"] == "dunhill") or (
                    i + 1 < len(solucao) and solucao[i + 1]["cigarro"] == "dunhill")):
                pontuacao += 1

        # O homem que fuma BlueMaster bebe Cerveja
        if (casa["cigarro"] == "blue master" and casa["bebida"] == "cerveja"):
            pontuacao += 1

        # O Alemão fuma Prince
        if (casa["nacionalidade"] == "alemao" and casa["cigarro"] == "prince"):
            pontuacao += 1

        # O Norueguês vive ao lado da casa Azul
        if (casa["nacionalidade"] == "noruegues"):
            if ((i - 1 >= 0 and solucao[i - 1]["cor"] == "azul") or (
                    i + 1 < len(solucao) and solucao[i + 1]["cor"] == "azul")):
                pontuacao += 1

        # O homem que fuma Blends é vizinho do que bebe Água
        if (casa["cigarro"] == "blends"):
            if ((i - 1 >= 0 and solucao[i - 1]["bebida"] == "agua") or (
                    i + 1 < len(solucao) and solucao[i + 1]["bebida"] == "agua")):
                pontuacao += 1

    return pontuacao


# Realiza o cruzamento de duas soluções gerando dois filhos
def crossover(solucao1, solucao2):
    filho1 = []
    filho2 = []

    for i in range(5):
        if (i < 2):
            filho1.append(solucao1[i])
            filho2.append(solucao2[i])
        else:
            filho1.append(solucao2[i])
            filho2.append(solucao1[i])

    return filho1, filho2


# Realiza mutação em uma solução
def mutation(solucao):
    return create()

def roleta(tabela):
    """Faz uma divisão diretamente proporcional para obter as porcentagens/probabilidades, de forma que
    a tabela_probabilidades se dá assim: tabela_probabilidades[pontos] = probabilidade
    Por fim, aplica-se uma estratégia para obter o cromossomo associado a determinada pontuação,
    seguindo a probabilidade"""

    tipos_de_pontos = []
    for i in tabela:
        tipos_de_pontos.append(i)

    #aplicando a divisão diretamente proporcional
    somatorio_pontos = sum(tipos_de_pontos)
    fator_proporcionalidade = 100//somatorio_pontos

    tabela_probabilidades = {}

    #usa-se essa variavel para garantir que não dê errado caso fator_proporcionalidade seja diferente de 100
    teto_somatorio_porcentagem = 0

    for i in range(len(tipos_de_pontos)):
        #obtendo: tabela_probabilidades[pontos] = probabilidade
        tabela_probabilidades[tipos_de_pontos[i]] = fator_proporcionalidade*tipos_de_pontos[i]
        teto_somatorio_porcentagem += tabela_probabilidades[tipos_de_pontos[i]]

    valor_escolhido = random.randint(1, teto_somatorio_porcentagem)
    resultado = 0
    acumulado = 0
    for tipo, probabilidade in tabela_probabilidades.items():
        acumulado += probabilidade
        if valor_escolhido <= acumulado:
            resultado = tipo
            break
    return random.choice(tabela[resultado]), random.choice(tabela[resultado])


populacao = []
geracao = []
maior_pontuacao = 0
resposta = []
# Criando população inicial
for i in range(tamanho_populacao):
    populacao.append(create())

for repeticao in range(quantidade_geracoes):
    # Avaliando cada solução com a função fitness
    ranking = {}
    tabela_por_pontos = defaultdict(list)
    for i in range(tamanho_populacao):
        solucao = populacao[i]
        pontuacao = fitness(solucao)
        tabela_por_pontos[pontuacao].append(solucao)
        ranking[i] = pontuacao


    # Ordenando a geração atual para que os primeiros sejam os mais aptos
    ranking = dict(sorted(ranking.items(), key=lambda item: item[1], reverse=True))
    classificacao = list(ranking.values())
    maior_pontuacao = classificacao[0]
    resposta = tabela_por_pontos[maior_pontuacao]
    for posicao in classificacao:
        geracao.append(populacao[posicao])

    # Sobrevivendo as melhores soluções
    for i in range(round(taxa_sobrevivencia * tamanho_populacao)):
        populacao[i] = geracao[i]

    # Cruzando o resto das soluções
    for i in range(round(taxa_sobrevivencia * tamanho_populacao), tamanho_populacao, 2):
        if (i + 1 < tamanho_populacao):
            pai1, pai2 = roleta(tabela_por_pontos)
            filho1, filho2 = crossover(pai1, pai2)
            populacao[i] = filho1
            populacao[i + 1] = filho2

    # Realizando mutação
    for i in range(round(taxa_sobrevivencia * tamanho_populacao), tamanho_populacao):
        if random.random() < taxa_mutacao:
            populacao[i] = mutation(populacao[i])

    geracao = []
    ranking = {}

print(f"{resposta}\n{maior_pontuacao}")

# solução: [{"cor": "amarela","nacionalidade": "noroegues","bebida": "água", "cigarro": "blends", "animal": "cachorros"}, ....]
