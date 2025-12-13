# Solutions for graph_tasks.ipynb homework

# Task 1: Implement DFS
visited = set()

def dfs(graph, node):
    """Обходит граф в глубину, начиная с node.
    graph: словарь {вершина: [соседи]}
    node: стартовая вершина
    """
    visited.add(node)
    print(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            dfs(graph, neighbor)

# Example graph
graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": [],
    "D": []
}

dfs(graph, "A")
print("Посещено:", visited)

# Graph with cycle
graph_cycle = {
    "A": ["B"],
    "B": ["C"],
    "C": ["A"],  # цикл обратно в A
}

visited = set()
dfs(graph_cycle, "A")
print("Посещено:", visited)

# Task 2: Build overlap graph
reads = ["ATTAC", "TACG", "CGT", "ACG"]

def overlap(a: str, b: str, min_overlap: int = 2) -> int:
    """
    Возвращает длину максимального перекрытия, когда конец a совпадает с началом b.
    Если перекрытие меньше min_overlap, возвращает 0.
    """
    max_olen = 0
    for olen in range(min_overlap, min(len(a), len(b)) + 1):
        if a.endswith(b[:olen]):
            max_olen = olen
    return max_olen

def build_overlap_graph(reads, min_overlap=2):
    graph = {r: [] for r in reads}
    for a in reads:
        for b in reads:
            if a != b:
                olen = overlap(a, b, min_overlap)
                if olen > 0:
                    graph[a].append(b)
    return graph

overlap_graph = build_overlap_graph(reads, min_overlap=2)
print("Overlap graph:", overlap_graph)

# Task 3: Topological sort
def topo_dfs(node, graph, visited, stack):
    visited.add(node)
    for neighbor in graph[node]:
        if neighbor not in visited:
            topo_dfs(neighbor, graph, visited, stack)
    stack.append(node)

def topological_sort_recursive(graph):
    visited = set()
    stack = []
    for node in graph:
        if node not in visited:
            topo_dfs(node, graph, visited, stack)
    stack.reverse()
    return stack

graph_topo = {
    "ATTAC": ["TACG"],
    "TACG": ["CGT"],
    "CGT": []
}

order = topological_sort_recursive(graph_topo)
print("Топологический порядок:", order)

# Task 4: Assemble from order
def assemble_from_order(order, reads_dict):
    if not order:
        return ""
    seq = reads_dict[order[0]]
    for next_read in order[1:]:
        prev = seq
        curr = reads_dict[next_read]
        olen = overlap(prev, curr, min_overlap=1)
        if olen > 0:
            seq += curr[olen:]
    return seq

reads_dict = {r: r for r in reads}
assembled = assemble_from_order(order, reads_dict)
print("Собранная последовательность:", assembled)
