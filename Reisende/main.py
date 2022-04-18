import random
from node import Node
import sys
import numpy as np
import matplotlib.pyplot as plt


def random_100():
    list_nodes = []

    for i in range(100):
        x = random.randrange(0, 100)
        y = random.randrange(0, 100)
        node = Node(i, x, y)
        list_nodes.append(node)

    return list_nodes


def euklid(node1, node2):
    p1 = np.array((node1.get_x(), node1.get_y()))
    p2 = np.array((node2.get_x(), node2.get_y()))

    return round(np.linalg.norm(p1 - p2))


def swap(obj1, obj2):
    aux = obj1
    obj1 = obj2
    obj2 = aux
    return obj1, obj2


def random_zahlen():
    zahl1 = random.randint(0, 4)
    zahl2 = random.randint(0, 4)

    return zahl1, zahl2


def vertauschende_mutation(stadte):
    aux_stadte = stadte.copy()

    zahl1, zahl2 = random_zahlen()
    while zahl1 == zahl2:
        zahl1, zahl2 = random_zahlen()

    if zahl1 > zahl2:
        zahl1, zahl2 = swap(zahl1, zahl2)

    for j in range(zahl1, zahl2 + 1):
        aux_stadte[zahl1 + zahl2 - j] = stadte[j]

    return aux_stadte


def kantenKombinationen(stadte, aux_stadte):
    dic_nachbar = {}

    length = 100  # trebuie in 100
    # vecini p1
    for index, val in enumerate(stadte):  # i ia indice base ia val
        dic_nachbar[val] = {stadte[index - 1], stadte[(index + 1) % length]}

    # vecini p2
    for index, val in enumerate(aux_stadte):
        dic_nachbar[val].add(aux_stadte[index - 1])
        dic_nachbar[val].add(aux_stadte[(index + 1) % length])

    choose = random.randint(1, 2)

    if choose == 1:
        nod = stadte[0]
    else:
        nod = aux_stadte[0]

    lista_finala = []
    lista_finala.append(nod)

    while len(lista_finala) < 100:
        lista_vecini = dic_nachbar[nod]
        del dic_nachbar[nod]
        for key in dic_nachbar:
            if nod in dic_nachbar[key]:
                dic_nachbar[key].remove(nod)

        # verificam ce nod sa luam dupa

        if len(lista_vecini) == 0:
            nod_nou = random.choice(list(dic_nachbar))
            lista_finala.append(nod_nou)
            nod = nod_nou

        else:
            minimum = 5
            lista_minime = []
            for i in lista_vecini:
                lungime = len(dic_nachbar[i])

                if lungime < minimum:
                    minimum = lungime

            for i in lista_vecini:
                lungime = len(dic_nachbar[i])
                if lungime == minimum:
                    lista_minime.append(i)

            nod_nou = random.choice(lista_minime)
            lista_finala.append(nod_nou)
            # print(nod_nou)
            nod = nod_nou

    return lista_finala


def plot_anfang_punkte(liste_punkte):

    for punkt in liste_punkte:
        plt.plot(punkt.get_x(), punkt.get_y(), color='black', linestyle='solid', linewidth=2,
                 marker='o', markerfacecolor='blue', markersize=8)
    plt.show()


def fitness_function(list_nodes):
    distance = 0
    lungime_lista = len(list_nodes)
    node_inceput = list_nodes[0]
    nod_sfarsit = list_nodes[lungime_lista - 1]
    node1 = list_nodes[0]

    i = 1
    while i < lungime_lista:
        node2 = list_nodes[i]
        distance = distance + euklid(node1, node2)
        node1 = node2
        i = i + 1

    distance = distance + euklid(node_inceput, nod_sfarsit)
    return distance

def plot_generation(generation, best_route):
    fig, ax = plt.subplots()
    for previous, current in zip(best_route, best_route[1:]):
        ax.plot([previous.get_x(), current.get_x()], [previous.get_y(), current.get_y()], 'g', linestyle="--")
    ax.plot([best_route[-1].get_x(), best_route[0].get_x()], [best_route[-1].get_y(), best_route[0].get_y()],
            'g', linestyle="--")
    ax.set_title(generation)
    plt.show()


def travelling_salesman_problem(parents):
    generation = 0

    best_distance = sys.maxsize
    best_route = []

    best_distance_global = sys.maxsize
    best_route_global = []

    dict_parents = []
    for parent in parents:
        dict_parents.append((parent, fitness_function(parent)))
        if fitness_function(parent) < best_distance:
            best_distance = fitness_function(parent)
            best_route = parent

    best_distances = [best_distance]

    print("----------------" + str(generation) + "--------------------")
    # plot la best pe segment
    plot_generation(generation, best_route)
    print("Best Distance: " + str(best_distance))

    generation += 1

    while generation <= 2000:
        copii = []
        for i in range(40):
            parinte1 = random.choice(list(zip(*dict_parents))[0])
            nr = random.random()
            # print("----------------" + str(generation) + "--------------------")
            if nr < 0.3:
                parinte2 = random.choice(list(zip(*dict_parents))[0])
                parinte1 = kantenKombinationen(parinte1, parinte2)
            copil = vertauschende_mutation(parinte1)
            copii.append(copil)

        dict_copii = []
        for copil in copii:
            dict_copii.append((copil, fitness_function(copil)))
            if fitness_function(copil) < best_distance:
                best_distance = fitness_function(copil)
                best_route = copil

        if generation in (500, 1000, 1500, 2000):
            print("----------------" + str(generation) + "--------------------")
            # plot la best pe segment
            plot_generation(generation, best_route)
            print("Best Distance: " + str(best_distance))

        best_distances.append(best_distance)

        if best_distance < best_distance_global:
            best_distance_global = best_distance
            best_route_global = best_route
        best_distance = sys.maxsize
        best_route = []

        # schimb parintii pt urmatoarea generatie
        dict_parents.extend(dict_copii)
        dict_parents = sorted(dict_parents, key=lambda elem: elem[1])[:10]
        generation = generation + 1

    # plot la global
    generations = [i for i in range(2001)]
    plt.plot(generations, best_distances, color='green', linewidth=3)
    plt.xlabel('Generations')
    plt.ylabel('Distances')
    plt.title('Graph')
    plt.show()

    return best_distance_global, best_route_global


if __name__ == '__main__':
    liste = random_100()

    plot_anfang_punkte(liste)

    perm_list = []

    for r in range(10):
        temp = liste.copy()
        random.shuffle(temp)
        perm_list.append(temp)

    dist, route = travelling_salesman_problem(perm_list)
    print("Best distance global: " + str(dist))

    fig, ax = plt.subplots()
    for previous, current in zip(route, route[1:]):
        ax.plot([previous.get_x(), current.get_x()], [previous.get_y(), current.get_y()], 'g', linestyle="--")
    ax.plot([route[-1].get_x(), route[0].get_x()], [route[-1].get_y(), route[0].get_y()], 'g', linestyle="--")
    ax.set_title("Best")
    plt.show()