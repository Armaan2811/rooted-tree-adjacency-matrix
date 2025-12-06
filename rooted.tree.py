from collections import deque
import matplotlib.pyplot as plt


def build_tree_from_adj_matrix(adj, root):
    n = len(adj)
    parent = [-1] * n
    level = [0] * n
    children = [[] for _ in range(n)]

    q = deque([root])
    visited = [False] * n
    visited[root] = True

    while q:
        u = q.popleft()
        for v in range(n):
            if adj[u][v] == 1 and not visited[v]:
                visited[v] = True
                parent[v] = u
                level[v] = level[u] + 1
                children[u].append(v)
                q.append(v)

    return parent, children, level


def get_ancestors(parent, v):
    anc = []
    cur = v
    while parent[cur] != -1:
        cur = parent[cur]
        anc.append(cur)
    anc.reverse()
    return anc


def get_descendants(children, v):
    desc = []
    stack = children[v][:]
    while stack:
        u = stack.pop()
        desc.append(u)
        stack.extend(children[u])
    return desc


def compute_positions(children, root):
    """Place nodes level by level; minimal layout."""
    pos = {}
    levels = {}

    def dfs(u, d):
        levels.setdefault(d, []).append(u)
        for w in children[u]:
            dfs(w, d + 1)

    dfs(root, 0)

    for d, nodes in levels.items():
        k = len(nodes)
        xs = [i - (k - 1) / 2 for i in range(k)]  # centered
        y = -d
        for u, x in zip(nodes, xs):
            pos[u] = (x, y)

    return pos


def draw_minimal_tree(children, root):
    pos = compute_positions(children, root)
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.axis("off")

    # edges
    for u in range(len(children)):
        for v in children[u]:
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            ax.plot([x1, x2], [y1, y2], color="black", linewidth=1.5)

    # nodes
    for u, (x, y) in pos.items():
        if u == root:
            ax.scatter(x, y, s=120, color="gold", edgecolors="black", zorder=3)
        else:
            ax.scatter(x, y, s=80, color="lightblue",
                       edgecolors="black", zorder=3)
        ax.text(x, y + 0.08, str(u), ha="center", va="bottom", fontsize=9)

    plt.tight_layout()
    plt.show()


def main():
    n = int(input("Enter number of vertices n: "))
    print("Enter adjacency matrix (each row as n space-separated 0/1):")
    adj = []
    for i in range(n):
        row = list(map(int, input(f"Row {i}: ").split()))
        if len(row) != n:
            raise ValueError("Each row must have exactly n entries")
        adj.append(row)

    root = int(input(f"Enter root vertex index (0..{n-1}): "))
    v = int(input(f"Enter vertex to analyze (0..{n-1}): "))

    parent, children, level = build_tree_from_adj_matrix(adj, root)

    parent_v = parent[v] if parent[v] != -1 else None
    children_v = children[v]
    ancestors_v = get_ancestors(parent, v)
    descendants_v = get_descendants(children, v)
    level_v = level[v]

    print(f"\nVertex {v}")
    print("Parent     :", parent_v)
    print("Children   :", children_v)
    print("Ancestors  :", ancestors_v)
    print("Descendants:", descendants_v)
    print("Level      :", level_v)

    draw_minimal_tree(children, root)


if __name__ == "__main__":
    main()
