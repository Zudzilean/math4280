"""
绘制二分图：左边 S1 共 7 个点（度数 8,6,4,4,4,4,4），右边 S2 共 9 个点（度数 6,5,4,4,4,4,3,3,1）
"""
import matplotlib
matplotlib.use('Agg')  # 不弹窗，只保存图片
import networkx as nx
import matplotlib.pyplot as plt
# 支持中文显示（Windows 常用字体）
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 度数序列
# S1: 左边 7 个点
degrees_S1 = [8, 6, 4, 4, 4, 4, 4]
# S2: 右边 9 个点
degrees_S2 = [6, 5, 4, 4, 4, 4, 3, 3, 1]

# 用二分图配置模型生成满足度数序列的图（保留多重边以保证度数精确）
G = nx.bipartite.configuration_model(degrees_S1, degrees_S2)
# 确定左右节点：前 7 个为 S1，后 9 个为 S2
S1_nodes = list(range(7))
S2_nodes = list(range(7, 7 + 9))

# 二分图布局：S1 在左，S2 在右
pos = nx.bipartite_layout(G, S1_nodes, align='vertical')
# 微调：让 S1 在左边，S2 在右边（bipartite_layout 默认左 0 右 1）
for node in S1_nodes:
    pos[node] = (0, pos[node][1])
for node in S2_nodes:
    pos[node] = (1, pos[node][1])

# 绘图
plt.figure(figsize=(10, 8))
nx.draw_networkx_nodes(G, pos, nodelist=S1_nodes, node_color='lightcoral', 
                       node_size=500, label='S1')
nx.draw_networkx_nodes(G, pos, nodelist=S2_nodes, node_color='lightblue', 
                       node_size=500, label='S2')
nx.draw_networkx_edges(G, pos, alpha=0.5)

# 节点标签：S1 用 a,b,..., S2 用 1,2,... 或直接标度数
labels = {}
for i in S1_nodes:
    labels[i] = f'S1-{i}\n(度{degrees_S1[i]})'
for i in S2_nodes:
    j = i - 7
    labels[i] = f'S2-{j}\n(度{degrees_S2[j]})'
nx.draw_networkx_labels(G, pos, labels, font_size=8)

plt.legend(scatterpoints=1)
plt.axis('off')
plt.title('二分图：S1（左，7 点）与 S2（右，9 点）')
plt.tight_layout()
plt.savefig('bipartite_graph.png', dpi=150, bbox_inches='tight')
print('图已保存为 bipartite_graph.png')
# plt.show()  # 若在交互环境需要显示可取消注释
print('S1 度数:', degrees_S1, '→ 实际度数:', [G.degree(i) for i in S1_nodes])
print('S2 度数:', degrees_S2, '→ 实际度数:', [G.degree(i) for i in S2_nodes])
