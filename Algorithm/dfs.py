graph = {'A': ['B', 'C'],
         'B': ['A', 'D', 'E'],
         'C': ['A', 'G', 'H'],
         'D': ['B'],
         'E': ['B', 'F'],
         'F': ['E'],
         'G': ['C'],
         'H': ['C']}



# -----------------------------------------------------------
def dfs(graph, root):
    visited = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.append(node)
            # stack.extend(graph[node])
            # stack += set(graph[node]) - set(visited)
    return visited

print(dfs(graph, 'A'))
# ['A', 'C', 'H', 'G', 'B', 'E', 'F', 'D']

# -----------------------------------------------------------
def dfs_path(graph, start, end):
    visited = []
    stack = [(start, [start])]
    while stack:
        node, path = stack.pop()
        if node == end:
            visited.append(path)
        else:
            for node2 in set(graph[node]) - set(path):
                stack.append((node2, path + [node2]))
    return visited

print(dfs_path(graph, 'A', 'H'))
# [['A', 'C', 'H']]


# -----------------------------------------------------------
def dfs_recursive(graph, root, visited = []):
    visited.append(root)
    for node in graph[root]:
        if node not in visited:
            dfs_recursive(graph, node, visited)
    return visited

print(dfs_recursive(graph, 'A'))
# ['A', 'B', 'D', 'E', 'F', 'C', 'G', 'H']

# -----------------------------------------------------------
paths = []
def dfs_path_recursive(graph, start, end, visited = []):
    visited = visited + [start]
    if start == end:
        paths.append(visited)
    for node in graph[start]:
        if node not in visited:
            dfs_path_recursive(graph, node, end, visited)

dfs_path_recursive(graph, 'A', 'H')
print(paths)
# [['A', 'C', 'H']]