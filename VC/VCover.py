import networkx as nx
import numpy as np
import random as rd
import matplotlib.pyplot as plt


def add_bitwise(a, b):
    for i in range(len(a)):
        a[i] = int(a[i]) | int(b[i])
    return a

def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    pos = _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)
    return pos

def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None, parsed=None):
    if pos is None:
        pos = {root: (xcenter, vert_loc)}
    else:
        pos[root] = (xcenter, vert_loc)
    if parsed is None:
        parsed = set()
    parsed.add(root)
    neighbors = list(G.neighbors(root))
    if not isinstance(G, nx.DiGraph) and parent is not None:
        neighbors.remove(parent)  
    if len(neighbors) != 0:
        dx = width / len(neighbors) 
        nextx = xcenter - width/2 - dx/2
        for neighbor in neighbors:
            nextx += dx
            pos = _hierarchy_pos(G, neighbor, width=dx, vert_gap=vert_gap, vert_loc=vert_loc-vert_gap, xcenter=nextx, pos=pos, parent=root, parsed=parsed)
    return pos



def is_a_vertex_cover_v2(G, vertex_cover):
    # Check if all edges are covered by the vertex cover
    for i in G.edges():
        if i[0] not in vertex_cover and i[1] not in vertex_cover:
            return False
    return True
def plotgraph(G):
    
    figure=plt.figure(figsize=(12, 6))
    plt.subplot(121)
    nb_node=len(G.nodes)
    labels = {i: G.nodes[i]["name"] for i in range(1,nb_node+1)}
    nx.draw(G, None, with_labels=True,labels=labels, font_weight='bold')
    plt.title("Graphe initial")
    return figure


def BnB_vertex(G,mode):
    M = nx.incidence_matrix(G)
    M = M.todense()
    nb_node = G.number_of_nodes()
    size_min = nb_node
    vertex_cover_min = []
    covered = np.zeros(G.number_of_edges())
    edges = list(G.edges)
    rd.shuffle(edges)
    print(edges)
    UI=mode["UI"]
    if UI:
        figure=plotgraph(G)
    while not plt.waitforbuttonpress():
        pass
    
    # Graph for the state tree
    state_tree = nx.DiGraph()
    state_id = 0
    root_id = state_id
    state_tree.add_node(state_id, label="root", cover=[], remaining_edges=edges.copy(), covered=covered.copy())
    nb_iter = 0
    
    TREE=mode["tree"]
    VERBOSE=mode["verbose"]
    PARA=False
    SPACE=mode["space"]
    if VERBOSE==2:print(edges)
    


    def iter(vertex_cover, remaining_edges, covered, parent_id, depth):
        nonlocal vertex_cover_min, size_min, state_id, nb_iter,PARA
        
        if PARA:
            PARA=False
            return
        if  is_a_vertex_cover_v2(G,vertex_cover):  # If all edges are covered
            if len(vertex_cover) < size_min:
                PARA=True
                vertex_cover_min = [vertex_cover[:]]  # Update the minimum vertex cover
                size_min = len(vertex_cover)
                if VERBOSE >= 1:
                    vc_min_print=[str(G.nodes[i]["name"]) for i in vertex_cover_min[0]]
                    print("vertex_cover_min =", vc_min_print, "size =", size_min, "and we are at", nb_iter, "iterations")
            return

        if not remaining_edges:
            if VERBOSE == 2:
                print("fin")
            return
        
        if len(vertex_cover) == size_min - 1 and not is_a_vertex_cover_v2(G,vertex_cover):
            if VERBOSE == 2:
                print("pas mieux")
            return
        PARA=False
        # Take the next edge to branch
        u, v = remaining_edges[0]
        if VERBOSE == 2:
            print("on a :", remaining_edges, "on choisit :", (u, v))
        new_remaining_edges = remaining_edges[1:]
        nb_iter += 1
        if VERBOSE == 2:
            print(nb_iter)
        if G.degree[v]>G.degree[u] and mode["heuristique"]:
            print("heur")
            temp=v
            v=u
            u=temp

        for node in (u, v):
            new_covered = add_bitwise(covered.copy(), M[node - 1, :])

            # Remove edges neighboring the chosen node
            updated_edges = [edge for edge in new_remaining_edges if node not in edge]

            if TREE:
                # Add the new state to the state tree
                state_id += 1
                state_tree.add_node(state_id, label=G.nodes[node]["name"], cover=vertex_cover + [node], remaining_edges=updated_edges, covered=new_covered)
                state_tree.add_edge(parent_id, state_id)
                
                # Display the updated state tree
                pos = _hierarchy_pos(state_tree, root=0)
                labels = nx.get_node_attributes(state_tree, 'label')
                plt.subplot(122)
                plt.cla()
                nx.draw(state_tree, pos, with_labels=True, labels=labels, node_size=120, node_color="lightblue", font_size=5, font_weight="bold", arrows=True)
                if PARA:
                    while not plt.waitforbuttonpress():
                        pass
                plt.title("Arbre des états")
                plt.pause(0.01)
                

                # Wait for spacebar press if enabled
                if SPACE:
                    while not plt.waitforbuttonpress():
                        pass

            iter(vertex_cover + [node], updated_edges, new_covered, state_id, depth + 1)

    iter([], edges, covered, root_id, 0)
    if len(vertex_cover_min)==0:
        print("error")
        return [666],state_tree,nb_iter,figure
    else:
        return vertex_cover_min[0], state_tree,nb_iter,figure

def load_graph(mode):
    G = nx.Graph()
    
    
    if mode["graphe"]=="AUGMENTEE":
        n_animaux=["chèvre","choux","loup","rat","lion"]
        for i in range(1,len(n_animaux)+1): 
            G.add_nodes_from([(i, {'name': n_animaux[i-1]})])
        G.add_edges_from([(1, 2), (1, 3), (1, 5), (2, 4)])
    elif mode["graphe"]=="ORIGINALE":
        n_animaux=["chèvre","choux","loup"]
        for i in range(1,len(n_animaux)+1): 
            G.add_nodes_from([(i, {'name': n_animaux[i-1]})])
        G.add_edges_from([(1, 2), (1, 3)])
        
    elif mode["graphe"]=="DIFFICILE":
        n_animaux=["poisson","ours","chèvre","choux","loup","aigle","rat","chèvre"]
        for i in range(1,len(n_animaux)+1): 
            G.add_nodes_from([(i, {'name': n_animaux[i-1]})])
        G.add_edges_from([(1, 2), (2, 3), (3, 4), (3, 5),(1, 6),(3,6),(6,7),(4,7),(2,8),(8,4),(8,6),(8,5)])
    elif mode["graphe"]=="MAISON":
        edges = [
            (1, 2), (1, 3), (2, 4), (3, 5), (4, 6),
            (5, 7), (6, 8), (7, 9), (8, 10), (9, 11),
            (10, 12), (11, 2), (12, 3), (13, 4), (14, 6),
            (15, 7), (16, 5), (17, 2), (18, 9), (19, 1),
            (20, 2), (3, 14), (5, 18), (7, 16), (8, 12)
        ]
        G.add_edges_from(edges)
        for i in G.nodes:
            G.nodes[i]["name"]=str(i)
    elif mode["graphe"]=="CONTRE-EXEMPLE":
        
        n_animaux=["chèvre","lion","loup","aigle"]
        for i in range(1,len(n_animaux)+1): 
            G.add_nodes_from([(i, {'name': n_animaux[i-1]})])
        G.add_edges_from([(1, 2), (1, 3),(1, 4)])
    elif mode["graphe"]=="POISSON":
        n_animaux=["poisson","ours","chèvre","choux","loup","aigle"]
        for i in range(1,len(n_animaux)+1): 
            G.add_nodes_from([(i, {'name': n_animaux[i-1]})])
        G.add_edges_from([(1, 2), (2, 3), (3, 4), (3, 5),(1, 6),(3,6)])
    return G

 
if __name__ == '__main__':
    # Set appropriate flags
    mode={"UI":True,"tree":True,"verbose":1,"space":False,"graphe":"POISSON","heuristique":True}
    G = load_graph(mode)
    vertex_cover_min, state_tree,nb_iter,frame = BnB_vertex(G,mode)
    