import networkx as nx

G = nx.Graph()

with open('input.txt', "r") as file:
    for line in file:
        edge = line.strip().split('-')
        if len(edge) == 2:
            G.add_edge(edge[0], edge[1])

cliques_3 = [clique for clique in nx.enumerate_all_cliques(G) if len(clique) == 3]


starts_with_t = 0
for c in cliques_3:
    for n in c:
        if n[0] =='t':
            starts_with_t +=1
            break

print(starts_with_t)

largest_clique = None
largest_size = 0
for c in nx.enumerate_all_cliques(G):
    if len(c) > largest_size:
        largest_size = len(c)
        largest_clique = c
print(','.join(sorted(largest_clique)))