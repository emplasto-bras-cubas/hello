
import random
import matplotlib.pyplot as plt 
import matplotlib
matplotlib.use('TkAgg')

def gerar_nota(grupo):
    if grupo == 'professor':
        return random.randint(7,10)
    elif grupo == 'tecnico':
        return random.randint(6,10)
    else:
        return random.randint(1,10)


def gerar_populacao(tamanho):
    populacao = []
    n_professores = int(tamanho * 0.2) #20%
    n_tecnicos = int(tamanho * 0.1) #10% 
    n_alunos = tamanho - n_professores - n_tecnicos #70%
    for i in range(n_professores):
        populacao.append({'grupo':'professor' ,'nota':gerar_nota('professor'), 'turma': None})
    for i in range(n_tecnicos):
        populacao.append({'grupo':'tecnico', 'nota':gerar_nota('tecnico'), 'turma':None})
    for i in range(n_alunos):
        turma = (i % 5) + 1
        populacao.append({'grupo':'aluno', 'nota':gerar_nota('aluno'), 'turma' : turma})
    return populacao

def media_nota(lista):
    soma = 0
    cont = 0
    for pessoa in lista:
        soma += pessoa['nota']
        cont += 1
    if cont == 0:
        return 0
    return soma / cont

def gerar_amostragem_aleatoria_simples(tamanho):
    return random.sample(populacao,tamanho)

def gerar_amostragem_estratificada(tamanho):
    n_prof = int(tamanho * 0.2)
    n_tec = int(tamanho * 0.1)
    n_alu = tamanho - n_prof - n_tec
    pop_professores = []
    pop_alunos = []
    pop_tec = []
    for pessoa in populacao:
        if pessoa['grupo'] == 'professor':
            pop_professores.append(pessoa)
        elif pessoa['grupo']  == 'tecnico':
            pop_tec.append(pessoa)
        else:
            pop_alunos.append(pessoa)
    amostra = []
    amostra += random.sample(pop_professores,n_prof)
    amostra += random.sample(pop_tec,n_tec)
    amostra += random.sample(pop_alunos,n_alu)
    return amostra

def gerar_amostragem_sistematica(tamanho):
    populacao_copia = populacao[:]
    random.shuffle(populacao_copia) #Embaralhar a base de dados
    N = len(populacao_copia) #quantidade de pessoas na população
    k = N // tamanho # k = tamanho da população / tamanho amostra

    amostra = []

    for i in range(0,N,k):
        amostra.append(populacao_copia[i])

    if len(amostra) < tamanho:
        amostra.append(populacao_copia[N-1])

    return amostra

def gerar_amostragem_conglomerados(num_turmas):
    turmas = []
    for pessoa in populacao:
        if pessoa['turma'] is not None and pessoa['turma'] not in turmas:
            turmas.append(pessoa['turma'])
    turmas_selecionadas = random.sample(turmas, num_turmas)
    amostra=[]
    for pessoa in populacao:
        if pessoa['turma'] in turmas_selecionadas:
            amostra.append(pessoa)
    
    return amostra


populacao = gerar_populacao(500)
amostra_simples = gerar_amostragem_aleatoria_simples(100)
amostra_estratificada = gerar_amostragem_estratificada(100)
amostra_sistematica = gerar_amostragem_sistematica(100)
amostra_conglomerados = gerar_amostragem_conglomerados(2)

print(f"Média da população: {media_nota(populacao):.2f}")
print(f"Média da amostra simples: {media_nota(amostra_simples):.2f}")
print(f"Média da amostra estratificada: {media_nota(amostra_estratificada):.2f}")
print(f"Média da amostra sistematica: {media_nota(amostra_sistematica):.2f}")
print(f"Média da amostra conglomerados: {media_nota(amostra_conglomerados):.2f}")

#for pessoa in populacao:
#    print(pessoa)

#pip install matplotlib
media_pop = media_nota(populacao)
media_simples = media_nota(amostra_simples)
media_estratificada = media_nota(amostra_estratificada)
media_sistematica = media_nota(amostra_sistematica)
media_conglomerados = media_nota(amostra_conglomerados)

nomes = ['Aleatória Simples', 'Estratificada', 'Sistemática', 'Conglomerados']
medias = [media_simples,media_estratificada,media_sistematica,media_conglomerados]
cores = ['royalblue', 'mediumseagreen','gold', 'tomato']


#Criar o gráfico
plt.figure(figsize=(8,6))
barras = plt.bar(nomes,medias, color=cores)
plt.axhline(y=media_pop, color='red', linestyle='--', label=f'Média População: {media_pop:.2f}')

for barra in barras:
    plt.text(barra.get_x() + barra.get_width()/2, barra.get_height()-0.40, 
        f'{barra.get_height():.2f}', ha='center', va='bottom', fontsize=10)

plt.ylabel('Nota Média')
plt.title('Comparação da nota média das amostras')
plt.legend()
plt.show()


