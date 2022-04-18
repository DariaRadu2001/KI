import random
from Node import Node
import matplotlib.pyplot as plt


# creez n noduri random care reprezinta orasele
def random_n_nodes(n):
    list_nodes = []

    for i in range(n):
        x = random.randrange(0, 50)
        y = random.randrange(0, 50)
        node = Node(i, x, y)
        list_nodes.append(node)

    return list_nodes


# fac o matrice pt distante dintre toate nodurile, pe diagonala principala avem valoarea 0
def generate_distance_matrix(list_nodes):

    distance_matrix = []
    for i in list_nodes:
        row = []
        for j in list_nodes:

            if i == j:
                row.append(0)
            else:
                #caz in care pct se suprapun pt a nu ajunge sa divid la 0
                if i.euklid(j) == 0:
                    row.append(0.000001)
                else:
                    row.append(i.euklid(j))

        distance_matrix.append(row)

    return distance_matrix


# fac o matrice pt feromoni dintre toate nodurile, pe diagonala principala avem valoarea 0 in rest 1
def generate_pheromon_matrix(n):
    pheromon_matrix = []

    for i in range(0, n):
        row = []
        for j in range(0, n):

            if i == j:
                row.append(0)
            else:
                row.append(1)

            pheromon_matrix.append(row)

    return pheromon_matrix


# ii in curs formula asta numa ca nu am pus /s ii in slide 49 un exemplu
def calculate_whk(pheromon_matix, distance_matrix, node1, node2, beta):

    whk = pheromon_matix[node1.get_name()][node2.get_name()]\
          * ((1/distance_matrix[node1.get_name()][node2.get_name()])**beta)
    return whk


# aici calculez ce nod va vizita o furnica dupa formula
def choose_next_node_smart(actual_node, beta, besucht, list_nodes, pheromon_matix, distance_matrix):
    wahrscheinlichkeiten = []
    biggest_whk = 0
    lista_candidati = []
    the_choosen_one = actual_node
    s = 0

    for i in list_nodes:
        if i.get_name() != actual_node.get_name():
            if i not in besucht:
                lista_candidati.append(i)
                wahrscheinlichkeiten.append(calculate_whk(pheromon_matix, distance_matrix, actual_node, i, beta))

    for j in wahrscheinlichkeiten:
        s = s+j

    for z in range(0, len(wahrscheinlichkeiten)):
        if wahrscheinlichkeiten[z]/s > biggest_whk:
            biggest_whk = wahrscheinlichkeiten[z]/s
            the_choosen_one = lista_candidati[z]

    return the_choosen_one


# unele furnici nu se duc dupa feromoni asa ca aleg random un node nevizitat
def choose_next_node_random(actual_node, besucht, list_nodes):
    lista_candidati = []

    for i in list_nodes:
        if i.get_name() != actual_node.get_name():
            if i not in besucht:
                lista_candidati.append(i)

    the_choosen_one = random.choice(lista_candidati)
    return the_choosen_one


def plot_anfang_punkte(liste_punkte):

    for punkt in liste_punkte:
        plt.plot(punkt.get_x(), punkt.get_y(), color='black', linestyle='solid', linewidth=1,
                 marker='o', markerfacecolor='pink', markersize=8)
    plt.show()


def ameisen(n, nr_furnici, iteratii, beta):
    iteratii_totale = iteratii
    list_nodes = random_n_nodes(n)
    plot_anfang_punkte(list_nodes)
    pheromon_matrix = generate_pheromon_matrix(n)
    distance_matrix = generate_distance_matrix(list_nodes)
    best_way_after_each_iteration = []

    # intr-o iteratie fac toate furniciile si gasesc cel mai bun drum
    while iteratii > 0:

        best_cost = 10000
        best_way = []
        # iau fiecare furnica care porneste dintr-un nod random
        for i in range(0, nr_furnici):

            besucht = []
            nod_actual = random.choice(list_nodes)
            besucht.append(nod_actual)

            # drumul furnicii n
            while len(besucht) != n:
                prev = nod_actual
                c = random.random()
                if c > 0.3:
                    nod_actual = choose_next_node_smart(nod_actual, beta, besucht, list_nodes,
                                                        pheromon_matrix, distance_matrix)
                else:
                    nod_actual = choose_next_node_random(nod_actual, besucht, list_nodes)

                # sunt lasati feromoni pe linia[prev, nod_actual]
                ii = prev.get_name()
                jj = nod_actual.get_name()

                pheromon_matrix[ii][jj] += 1
                pheromon_matrix[jj][ii] += 1

                besucht.append(nod_actual)

            # costul rutei pt furnica n dupa distance_matrix
            cost = 0
            for iii in range(0, len(besucht) - 1):
                cost += distance_matrix[besucht[iii].get_name()][besucht[iii + 1].get_name()]

            # print("Cost = " + str(cost) + " drum")
            # for nod in besucht:
            #     print(str(nod))

            # verificam daca ii furnica cu cel mai bun drum
            if cost < best_cost:
                best_cost = cost
                best_way = besucht

            # nr de feromoni scade in timp dupa fiecare furnica
            for z in range(0, n):
                for j in range(0, n):
                    pheromon_matrix[z][j] -= 0.005
                    if pheromon_matrix[z][j] < 0:
                        pheromon_matrix[z][j] = 0

        print("Cel mai bun Cost dupa iteratia " + str(iteratii_totale - iteratii + 1)
              + " = " + str(best_cost) + " drum")
        for nod in best_way:
            print(str(nod))

        # dupa ce s-au terminat furniciile
        iteratii -= 1
        # adaug intr-un dictionar drumul cel mai bun dintr-o iteratie si costul ei
        best_way_after_each_iteration.append((best_way, best_cost))

    # dam cel mai bun drum din toate iteratiile
    the_best_cost_of_all_iterations = 10000
    the_best_way_of_all_iterations = []
    for key in best_way_after_each_iteration:
        if key[1] < the_best_cost_of_all_iterations:
            the_best_cost_of_all_iterations = key[1]
            the_best_way_of_all_iterations = key[0]

    return the_best_way_of_all_iterations, the_best_cost_of_all_iterations


def plot_best(best_route):
    fig, ax = plt.subplots()
    for previous, current in zip(best_route, best_route[1:]):
        ax.plot([previous.get_x(), current.get_x()], [previous.get_y(), current.get_y()], 'g', linestyle="--")
    ax.plot([best_route[-1].get_x(), best_route[0].get_x()], [best_route[-1].get_y(), best_route[0].get_y()],
            'g', linestyle="--")
    plt.show()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    beta = 2
    n = 30
    nr_furnici = 30 #50
    iteratii = 50 #5000

    the_best_way_of_all_iterations, the_best_cost_of_all_iterations = ameisen(n, nr_furnici, iteratii, beta)
    print("CEL MAI BUN COST = " + str(the_best_cost_of_all_iterations) + " drum")
    plot_best(the_best_way_of_all_iterations)
