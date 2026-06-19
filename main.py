import networkx as nx
import matplotlib.pyplot as plt

def draw_relationship_graph(mbti):

    relation = mbti_relationships[mbti]

    G = nx.Graph()

    center = mbti
    G.add_node(center)

    colors = []

    node_colors = {
        center: "#CDB4DB"
    }

    for p in relation["best"]:
        G.add_edge(center, p)
        node_colors[p] = "#BDE0FE"

    for p in relation["friend"]:
        G.add_edge(center, p)
        node_colors[p] = "#A2D2FF"

    for p in relation["growth"]:
        G.add_edge(center, p)
        node_colors[p] = "#CAFFBF"

    for p in relation["challenge"]:
        G.add_edge(center, p)
        node_colors[p] = "#FFC8DD"

    pos = nx.spring_layout(G, seed=42)

    plt.figure(figsize=(8,6))

    nx.draw_networkx_nodes(
        G,
        pos,
        node_color=[node_colors[node] for node in G.nodes()],
        node_size=2500
    )

    nx.draw_networkx_edges(
        G,
        pos,
        edge_color="#BDB2FF",
        width=2
    )

    nx.draw_networkx_labels(
        G,
        pos,
        font_size=10,
        font_weight="bold"
    )

    plt.axis("off")

    st.pyplot(plt)
