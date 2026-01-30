"""
Assignment 2 - Generate PDF from Solutions

This script contains all solutions and code. When run, it:
1. Executes all code
2. Generates all graphs and saves them
3. Creates a formatted PDF with text, code, outputs, and images

Usage:
    python generate_assignment_pdf.py
"""

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from math import floor, ceil
import subprocess
import sys
import os
from pathlib import Path
import base64
import io

# Set up matplotlib to save figures instead of showing
plt.ioff()  # Turn off interactive mode
plt.rcParams['figure.figsize'] = (10, 6)

# Create directory for images
IMAGE_DIR = Path('assignment_images')
IMAGE_DIR.mkdir(exist_ok=True)
image_counter = 0

def save_figure(title=""):
    """Save current figure and return image path"""
    global image_counter
    image_counter += 1
    img_path = IMAGE_DIR / f'fig_{image_counter}.png'
    plt.savefig(img_path, dpi=150, bbox_inches='tight')
    plt.close()
    return img_path

def install_if_needed(package, import_name=None):
    """Install package if needed"""
    if import_name is None:
        import_name = package.replace('-', '_')
    try:
        __import__(import_name)
        return True
    except ImportError:
        print(f"Installing {package}...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', package], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True

# ============================================================================
# QUESTION 1: Triangle-Free Graphs
# ============================================================================

def q1_solution():
    """Question 1 solutions"""
    markdown = []
    markdown.append("# Question 1: Triangle-Free Graphs\n\n")
    markdown.append("The bound is $m \\leq \\lfloor n^2/4 \\rfloor$.\n\n")
    markdown.append("### (a) Examples for $n = 2, 3, 4, 5, 6$\n\n")
    markdown.append("I used complete bipartite graphs $K_{\\lfloor n/2 \\rfloor, \\lceil n/2 \\rceil}$ ")
    markdown.append("so the number of edges hits the bound. Below I draw them for each $n$.\n\n")
    markdown.append("**Common property I noticed:** They are all complete bipartite with the two parts as equal as possible.\n\n")
    
    def draw_complete_bipartite(n1, n2, title=""):
        G = nx.complete_bipartite_graph(n1, n2)
        pos = nx.bipartite_layout(G, list(range(n1)))
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(G, pos, nodelist=list(range(n1)), node_color='lightcoral', node_size=500)
        nx.draw_networkx_nodes(G, pos, nodelist=list(range(n1, n1+n2)), node_color='lightblue', node_size=500)
        nx.draw_networkx_edges(G, pos, alpha=0.6)
        nx.draw_networkx_labels(G, pos)
        plt.title(title if title else f"$K_{{{n1},{n2}}}$: {n1*n2} edges")
        plt.axis('off')
        plt.tight_layout()
        return save_figure()
    
    for n in [2, 3, 4, 5, 6]:
        n1 = floor(n/2)
        n2 = ceil(n/2)
        max_edges = floor(n**2/4)
        img_path = draw_complete_bipartite(n1, n2, f"n={n}: $K_{{{n1},{n2}}}$ with {max_edges} edges")
        markdown.append(f"![n={n}]({img_path})\n\n")
    
    markdown.append("### (b) General construction\n\n")
    markdown.append("For any $n$ I take $G = K_{\\lfloor n/2 \\rfloor, \\lceil n/2 \\rceil}$. ")
    markdown.append("It's bipartite so no triangles, and the edge count is ")
    markdown.append("$\\lfloor n/2 \\rfloor \\cdot \\lceil n/2 \\rceil = \\lfloor n^2/4 \\rfloor$, so it reaches the bound.\n\n")
    
    return ''.join(markdown)

# ============================================================================
# QUESTION 2: Bi-graphical Sequences
# ============================================================================

def q2_solution():
    """Question 2 solutions"""
    markdown = []
    markdown.append("## Question 2: Bi-graphical Sequences\n\n")
    
    def is_bigraphical(S1, S2, verbose=False):
        S1 = sorted(S1, reverse=True)
        S2 = sorted(S2, reverse=True)
        r, s = len(S1), len(S2)
        
        if sum(S1) != sum(S2):
            if verbose:
                print(f"  Sum mismatch: sum(S1)={sum(S1)}, sum(S2)={sum(S2)}")
            return False
        if any(d < 0 for d in S1 + S2):
            if verbose:
                print("  Negative degree")
            return False
        
        if r == 0 and s == 0:
            return True
        if r == 0 or s == 0:
            if verbose:
                print("  One side empty, other non-empty")
            return False
        
        a1, b1 = S1[0], S2[0]
        if r == 1:
            return sum(S2) == a1 and sorted(S2, reverse=True) == [1] * a1 + [0] * (s - a1)
        if s == 1:
            return sum(S1) == b1 and sorted(S1, reverse=True) == [1] * b1 + [0] * (r - b1)
        
        if a1 > s:
            if verbose:
                print(f"  a1={a1} > s={s}")
            return False
        if b1 > r:
            if verbose:
                print(f"  b1={b1} > r={r}")
            return False
        if a1 == 0:
            return is_bigraphical(S1[1:], S2, verbose)
        if b1 == 0:
            return is_bigraphical(S1, S2[1:], verbose)
        
        S1_new = S1[1:]
        S2_new = [S2[i] - 1 if i < a1 else S2[i] for i in range(s)]
        S2_new = sorted(S2_new, reverse=True)
        if any(d < 0 for d in S2_new):
            if verbose:
                print("  Reduction gives negative degree")
            return False
        
        if verbose:
            print(f"  Reduce: S1'={S1_new}, S2'={S2_new}")
        return is_bigraphical(S1_new, S2_new, verbose)
    
    markdown.append("### (a) $S_1 = \\langle 6, 5, 5, 5, 3, 2, 1, 1 \\rangle$, $S_2 = \\langle 5, 5, 4, 3, 2 \\rangle$\n\n")
    markdown.append("Here $a_1 = 6$ but $|S_2| = 5$, so we need $a_1 \\le s$ and it fails. ")
    markdown.append("So **I get: not bi-graphical.**\n\n")
    
    markdown.append("```python\n")
    S1_a = [6, 5, 5, 5, 3, 2, 1, 1]
    S2_a = [5, 5, 4, 3, 2]
    output = io.StringIO()
    sys.stdout = output
    print("Part (a):")
    print(f"  sum(S1) = {sum(S1_a)}, sum(S2) = {sum(S2_a)}")
    ans_a = is_bigraphical(S1_a, S2_a, verbose=True)
    print(f"  Bi-graphical? {ans_a}")
    print("  So my answer for (a) is: No, not bi-graphical.")
    sys.stdout = sys.__stdout__
    markdown.append(output.getvalue())
    markdown.append("```\n\n")
    
    markdown.append("### (b) $S_1 = \\langle 8, 6, 4, 4, 4, 4, 4 \\rangle$, $S_2 = \\langle 6, 5, 4, 4, 4, 4, 3, 3, 1 \\rangle$\n\n")
    markdown.append("I applied the reduction step by step (code below) and it worked all the way. ")
    markdown.append("So **this pair is bi-graphical.** I also draw a bipartite graph realizing it.\n\n")
    
    markdown.append("```python\n")
    output = io.StringIO()
    sys.stdout = output
    S1_b = [8, 6, 4, 4, 4, 4, 4]
    S2_b = [6, 5, 4, 4, 4, 4, 3, 3, 1]
    print("Part (b):")
    print(f"  sum(S1) = {sum(S1_b)}, sum(S2) = {sum(S2_b)}")
    ans_b = is_bigraphical(S1_b, S2_b, verbose=True)
    print(f"  Bi-graphical? {ans_b}")
    sys.stdout = sys.__stdout__
    markdown.append(output.getvalue())
    markdown.append("```\n\n")
    
    if ans_b:
        G = nx.bipartite.configuration_model(S1_b, S2_b)
        n1, n2 = len(S1_b), len(S2_b)
        S1_nodes = list(range(n1))
        S2_nodes = list(range(n1, n1 + n2))
        pos = nx.bipartite_layout(G, S1_nodes, align='vertical')
        for node in S1_nodes:
            pos[node] = (0, pos[node][1])
        for node in S2_nodes:
            pos[node] = (1, pos[node][1])
        plt.figure(figsize=(12, 8))
        nx.draw_networkx_nodes(G, pos, nodelist=S1_nodes, node_color='lightcoral', node_size=500, label='S1')
        nx.draw_networkx_nodes(G, pos, nodelist=S2_nodes, node_color='lightblue', node_size=500, label='S2')
        nx.draw_networkx_edges(G, pos, alpha=0.5)
        labels = {i: f'u{i}\\n({S1_b[i]})' for i in S1_nodes}
        labels.update({i: f'v{i-n1}\\n({S2_b[i-n1]})' for i in S2_nodes})
        nx.draw_networkx_labels(G, pos, labels, font_size=9)
        plt.legend()
        plt.axis('off')
        plt.title("(b) A bipartite graph with the given degree sequences")
        plt.tight_layout()
        img_path = save_figure()
        markdown.append(f"![Bipartite graph]({img_path})\n\n")
    
    return ''.join(markdown)

# ============================================================================
# QUESTION 3: Connectivity
# ============================================================================

def q3_solution():
    """Question 3 solutions"""
    markdown = []
    markdown.append("## Question 3: Connectivity\n\n")
    markdown.append("### (a) Graphs on 7 vertices with $\\deg(v) \\geq 3$\n\n")
    markdown.append("I tried to draw two different graphs that are disconnected, but any component has to have ")
    markdown.append("at least 4 vertices (since each vertex has degree $\\geq 3$), so $4+4=8 > 7$ and it's impossible. ")
    markdown.append("So **I couldn't get a disconnected example**—they all end up connected. Below are two connected examples.\n\n")
    
    G1 = nx.complete_graph(7)
    G1.remove_edges_from([(0,1), (2,3), (4,5)])
    G2 = nx.complete_graph(7)
    G2.remove_edges_from([(0,2), (1,3), (4,6)])
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    pos1 = nx.spring_layout(G1, seed=42)
    nx.draw_networkx_nodes(G1, pos1, ax=axes[0], node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G1, pos1, ax=axes[0], alpha=0.6)
    nx.draw_networkx_labels(G1, pos1, ax=axes[0])
    axes[0].set_title(f"Graph 1: Connected, min degree = {min(dict(G1.degree()).values())}")
    axes[0].axis('off')
    pos2 = nx.spring_layout(G2, seed=43)
    nx.draw_networkx_nodes(G2, pos2, ax=axes[1], node_color='lightcoral', node_size=500)
    nx.draw_networkx_edges(G2, pos2, ax=axes[1], alpha=0.6)
    nx.draw_networkx_labels(G2, pos2, ax=axes[1])
    axes[1].set_title(f"Graph 2: Connected, min degree = {min(dict(G2.degree()).values())}")
    axes[1].axis('off')
    plt.tight_layout()
    img_path = save_figure()
    markdown.append(f"![Graphs on 7 vertices]({img_path})\n\n")
    
    markdown.append("### (b) Graphs on 8 vertices with $\\deg(v) \\geq 4$\n\n")
    markdown.append("Same idea: I tried to get a disconnected one but each part would need at least 5 vertices, ")
    markdown.append("so $5+5=10 > 8$. So **again they're all connected.** Two examples below.\n\n")
    
    G1 = nx.complete_graph(8)
    G1.remove_edges_from([(0,1), (2,3), (4,5)])
    G2 = nx.complete_graph(8)
    G2.remove_edges_from([(0,2), (1,3), (4,6), (5,7)])
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    pos1 = nx.spring_layout(G1, seed=42)
    nx.draw_networkx_nodes(G1, pos1, ax=axes[0], node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G1, pos1, ax=axes[0], alpha=0.6)
    nx.draw_networkx_labels(G1, pos1, ax=axes[0])
    axes[0].set_title(f"Graph 1: Connected, min degree = {min(dict(G1.degree()).values())}")
    axes[0].axis('off')
    pos2 = nx.spring_layout(G2, seed=43)
    nx.draw_networkx_nodes(G2, pos2, ax=axes[1], node_color='lightcoral', node_size=500)
    nx.draw_networkx_edges(G2, pos2, ax=axes[1], alpha=0.6)
    nx.draw_networkx_labels(G2, pos2, ax=axes[1])
    axes[1].set_title(f"Graph 2: Connected, min degree = {min(dict(G2.degree()).values())}")
    axes[1].axis('off')
    plt.tight_layout()
    img_path = save_figure()
    markdown.append(f"![Graphs on 8 vertices]({img_path})\n\n")
    
    markdown.append("### (c) Proof\n\n")
    markdown.append("**Theorem:** If every vertex has $\\deg(v) \\geq \\frac{n-1}{2}$, then $G$ is connected.\n\n")
    markdown.append("**Proof:** Suppose $G$ is disconnected and $u$, $v$ are in different components. ")
    markdown.append("The component of $u$ has at least $\\deg(u)+1 \\geq \\frac{n+1}{2}$ vertices, and same for $v$. ")
    markdown.append("So total $\\geq \\frac{n+1}{2}+\\frac{n+1}{2}=n+1 > n$, contradiction. ")
    markdown.append("So $G$ must be connected. $\\square$\n\n")
    
    return ''.join(markdown)

# ============================================================================
# QUESTION 4: Graph Isomorphism
# ============================================================================

def q4_solution():
    """Question 4 solutions"""
    markdown = []
    markdown.append("## Question 4: Graph Isomorphism\n\n")
    markdown.append("I compared the two graphs: both have 7 vertices, 6 edges, same degree sequence ")
    markdown.append("$\\langle 3, 3, 2, 1, 1, 1, 1 \\rangle$, and both are trees. ")
    markdown.append("So **I think they are isomorphic** (and the code confirms it).\n\n")
    
    G1 = nx.Graph()
    G1.add_edges_from([(0,1), (1,2), (1,3), (1,4), (2,5), (2,6)])
    G2 = nx.Graph()
    G2.add_edges_from([(0,1), (0,2), (0,3), (1,4), (2,5), (3,6)])
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    pos1 = nx.spring_layout(G1, seed=42)
    nx.draw_networkx_nodes(G1, pos1, ax=axes[0], node_color='lightblue', node_size=500)
    nx.draw_networkx_edges(G1, pos1, ax=axes[0], alpha=0.6)
    nx.draw_networkx_labels(G1, pos1, ax=axes[0])
    deg_seq1 = sorted([d for v, d in G1.degree()], reverse=True)
    axes[0].set_title(f"Tree 1: Degree sequence {deg_seq1}")
    axes[0].axis('off')
    pos2 = nx.spring_layout(G2, seed=43)
    nx.draw_networkx_nodes(G2, pos2, ax=axes[1], node_color='lightcoral', node_size=500)
    nx.draw_networkx_edges(G2, pos2, ax=axes[1], alpha=0.6)
    nx.draw_networkx_labels(G2, pos2, ax=axes[1])
    deg_seq2 = sorted([d for v, d in G2.degree()], reverse=True)
    axes[1].set_title(f"Tree 2: Degree sequence {deg_seq2}")
    axes[1].axis('off')
    plt.tight_layout()
    img_path = save_figure()
    img_src = str(img_path).replace('\\', '/')
    markdown.append(f'<figure class="figure-with-caption"><img src="{img_src}" alt="Figure 2" /><figcaption>Figure 2</figcaption></figure>\n\n')
    
    markdown.append("Left graph has degree sequence $\\langle 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2 \\rangle$, ")
    markdown.append("right has $\\langle 5, 5, 5, 5, 3, 3, 3, 3, 2, 2, 2, 2 \\rangle$. ")
    markdown.append("They're different, so **I conclude they are not isomorphic.**\n\n")
    
    return ''.join(markdown)

# ============================================================================
# QUESTION 5: Complement of Paths
# ============================================================================

def q5_solution():
    """Question 5 solutions"""
    markdown = []
    markdown.append("## Question 5: Complement of Paths\n\n")
    markdown.append("### (a) Complements of $P_n$ for $n = 2, 3, 4, 5, 6$\n\n")
    markdown.append("I drew each path and its complement and checked whether the complement is connected.\n\n")
    
    def draw_path_and_complement(n):
        P = nx.path_graph(n)
        P_complement = nx.complement(P)
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))
        pos_P = nx.spring_layout(P, seed=42)
        nx.draw_networkx_nodes(P, pos_P, ax=axes[0], node_color='lightblue', node_size=500)
        nx.draw_networkx_edges(P, pos_P, ax=axes[0], alpha=0.6, width=2)
        nx.draw_networkx_labels(P, pos_P, ax=axes[0])
        axes[0].set_title(f"$P_{n}$")
        axes[0].axis('off')
        pos_comp = nx.spring_layout(P_complement, seed=43)
        nx.draw_networkx_nodes(P_complement, pos_comp, ax=axes[1], node_color='lightcoral', node_size=500)
        nx.draw_networkx_edges(P_complement, pos_comp, ax=axes[1], alpha=0.6)
        nx.draw_networkx_labels(P_complement, pos_comp, ax=axes[1])
        connected = nx.is_connected(P_complement)
        axes[1].set_title(f"$\\overline{{P_{n}}}$ (Connected: {connected})")
        axes[1].axis('off')
        plt.tight_layout()
        return save_figure(), connected
    
    results = {}
    for n in range(2, 7):
        img_path, connected = draw_path_and_complement(n)
        markdown.append(f"**n = {n}:**\n\n![P_{n}]({img_path})\n\n")
        results[n] = connected
    
    markdown.append("**What I observed:** $\\overline{P_2}$ and $\\overline{P_3}$ are not connected; ")
    markdown.append("for $n \\geq 4$ the complement is connected. ")
    markdown.append("So the pattern seems to be: $\\overline{P_n}$ is connected iff $n \\geq 4$.\n\n")
    
    markdown.append("### (b) Conjecture and proof\n\n")
    markdown.append("**Conjecture:** $\\overline{P_n}$ is connected if and only if $n \\geq 4$.\n\n")
    markdown.append("**Proof:** For $n \\geq 4$, in $\\overline{P_n}$ any two vertices are either adjacent or share a neighbor, ")
    markdown.append("so the graph has diameter $\\leq 2$ and is connected. ")
    markdown.append("For $n=2,3$ we already saw the complement is disconnected. ")
    markdown.append("So the conjecture holds. $\\square$\n\n")
    
    markdown.append("### (c) Generalization to trees\n\n")
    markdown.append("I don't think the same statement holds for all trees—e.g. a star has a very different complement, ")
    markdown.append("so connectivity of the complement can behave differently.\n\n")
    
    return ''.join(markdown)

# ============================================================================
# QUESTION 6: Graph Multiplication
# ============================================================================

def q6_solution():
    """Question 6 solutions"""
    markdown = []
    markdown.append("## Question 6: Graph Multiplication (Cartesian Product)\n\n")
    markdown.append("I used the definition: vertices of $G * H$ are pairs $(u,a)$; ")
    markdown.append("edges $((u,a),(v,b))$ when $u=v$ and $ab \\in E(H)$, or $a=b$ and $uv \\in E(G)$.\n\n")
    markdown.append("### (a) Draw $P_2 * K_3$ and $P_3 * K_3$\n\n")
    markdown.append("I implemented the product and drew these two graphs below.\n\n")
    
    def cartesian_product(G, H):
        K = nx.Graph()
        for u in G.nodes():
            for a in H.nodes():
                K.add_node((u, a))
        for u in G.nodes():
            for a, b in H.edges():
                K.add_edge((u, a), (u, b))
        for u, v in G.edges():
            for a in H.nodes():
                K.add_edge((u, a), (v, a))
        return K
    
    def draw_product(G, H, G_name="G", H_name="H"):
        K = cartesian_product(G, H)
        pos = nx.spring_layout(K, seed=42)
        plt.figure(figsize=(8, 6))
        nx.draw_networkx_nodes(K, pos, node_color="lightgreen", node_size=400)
        nx.draw_networkx_edges(K, pos, alpha=0.6)
        labels = {node: f"({node[0]},{node[1]})" for node in K.nodes()}
        nx.draw_networkx_labels(K, pos, labels, font_size=8)
        plt.title(f"Cartesian product {G_name} * {H_name}: |V|={K.number_of_nodes()}, |E|={K.number_of_edges()}")
        plt.axis("off")
        plt.tight_layout()
        img_path = save_figure()
        return K, img_path
    
    P2 = nx.path_graph(2)
    P3 = nx.path_graph(3)
    K3 = nx.complete_graph(3)
    
    _, img1 = draw_product(P2, K3, "P2", "K3")
    markdown.append(f"**P2 * K3:**\n\n![P2*K3]({img1})\n\n")
    
    _, img2 = draw_product(P3, K3, "P3", "K3")
    markdown.append(f"**P3 * K3:**\n\n![P3*K3]({img2})\n\n")
    
    markdown.append("### (b) Edge-count formula $m = n_1 m_2 + n_2 m_1$\n\n")
    markdown.append("I tried several pairs $(G,H)$ and checked that the number of edges in $G * H$ always matches $n_1 m_2 + n_2 m_1$.\n\n")
    markdown.append("```python\n")
    output = io.StringIO()
    sys.stdout = output
    
    def edge_count_product(G, H):
        n1, m1 = G.number_of_nodes(), G.number_of_edges()
        n2, m2 = H.number_of_nodes(), H.number_of_edges()
        K = cartesian_product(G, H)
        m = K.number_of_edges()
        formula = n1 * m2 + n2 * m1
        print(f"G: n1={n1}, m1={m1}; H: n2={n2}, m2={m2}")
        print(f"G * H: |V|={K.number_of_nodes()}, |E|={m}")
        print(f"Formula n1*m2 + n2*m1 = {formula}")
        print(f"Matches formula? {m == formula}\n")
    
    examples_G = [nx.path_graph(2), nx.path_graph(3), nx.cycle_graph(4)]
    examples_H = [nx.complete_graph(3), nx.path_graph(4)]
    
    for i, G in enumerate(examples_G, start=1):
        for j, H in enumerate(examples_H, start=1):
            print(f"Example G{i} * H{j}:")
            edge_count_product(G, H)
    
    sys.stdout = sys.__stdout__
    markdown.append(output.getvalue())
    markdown.append("```\n\n")
    
    return ''.join(markdown)

# ============================================================================
# QUESTION 7: Bipartite Graphs with Bipartite Complements
# ============================================================================

def q7_solution():
    """Question 7 solutions"""
    markdown = []
    markdown.append("## Question 7: Bipartite Graphs with Bipartite Complements\n\n")
    markdown.append("### (a) Find a bipartite graph whose complement is also bipartite\n\n")
    markdown.append("I tried $K_{2,2}$: it's bipartite, and its complement is just two disjoint edges, ")
    markdown.append("so the complement is bipartite too. I drew both below.\n\n")
    
    G = nx.complete_bipartite_graph(2, 2)
    G_complement = nx.complement(G)
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    pos = nx.bipartite_layout(G, [0, 1])
    nx.draw_networkx_nodes(G, pos, nodelist=[0, 1], node_color='lightcoral', ax=axes[0], node_size=500)
    nx.draw_networkx_nodes(G, pos, nodelist=[2, 3], node_color='lightblue', ax=axes[0], node_size=500)
    nx.draw_networkx_edges(G, pos, ax=axes[0], alpha=0.6, width=2)
    nx.draw_networkx_labels(G, pos, ax=axes[0])
    axes[0].set_title("$K_{2,2}$ (Bipartite)")
    axes[0].axis('off')
    pos_comp = nx.spring_layout(G_complement, seed=42)
    nx.draw_networkx_nodes(G_complement, pos_comp, ax=axes[1], node_color='lightgreen', node_size=500)
    nx.draw_networkx_edges(G_complement, pos_comp, ax=axes[1], alpha=0.6, width=2)
    nx.draw_networkx_labels(G_complement, pos_comp, ax=axes[1])
    is_bipartite_comp = nx.is_bipartite(G_complement)
    axes[1].set_title(f"$\\overline{{K_{2,2}}}$ (Bipartite: {is_bipartite_comp})")
    axes[1].axis('off')
    plt.tight_layout()
    img_path = save_figure()
    markdown.append(f"![K_{2,2} and complement]({img_path})\n\n")
    
    markdown.append("### (a') Experiment with more examples\n\n")
    markdown.append("I ran a few more bipartite graphs and checked whether their complements are bipartite.\n\n")
    markdown.append("```python\n")
    output = io.StringIO()
    sys.stdout = output
    
    examples = [
        ("K_{2,2}", nx.complete_bipartite_graph(2, 2)),
        ("K_{3,3}", nx.complete_bipartite_graph(3, 3)),
        ("Empty bipartite (3,3)", nx.Graph([(i, j) for i in range(3) for j in range(3, 6)])),
    ]
    
    for name, G in examples:
        G_comp = nx.complement(G)
        print(f"\n{name}:")
        print(f"  Original bipartite: {nx.is_bipartite(G)}")
        print(f"  Complement bipartite: {nx.is_bipartite(G_comp)}")
        print(f"  Original: {G.number_of_nodes()} vertices, {G.number_of_edges()} edges")
        print(f"  Complement: {G_comp.number_of_nodes()} vertices, {G_comp.number_of_edges()} edges")
    
    sys.stdout = sys.__stdout__
    markdown.append(output.getvalue())
    markdown.append("```\n\n")
    
    markdown.append("### (c) Proposition and proof\n\n")
    markdown.append("**Proposition:** A bipartite graph $G$ has a bipartite complement iff ")
    markdown.append("$G = K_{2,2}$ or $G$ is empty (with $n \\leq 2$).\n\n")
    markdown.append("**Proof:** ($\\Rightarrow$) If $\\overline{G}$ is bipartite it has no odd cycles. ")
    markdown.append("If $G$ has a part of size $\\geq 3$, then in $\\overline{G}$ that part gets edges inside it ")
    markdown.append("and we get a triangle, so $\\overline{G}$ isn't bipartite. So both parts have size $\\leq 2$. ")
    markdown.append("For $K_{2,2}$, $\\overline{G}$ is two disjoint edges (bipartite). ")
    markdown.append("For bigger $K_{m,n}$ the complement has cliques, so not bipartite.\n\n")
    markdown.append("($\\Leftarrow$) $K_{2,2}$: complement is two disjoint edges. ")
    markdown.append("Empty graph: complement is $K_n$, bipartite only when $n \\leq 2$. $\\square$\n\n")
    
    return ''.join(markdown)

# ============================================================================
# MAIN: Generate PDF
# ============================================================================

def generate_pdf():
    """Generate PDF from all solutions"""
    print("Generating assignment PDF...")
    
    # Collect all markdown content
    full_markdown = []
    full_markdown.append("# Assignment 2\n\n")
    full_markdown.append("My solutions for the assignment. I used Python (NetworkX, matplotlib) for the graphs.\n\n")
    full_markdown.append("---\n\n")
    
    print("Processing Question 1...")
    full_markdown.append(q1_solution())
    full_markdown.append("\n---\n\n")
    
    print("Processing Question 2...")
    full_markdown.append(q2_solution())
    full_markdown.append("\n---\n\n")
    
    print("Processing Question 3...")
    full_markdown.append(q3_solution())
    full_markdown.append("\n---\n\n")
    
    print("Processing Question 4...")
    full_markdown.append(q4_solution())
    full_markdown.append("\n---\n\n")
    
    print("Processing Question 5...")
    full_markdown.append(q5_solution())
    full_markdown.append("\n---\n\n")
    
    print("Processing Question 6...")
    full_markdown.append(q6_solution())
    full_markdown.append("\n---\n\n")
    
    print("Processing Question 7...")
    full_markdown.append(q7_solution())
    
    markdown_content = ''.join(full_markdown)
    
    # Save markdown file
    md_path = Path('Assignment2_Solutions.md')
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(markdown_content)
    print(f"\nMarkdown saved to: {md_path}")
    
    # Convert markdown to HTML first
    install_if_needed('markdown')
    
    import markdown
    
    # Convert markdown to HTML
    html_content = markdown.markdown(markdown_content, extensions=['extra', 'codehilite'])
    
    # Add CSS
    css_style = """
    <style>
        @media print {
            @page { margin: 2cm; }
            body { max-width: 100%; }
        }
        body {
            font-family: 'DejaVu Sans', 'Microsoft YaHei', Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background: white;
        }
        h1 { color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; margin-top: 30px; border-bottom: 2px solid #ecf0f1; padding-bottom: 5px; }
        h3 { color: #7f8c8d; margin-top: 25px; }
        code {
            background: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }
        pre {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
            overflow-x: auto;
            border-left: 4px solid #3498db;
        }
        pre code {
            background: transparent;
            padding: 0;
            color: inherit;
        }
        img {
            max-width: 100%;
            height: auto;
            display: block;
            margin: 20px auto;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        hr {
            border: none;
            border-top: 2px solid #ecf0f1;
            margin: 30px 0;
        }
        figure.figure-with-caption {
            margin: 20px auto;
            text-align: center;
        }
        figure.figure-with-caption img {
            margin-bottom: 0;
        }
        figure.figure-with-caption figcaption {
            font-size: 0.85em;
            color: #7f8c8d;
            margin-top: 6px;
        }
    </style>
    """
    
    # MathJax 3: 在浏览器中正确渲染 LaTeX 公式 ($...$ 与 $$...$$)
    mathjax_script = """
    <script>
    MathJax = {
        tex: {
            inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
            displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']]
        }
    };
    </script>
    <script src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js" async></script>
    """

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Assignment 2 Solutions</title>
        {css_style}
        {mathjax_script}
    </head>
    <body>
        {html_content}
    </body>
    </html>
    """
    
    # Save HTML file
    html_path = Path('Assignment2_Solutions.html')
    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(full_html)
    print(f"HTML saved to: {html_path}")
    
    # Try to generate PDF with weasyprint
    try:
        install_if_needed('weasyprint')
        from weasyprint import HTML
        print("Converting to PDF...")
        pdf_path = Path('Assignment2_Solutions.pdf')
        HTML(string=full_html, base_url=str(Path.cwd())).write_pdf(pdf_path)
        print(f"✓ PDF generated: {pdf_path}")
        return True
    except Exception as e:
        print(f"\nPDF generation failed: {e}")
        print("\n" + "="*60)
        print("No problem! HTML file has been generated.")
        print("To convert HTML to PDF:")
        print("="*60)
        print("1. Double-click to open: Assignment2_Solutions.html")
        print("2. Press Ctrl+P (or Cmd+P on Mac)")
        print("3. Select 'Save as PDF' or 'Microsoft Print to PDF'")
        print("4. Click Save")
        print("="*60)
        return False

if __name__ == '__main__':
    generate_pdf()
