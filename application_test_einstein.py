import random
import copy
import matplotlib.pyplot as plt
from collections import defaultdict

# Configurações Gerais
tamanho_populacao = 400
taxa_sobrevivencia = 0.35
taxa_cruzamento = 0.65
taxa_mutacao = 0.05
taxa_migracao = 0.05

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
        if (casa["nacionalidade"] == "noruegues" and i == 0):
            pontuacao += 4

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
        if (i + 1 < len(solucao) and solucao[i]["cor"] == "verde"
                and solucao[i + 1]["cor"] == "branca"):
            pontuacao += 4

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
            pontuacao += 4

        # O homem que fuma Blends vive ao lado do que tem Gatos
        if (casa["cigarro"] == "blends"):
            if ((i - 1 >= 0 and solucao[i - 1]["animal"] == "gatos")
                    or (i + 1 < len(solucao) and solucao[i + 1]["animal"] == "gatos")):
                pontuacao += 4

        # O homem que cria Cavalos vive ao lado do que fuma Dunhill
        if (casa["animal"] == "cavalos"):
            if ((i - 1 >= 0 and solucao[i - 1]["cigarro"] == "dunhill") or
                    (i + 1 < len(solucao) and solucao[i + 1]["cigarro"] == "dunhill")):
                pontuacao += 4

        # O homem que fuma BlueMaster bebe Cerveja
        if (casa["cigarro"] == "blue master" and casa["bebida"] == "cerveja"):
            pontuacao += 1

        # O Alemão fuma Prince
        if (casa["nacionalidade"] == "alemao" and casa["cigarro"] == "prince"):
            pontuacao += 1

        # O Norueguês vive ao lado da casa Azul
        if (casa["nacionalidade"] == "noruegues"):
            if ((i - 1 >= 0 and solucao[i - 1]["cor"] == "azul")
                    or (i + 1 < len(solucao) and solucao[i + 1]["cor"] == "azul")):
                pontuacao += 4

        # O homem que fuma Blends é vizinho do que bebe Água
        if (casa["cigarro"] == "blends"):
            if ((i - 1 >= 0 and solucao[i - 1]["bebida"] == "agua")
                    or (i + 1 < len(solucao) and solucao[i + 1]["bebida"] == "agua")):
                pontuacao += 4
    return pontuacao


# Realiza o cruzamento de duas soluções gerando dois filhos
def crossover(solucao1, solucao2):
    filho1 = []
    filho2 = []

    for i in range(5):
        filho1.append({"cor": solucao1[i]["cor"],
                       "nacionalidade": solucao1[i]["nacionalidade"],
                       "bebida": solucao2[i]["bebida"],
                       "cigarro": solucao2[i]["cigarro"],
                       "animal": solucao2[i]["animal"],
                       })
        filho2.append({"cor": solucao2[i]["cor"],
                       "nacionalidade": solucao2[i]["nacionalidade"],
                       "bebida": solucao1[i]["bebida"],
                       "cigarro": solucao1[i]["cigarro"],
                       "animal": solucao1[i]["animal"],
                       })

    return filho1, filho2


# Realiza mutação em uma solução
def mutation(solucao):
    pos_casa1 = random.randint(0,4)
    pos_casa2 = random.randint(0,4)
    while (pos_casa1 == pos_casa2):
        pos_casa2 = random.randint(0, 4)

    pos_atributo = random.randint(0,4)

    atributos = ["cor","nacionalidade","bebida","cigarro","animal"]
    mutante = solucao

    aux_atributo = ""
    aux_atributo = mutante[pos_casa1][atributos[pos_atributo]]
    mutante[pos_casa1][atributos[pos_atributo]] = mutante[pos_casa2][atributos[pos_atributo]]
    mutante[pos_casa2][atributos[pos_atributo]] = aux_atributo
    return mutante


def insere_imigrante():
    return create()


def roleta(tabela):
    tipos_de_pontos = []
    for i in tabela:
        tipos_de_pontos.append(i)

    result1 = random.choices(tipos_de_pontos, weights=tipos_de_pontos, k=1)[0]
    result2 = random.choices(tipos_de_pontos, weights=tipos_de_pontos, k=1)[0]
    return  random.choice(tabela[result1]), random.choice(tabela[result2])


def imprime_solucao(resposta):
    i = 1
    for casa in resposta:
        print(f"==Casa {i}==")
        i += 1
        for chave, valor in casa.items():
            print(f"{chave}: {valor}")
        print()  # Adiciona uma linha em branco entre os dicionários para melhor legibilidade

populacao = []
geracao = []
quantidade_geracoes = 0
maior_pontuacao = 0
resposta = []

x_media = []
y_media = []
x_maior = []
y_maior = []

# Criando população inicial
for i in range(tamanho_populacao):
    populacao.append(create())

while (maior_pontuacao != 36):
    # log da geração atual
    log = "Geração {n_geracao}... maior pontuação: {pontuacao}..."
    print(log.format(n_geracao=quantidade_geracoes, solucao=resposta, pontuacao=maior_pontuacao))

    # Avaliando cada solução com a função fitness

        #ranking se dá dessa forma: ranking[id_da_solucao] = pontuacao
    ranking = {}
        #tabela de pontos se dá dessa forma: tabela_de_pontos [pontuacao] = solucao
    tabela_por_pontos = defaultdict(list)
    media_pontos = 0
    for i in range(tamanho_populacao):
        solucao = populacao[i]
        pontuacao = fitness(solucao)
        tabela_por_pontos[pontuacao].append(solucao)
        ranking[i] = pontuacao
        media_pontos += pontuacao
    media_pontos = media_pontos / tamanho_populacao

    # Ordenando a tabela ranking para que os primeiros sejam os mais aptos
    ranking = dict(
        sorted(ranking.items(), key=lambda item: item[1], reverse=True))

    #contem todas as pontuações em ordem decrescente
    classificacao = list(ranking.values())

    maior_pontuacao = classificacao[0]
    resposta = tabela_por_pontos[maior_pontuacao]

    # chaves_ranking recebe a lista de todas as chaves ordenadas decrescentemente, de acordo com a pontuação.
    # a chave funciona como id de uma solucao
    chaves_ranking = list(ranking.keys())

    # Sobrevivendo as melhores soluções
    for i in range(round(taxa_sobrevivencia * tamanho_populacao)):
        geracao.append(populacao[chaves_ranking[i]])

    # Cruzamento utilizando roleta
    for i in range(round(taxa_sobrevivencia * tamanho_populacao),
                   tamanho_populacao,2):
        if (i + 1 < tamanho_populacao):
            pai1, pai2 = roleta(tabela_por_pontos)
            filho1, filho2 = crossover(pai1, pai2)
            geracao.append(filho1)
            geracao.append(filho2)

    # Realizando mutação
    for i in range(round(taxa_mutacao * tamanho_populacao), tamanho_populacao):
        if random.random() <= taxa_mutacao:
            geracao[i] = mutation(geracao[i])

    #Adicionando imigrante
    for i in range(round(taxa_migracao * tamanho_populacao),
                   tamanho_populacao):
        if random.random() <= taxa_migracao:
            geracao[i] = insere_imigrante()

    populacao = geracao
    geracao = []
    ranking = {}
    quantidade_geracoes += 1
    tabela_por_pontos.clear()
    x_media.append(quantidade_geracoes)
    y_media.append(media_pontos)
    x_maior.append(quantidade_geracoes)
    y_maior.append(maior_pontuacao)

log = "Geração {n_geracao}... Solução: "
print(log.format(n_geracao=quantidade_geracoes))
imprime_solucao(resposta[0])

plt.plot(x_media, y_media, color='blue')
plt.plot(x_maior, y_maior, color='green')
plt.show()

