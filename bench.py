import yaml
import networkx as nx
import matplotlib as plt

def build_dag_from_definition(filename):
  with open(filename, 'r') as file:
    data = yaml.safe_load(file)

  g = nx.DiGraph()
  for step in data['steps'].keys():
    g.add_node(step)

  for step, definition in data['steps'].items():
    if definition.get('after', None):
       for dep in definition['after']:
           g.add_edge(dep, step)
  return g

def plot_graph(g):
  layout = nx.spring_layout(g, k=0.2,iterations=50)
  nx.draw_networkx_edges(g, layout, edge_color='#AAAAAA')
  nx.draw_networkx_nodes(g, layout, nodelist=g.nodes(), node_size=100, node_color='#fc8d62')
  nodes = [node for node in g.nodes]
  for l in layout:
      layout[l][1] -= 0.03
  nx.draw_networkx_labels(g, layout, labels=dict(zip(nodes, nodes)), font_size=10)

