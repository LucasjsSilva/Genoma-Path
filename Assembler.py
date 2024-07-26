import numpy as np

def abrir_arquivo(nome):
    composicao = []
    with open(nome, 'r') as arquivo:
        for linha in arquivo:
            composicao.extend([composicao.strip() for composicao in linha.strip().split(',')])
    return composicao

def prefixo_sufixo(composicao, k):
    dicionario = {} #Dicionario que guarda os sufixos e prefixos de acordo com o kmer.
    for c in composicao:
        if c not in dicionario:
            dicionario[c] = [c[0:k-1], c[1:k], 1]
        else:
            dicionario[c][2] += 1
    return dicionario

def balanceia_grafo(matriz):
    vertice_inicio, vertice_final = None, None
    for i in range(len(matriz)):
        grau_saida = 0
        grau_entrada = 0
        for j in range(len(matriz)):
            grau_saida += matriz[:, i][j]
        for l in range(len(matriz)):
            grau_entrada += matriz[i, :][l]
        if grau_saida != grau_entrada:
            if grau_saida > grau_entrada:
                vertice_inicio = i
            else:
                vertice_final = i
    if vertice_inicio is not None and vertice_final is not None:
        matriz[vertice_inicio][vertice_final] += 1

    return matriz, vertice_inicio
def ciclo_euleriano(matriz):
    matriz, vertice_inicio = balanceia_grafo(matriz)
    ciclo = []
    pilha = [vertice_inicio]
    while pilha:
        u = pilha[-1]
        for i in range(len(matriz)):
            if matriz[u][i] > 0:
                pilha.append(i)
                matriz[u][i] -= 1
                break
        else:
            ciclo.append(pilha.pop())
    return ciclo[::-1]

def assembler(kmers, k):
    dicionario = prefixo_sufixo(kmers, k)
    vertices = []
    for chave, valor in dicionario.items():
        vertice_origem, vertice_destino, quantidade = valor
        if vertice_origem not in vertices:
            vertices.append(vertice_origem)
        if vertice_destino not in vertices:
            vertices.append(vertice_destino)

    quant_vertices = len(vertices)
    matriz = np.zeros((quant_vertices, quant_vertices), dtype=int)

    for chave, valor in dicionario.items():
        vertice_origem, vertice_destino, quantidade = valor
        i = vertices.index(vertice_origem)
        j = vertices.index(vertice_destino)
        matriz[i][j] = quantidade

    ciclo = ciclo_euleriano(matriz)
    ciclo = [vertices[i] for i in ciclo]

    sequencia = ciclo[1]
    for i in range(2, len(ciclo)):
        sequencia += ciclo[i][-1]

    return sequencia

def salvar_arquivo(sequencia):
    with open('output.txt', 'w') as file:
        file.write(sequencia)

composicao = abrir_arquivo('composition120.txt')

sequencia = assembler(composicao, 15)

salvar_arquivo(sequencia)

