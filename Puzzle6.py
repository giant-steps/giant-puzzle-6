import numpy as np

for (n, norm_type) in [(3, "L2"), (7, "L2")]:
    total_vertices = int(2**n)
    A = np.zeros(shape = (total_vertices, total_vertices))
    v = np.zeros(shape = (total_vertices, 1))
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

    for i in range(total_vertices - 1):
        A[i, i] = 1.0
        v[i] = 1.0
        for j in range(total_vertices):
            if j != i:
                A[i, j] = - P[i, j]
    A[total_vertices-1, total_vertices-1] = 1.0
    probs_array = np.dot(np.linalg.inv(A), v)
    print(probs_array[0,0])

for (n, norm_type) in [(3, "L2"), (7, "L2")]:

    total_vertices = int(2**n)
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

    for i in range(total_vertices - 1):
        A[i, i] = 1.0
        if i == final_pos:
            v[i] = P[i, total_vertices - 1]
        for j in range(total_vertices - 1):
            if j != i:
                A[i, j] = - P[i, j]
    probs_array = np.dot(np.linalg.inv(A), v)

    Q = np.zeros(shape = (total_vertices, total_vertices))
    w = np.zeros(shape = (total_vertices, 1))
    I = np.eye(total_vertices)

    for i in range(total_vertices - 1):
        if i < total_vertices:
            w[i] = 1.0
        for j in range(total_vertices - 1):
            Q[i, j] = - P[i, j] * probs_array[j, 0] / probs_array[i, 0]
    print(np.dot(np.linalg.inv(I+Q), w)[0,0])