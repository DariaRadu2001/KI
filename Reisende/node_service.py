class NodeService:
    def __init__(self):
        self.nodes = set()
        self.nodes_heuristik = {}

    def add_node(self, node):
        self.nodes.add(node)

    def add_node_heuristik(self, x_coord, y_coord, distance):
        self.nodes_heuristik[(x_coord, y_coord)] = distance

    def search_node(self, x_coord, y_coord):
        for node in self.nodes:
            if node.get_x_coord() == x_coord and node.get_y_coord() == y_coord:
                return node

    def get_nodes(self):
        return self.nodes