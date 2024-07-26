def Composition(Sequencia, k):
    comp = []
    for i in range(len(Sequencia)-k+1):
        mer = ''
        for j in range(k):
            mer += Sequencia[i+j]
        comp.append(mer)

    return sorted(comp)

sequencia = input("Digite uma sequencia: ")
k = int(input("Digite um valor K: "))

kmers = Composition(sequencia, 15)

with open('composition.txt', 'w') as file:
    for k in kmers:
        file.write(k + ',')
