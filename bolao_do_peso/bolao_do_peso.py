numero_participantes = int(input("Digite o número de participantes: "))
n=1
lista = []
while n <= numero_participantes:
    nome_participante = input("Digite o nome do participante: ")
    peso_inicial = float(input(f'digite o peso inicial do(a) {nome_participante}: '))
    peso_final = float(input(f'digite o peso final do(a) {nome_participante}: '))
    perda_peso = peso_inicial - peso_final
    percentual_perda_de_peso = f'{(perda_peso / peso_inicial)*100}%'
    lista.append({nome_participante:perda_peso,n-1:percentual_perda_de_peso})
    n += 1

maior = 0.0001
indice = 0
for e,l in enumerate(lista):

    if (float(l[e].replace("%",""))*1 > maior):
        maior = float(l[e].replace("%","")*1)
        indice = e

    else:
        pass


print(lista[indice])