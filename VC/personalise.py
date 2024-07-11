#animals={"carnivores":5,"carnivores":6}
import networkx as nx

import matplotlib.pyplot as plt



def fill_graph(amount):
    G = nx.Graph()
    carnivores = [
    "loup",
    "tigre",
    "lion",
    "cobra",
    "loup gris",
    "panthère",
    "ours polaire",
    "guépard",
    "crocodile",
    "hyène"
    ]

    herbivores = [
    "éléphant",
    "girafe",
    "zèbre",
    "cheval",
    "vache",
    "cerf",
    "kangourou",
    "panda",
    "rhino",
    "mouton"
    ]

    vegetals = [
    "choux",
    "foin",
    "herbe",
    "sapin",
    "tomate",
    "pissenlit",
    "rose",
    "fougère",
    "cactus",
    "tulipe"
    ]
    omnivores = [
    "rat",
    "cochon",
    "raton laveur",
    "corbeau",
    "poule",
    "chacal",
    "sanglier",
    "chimpanzé",
    "putois",
    "renard"
    ]
    grains=[
        "blé",
        "riz",
        "maïs",
        "avoine",
        "seigle"
    ]

    deb=0
    if amount["carnivores"]!=0:
        for i in range(amount["carnivores"]):
            G.add_nodes_from([(i+deb+1, {"name": carnivores[i]})])
    deb+=amount["carnivores"]

    if amount["herbivores"]!=0:
        for i in range(amount["herbivores"]):
            G.add_nodes_from([(i+deb+1, {"name": herbivores[i]})])
            for j in range(amount["carnivores"]):
                G.add_edge(i+deb+1,j+1)
    deb+=amount["herbivores"]
    print(G.nodes.data())
    if amount["vegetals"]!=0:
        for i in range(amount["vegetals"]):
            G.add_nodes_from([(i+deb+1, {"name": vegetals[i]})])
            for j in range(amount["herbivores"]):
                G.add_edge(i+deb+1,j+amount["carnivores"]+1)
    deb+=amount["vegetals"]
    
    if amount["omnivores"]!=0:
        for i in range(amount["omnivores"]):
            G.add_nodes_from([(i+deb+1, {"name": omnivores[i]})])
            for j in range(amount["vegetals"]):
                G.add_edge(i+deb+1,j+amount["carnivores"]+amount["herbivores"]+1)
            for j in range(amount["carnivores"]+1):
                G.add_edge(i+deb+1,j+1)
    deb+=amount["omnivores"]

    if amount["grains"]!=0:
        for i in range(amount["grains"]):
            G.add_nodes_from([(i+deb+1, {"name": grains[i]})])
            for j in range(amount["omnivores"]):
                G.add_edge(i+deb+1,j+amount["carnivores"]+amount["herbivores"]+amount["vegetals"]+1)

    return G

if __name__ == '__main__':
    amount={
        "carnivores":3,
        "herbivores":2,
        "vegetals":1,
        "omnivores":2,
        "grains":1,
        "tot":9,
    }
    G=fill_graph(amount)
    labels = {i: G.nodes[i]["name"] for i in range(1,amount["tot"]+1)}

    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    nx.draw(G, None, with_labels=True,labels=labels, font_weight='bold')
    plt.title("Graphe initial")
    plt.show()