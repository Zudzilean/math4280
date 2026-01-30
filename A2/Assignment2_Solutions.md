# Assignment 2

My solutions for the assignment. I used Python (NetworkX, matplotlib) for the graphs.

---

# Question 1: Triangle-Free Graphs

The bound is $m \leq \lfloor n^2/4 \rfloor$.

### (a) Examples for $n = 2, 3, 4, 5, 6$

I used complete bipartite graphs $K_{\lfloor n/2 \rfloor, \lceil n/2 \rceil}$ so the number of edges hits the bound. Below I draw them for each $n$.

**Common property I noticed:** They are all complete bipartite with the two parts as equal as possible.

![n=2](assignment_images\fig_1.png)

![n=3](assignment_images\fig_2.png)

![n=4](assignment_images\fig_3.png)

![n=5](assignment_images\fig_4.png)

![n=6](assignment_images\fig_5.png)

### (b) General construction

For any $n$ I take $G = K_{\lfloor n/2 \rfloor, \lceil n/2 \rceil}$. It's bipartite so no triangles, and the edge count is $\lfloor n/2 \rfloor \cdot \lceil n/2 \rceil = \lfloor n^2/4 \rfloor$, so it reaches the bound.


---

## Question 2: Bi-graphical Sequences

### (a) $S_1 = \langle 6, 5, 5, 5, 3, 2, 1, 1 \rangle$, $S_2 = \langle 5, 5, 4, 3, 2 \rangle$

Here $a_1 = 6$ but $|S_2| = 5$, so we need $a_1 \le s$ and it fails. So **I get: not bi-graphical.**

```python
Part (a):
  sum(S1) = 28, sum(S2) = 19
  Sum mismatch: sum(S1)=28, sum(S2)=19
  Bi-graphical? False
  So my answer for (a) is: No, not bi-graphical.
```

### (b) $S_1 = \langle 8, 6, 4, 4, 4, 4, 4 \rangle$, $S_2 = \langle 6, 5, 4, 4, 4, 4, 3, 3, 1 \rangle$

I applied the reduction step by step (code below) and it worked all the way. So **this pair is bi-graphical.** I also draw a bipartite graph realizing it.

```python
Part (b):
  sum(S1) = 34, sum(S2) = 34
  Reduce: S1'=[6, 4, 4, 4, 4, 4], S2'=[5, 4, 3, 3, 3, 3, 2, 2, 1]
  Reduce: S1'=[4, 4, 4, 4, 4], S2'=[4, 3, 2, 2, 2, 2, 2, 2, 1]
  Reduce: S1'=[4, 4, 4, 4], S2'=[3, 2, 2, 2, 2, 2, 1, 1, 1]
  Reduce: S1'=[4, 4, 4], S2'=[2, 2, 2, 1, 1, 1, 1, 1, 1]
  Reduce: S1'=[4, 4], S2'=[1, 1, 1, 1, 1, 1, 1, 1, 0]
  Reduce: S1'=[4], S2'=[1, 1, 1, 1, 0, 0, 0, 0, 0]
  Bi-graphical? True
```

![Bipartite graph](assignment_images\fig_6.png)


---

## Question 3: Connectivity

### (a) Graphs on 7 vertices with $\deg(v) \geq 3$

I tried to draw two different graphs that are disconnected, but any component has to have at least 4 vertices (since each vertex has degree $\geq 3$), so $4+4=8 > 7$ and it's impossible. So **I couldn't get a disconnected example**—they all end up connected. Below are two connected examples.

![Graphs on 7 vertices](assignment_images\fig_7.png)

### (b) Graphs on 8 vertices with $\deg(v) \geq 4$

Same idea: I tried to get a disconnected one but each part would need at least 5 vertices, so $5+5=10 > 8$. So **again they're all connected.** Two examples below.

![Graphs on 8 vertices](assignment_images\fig_8.png)

### (c) Proof

**Theorem:** If every vertex has $\deg(v) \geq \frac{n-1}{2}$, then $G$ is connected.

**Proof:** Suppose $G$ is disconnected and $u$, $v$ are in different components. The component of $u$ has at least $\deg(u)+1 \geq \frac{n+1}{2}$ vertices, and same for $v$. So total $\geq \frac{n+1}{2}+\frac{n+1}{2}=n+1 > n$, contradiction. So $G$ must be connected. $\square$


---

## Question 4: Graph Isomorphism

I compared the two graphs: both have 7 vertices, 6 edges, same degree sequence $\langle 3, 3, 2, 1, 1, 1, 1 \rangle$, and both are trees. So **I think they are isomorphic** (and the code confirms it).

<figure class="figure-with-caption"><img src="assignment_images/fig_9.png" alt="Figure 2" /><figcaption>Figure 2</figcaption></figure>

Left graph has degree sequence $\langle 4, 4, 4, 4, 4, 4, 4, 4, 2, 2, 2, 2 \rangle$, right has $\langle 5, 5, 5, 5, 3, 3, 3, 3, 2, 2, 2, 2 \rangle$. They're different, so **I conclude they are not isomorphic.**


---

## Question 5: Complement of Paths

### (a) Complements of $P_n$ for $n = 2, 3, 4, 5, 6$

I drew each path and its complement and checked whether the complement is connected.

**n = 2:**

![P_2](assignment_images\fig_10.png)

**n = 3:**

![P_3](assignment_images\fig_11.png)

**n = 4:**

![P_4](assignment_images\fig_12.png)

**n = 5:**

![P_5](assignment_images\fig_13.png)

**n = 6:**

![P_6](assignment_images\fig_14.png)

**What I observed:** $\overline{P_2}$ and $\overline{P_3}$ are not connected; for $n \geq 4$ the complement is connected. So the pattern seems to be: $\overline{P_n}$ is connected iff $n \geq 4$.

### (b) Conjecture and proof

**Conjecture:** $\overline{P_n}$ is connected if and only if $n \geq 4$.

**Proof:** For $n \geq 4$, in $\overline{P_n}$ any two vertices are either adjacent or share a neighbor, so the graph has diameter $\leq 2$ and is connected. For $n=2,3$ we already saw the complement is disconnected. So the conjecture holds. $\square$

### (c) Generalization to trees

I don't think the same statement holds for all trees—e.g. a star has a very different complement, so connectivity of the complement can behave differently.


---

## Question 6: Graph Multiplication (Cartesian Product)

I used the definition: vertices of $G * H$ are pairs $(u,a)$; edges $((u,a),(v,b))$ when $u=v$ and $ab \in E(H)$, or $a=b$ and $uv \in E(G)$.

### (a) Draw $P_2 * K_3$ and $P_3 * K_3$

I implemented the product and drew these two graphs below.

**P2 * K3:**

![P2*K3](assignment_images\fig_15.png)

**P3 * K3:**

![P3*K3](assignment_images\fig_16.png)

### (b) Edge-count formula $m = n_1 m_2 + n_2 m_1$

I tried several pairs $(G,H)$ and checked that the number of edges in $G * H$ always matches $n_1 m_2 + n_2 m_1$.

```python
Example G1 * H1:
G: n1=2, m1=1; H: n2=3, m2=3
G * H: |V|=6, |E|=9
Formula n1*m2 + n2*m1 = 9
Matches formula? True

Example G1 * H2:
G: n1=2, m1=1; H: n2=4, m2=3
G * H: |V|=8, |E|=10
Formula n1*m2 + n2*m1 = 10
Matches formula? True

Example G2 * H1:
G: n1=3, m1=2; H: n2=3, m2=3
G * H: |V|=9, |E|=15
Formula n1*m2 + n2*m1 = 15
Matches formula? True

Example G2 * H2:
G: n1=3, m1=2; H: n2=4, m2=3
G * H: |V|=12, |E|=17
Formula n1*m2 + n2*m1 = 17
Matches formula? True

Example G3 * H1:
G: n1=4, m1=4; H: n2=3, m2=3
G * H: |V|=12, |E|=24
Formula n1*m2 + n2*m1 = 24
Matches formula? True

Example G3 * H2:
G: n1=4, m1=4; H: n2=4, m2=3
G * H: |V|=16, |E|=28
Formula n1*m2 + n2*m1 = 28
Matches formula? True

```


---

## Question 7: Bipartite Graphs with Bipartite Complements

### (a) Find a bipartite graph whose complement is also bipartite

I tried $K_{2,2}$: it's bipartite, and its complement is just two disjoint edges, so the complement is bipartite too. I drew both below.

![K_(2, 2) and complement](assignment_images\fig_17.png)

### (a') Experiment with more examples

I ran a few more bipartite graphs and checked whether their complements are bipartite.

```python

K_{2,2}:
  Original bipartite: True
  Complement bipartite: True
  Original: 4 vertices, 4 edges
  Complement: 4 vertices, 2 edges

K_{3,3}:
  Original bipartite: True
  Complement bipartite: False
  Original: 6 vertices, 9 edges
  Complement: 6 vertices, 6 edges

Empty bipartite (3,3):
  Original bipartite: True
  Complement bipartite: False
  Original: 6 vertices, 9 edges
  Complement: 6 vertices, 6 edges
```

### (c) Proposition and proof

**Proposition:** A bipartite graph $G$ has a bipartite complement iff $G = K_{2,2}$ or $G$ is empty (with $n \leq 2$).

**Proof:** ($\Rightarrow$) If $\overline{G}$ is bipartite it has no odd cycles. If $G$ has a part of size $\geq 3$, then in $\overline{G}$ that part gets edges inside it and we get a triangle, so $\overline{G}$ isn't bipartite. So both parts have size $\leq 2$. For $K_{2,2}$, $\overline{G}$ is two disjoint edges (bipartite). For bigger $K_{m,n}$ the complement has cliques, so not bipartite.

($\Leftarrow$) $K_{2,2}$: complement is two disjoint edges. Empty graph: complement is $K_n$, bipartite only when $n \leq 2$. $\square$

