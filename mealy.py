def execute(entry, state, machine):
    in_matrix, out_matrix = machine
    out = []
    for w in entry:
        out.append(out_matrix[state][w])
        state = in_matrix[state][w]
    return out

def dual(machine):
    in_matrix, out_matrix = machine
    in_ret = [[None for i in range(len(in_matrix))] for j in range(len(out_matrix))]
    out_ret = [[None for i in range(len(in_matrix))] for j in range(len(out_matrix))]
    for p in range(len(in_matrix)):
        for x in range(len(out_matrix)):
            in_ret[x][p] = out_matrix[p][x]
            out_ret[x][p] = in_matrix[p][x]

    return in_ret, out_ret

def inverse(machine):
    in_matrix, out_matrix = machine
    in_ret = [[None for i in range(len(out_matrix))] for j in range(len(in_matrix))]
    out_ret = [[None for i in range(len(out_matrix))] for j in range(len(in_matrix))]
    for p in range(len(in_matrix)):
        for x in range(len(out_matrix)):
            q, y = in_matrix[p][x], out_matrix[p][x]
            if in_ret[p][y] != None: return False
            in_ret[p][y] = q
            out_ret[p][y] = x
    return in_ret, out_ret
