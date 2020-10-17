graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'G', 'H'],
         'D': ['B'],
         'E': ['B', 'F'],
         'F': ['E'],
         'G': ['C'],
         'H': ['C']}


from collections import deque
# -----------------------------------------------------------
def bfs(graph, root):
    visited = []
    queue = deque([root])

    while queue:
        node = queue.pop()
        if node not in visited:
            visited.append(node)
            queue.extendleft(graph[node])
            # queue += set(graph[node]) - set(visited)
    return visited

print(bfs(graph, 'A'))
# ['A', 'B', 'C', 'D', 'E', 'G', 'H', 'F']


# -----------------------------------------------------------
def bfs_paths(graph, start, end):
    queue = [(start, [start])]
    visited = []

    while queue:
        node1, path = queue.pop(0)
        if node1 == end:
            visited.append(path)
        else:
            for node2 in set(graph[node1]) - set(path):
                queue.append((node2, path + [node2]))
    return visited

print(bfs_paths(graph, 'A', 'H'))
# [['A', 'C', 'H']]
