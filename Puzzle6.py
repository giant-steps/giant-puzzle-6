import numpy as np

# n é o número de dimensões e L2 é a norma utilizada
for (n, norm_type) in [(3, "L2"), (7, "L2")]:
    total_vertices = int(2**n)
    A = np.zeros(shape = (total_vertices, total_vertices)) # Matriz com os coeficientes do sistema linear
    v = np.zeros(shape = (total_vertices, 1)) # Vetor de 1 referente a cada passo dado
    P = np.zeros(shape = (total_vertices, total_vertices)) # Matriz de probabilidades

    final_coordinate = []
    for i in range(n-1):
        final_coordinate.append(1)
    final_coordinate.append(0)
    final_coordinate = tuple(final_coordinate)

    list_coordinates = []
    dict_coordinates = {}
    for i in range(total_vertices):
        coordinate = []
        curr_number = i
        for j in range(n):
            coordinate.append(curr_number % 2)
            curr_number = int(curr_number / 2)
        list_coordinates.append(tuple(coordinate))
        dict_coordinates[tuple(coordinate)] = i

    final_pos = dict_coordinates[final_coordinate]

    # O loop abaixo atualiza as probabilidades de a formiga partir de um vértice e chegar a qualquer outro
    for i in range(total_vertices):
        old_coordinate = list(list_coordinates[i])
        curr_sum = 0.0
        for j in range(total_vertices):
            if j != i:
                new_coordinate = list(list_coordinates[j])
                dist = 0.0
                if norm_type == "L2":
                    for k in range(n):
                        dist += (new_coordinate[k] - old_coordinate[k]) ** 2
                    dist = np.sqrt(dist)
                elif norm_type == "L1":
                    for k in range(n):
                        dist += abs(new_coordinate[k] - old_coordinate[k])
                P[i, j] = 1.0 / dist
                curr_sum += 1.0 / dist

        # Normalização das probabilidades para que somem um dado o vértice de origem
        for j in range(total_vertices):
            P[i, j] = P[i, j] / curr_sum

    # Atualização dos coeficientes do sistema linear
    for i in range(total_vertices - 1):
        A[i, i] = 1.0
        v[i] = 1.0
        for j in range(total_vertices):
            if j != i:
                A[i, j] = - P[i, j]
    A[total_vertices-1, total_vertices-1] = 1.0
    probs_array = np.dot(np.linalg.inv(A), v)

    # O primeiro elemento possui o valor esperado partindo da origem do cubo
    print(probs_array[0,0])

# resolução do problema considerando a condição sobre o penúltimo vértice
for (n, norm_type) in [(3, "L2"), (7, "L2")]:

    total_vertices = int(2**n)

    # Inicialmente resolvemos o sistema para encontrar a probabilidade de, partindo-se de um vértice j, o 
    # penúltimo vértice do passeio ser um vértice pré-determinado
    A = np.zeros(shape = (total_vertices - 1, total_vertices - 1))
    v = np.zeros(shape = (total_vertices - 1, 1))
    P = np.zeros(shape = (total_vertices, total_vertices))

    final_coordinate = []
    for i in range(n-1):
        final_coordinate.append(1)
    final_coordinate.append(0)
    final_coordinate = tuple(final_coordinate)

    list_coordinates = []
    dict_coordinates = {}
    for i in range(total_vertices):
        coordinate = []
        curr_number = i
        for j in range(n):
            coordinate.append(curr_number % 2)
            curr_number = int(curr_number / 2)
        list_coordinates.append(tuple(coordinate))
        dict_coordinates[tuple(coordinate)] = i

    final_pos = dict_coordinates[final_coordinate]

    # Aqui calculamos as probabilidades sem a condição
    for i in range(total_vertices):
        old_coordinate = list(list_coordinates[i])
        curr_sum = 0.0
        for j in range(total_vertices):
            if j != i:
                new_coordinate = list(list_coordinates[j])
                dist = 0.0
                if norm_type == "L2":
                    for k in range(n):
                        dist += (new_coordinate[k] - old_coordinate[k]) ** 2
                    dist = np.sqrt(dist)
                elif norm_type == "L1":
                    for k in range(n):
                        dist += abs(new_coordinate[k] - old_coordinate[k])
                P[i, j] = 1.0 / dist
                curr_sum += 1.0 / dist
        for j in range(total_vertices):
            P[i, j] = P[i, j] / curr_sum

    # Neste loop a matriz A é inicializada com os coeficientes correspondentes para calcularmos as 
    # probabilidades condicionais e, a matriz v, com o valor da probabilidade no penúltimo vértice
    for i in range(total_vertices - 1):
        A[i, i] = 1.0
        if i == final_pos:
            v[i] = P[i, total_vertices - 1]
        for j in range(total_vertices - 1):
            if j != i:
                A[i, j] = - P[i, j]

    # probs_array é o vetor de probabilidades condicionais
    probs_array = np.dot(np.linalg.inv(A), v)

    Q = np.zeros(shape = (total_vertices, total_vertices))
    w = np.zeros(shape = (total_vertices, 1))
    I = np.eye(total_vertices)

    # Aqui resolvemos o problema equivalente, porém transformando todas as probabilidades em condicionais
    for i in range(total_vertices - 1):
        if i < total_vertices:
            w[i] = 1.0
        for j in range(total_vertices - 1):
            Q[i, j] = - P[i, j] * probs_array[j, 0] / probs_array[i, 0]
    print(np.dot(np.linalg.inv(I+Q), w)[0,0])