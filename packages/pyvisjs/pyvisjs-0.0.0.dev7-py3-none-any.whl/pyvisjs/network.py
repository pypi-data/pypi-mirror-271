from .base_dictable import BaseDictable
from .utils import open_file, save_file
from .node import Node
from .edge import Edge
from .options import Options
from jinja2 import Environment, PackageLoader, select_autoescape
from typing import List

class Network(BaseDictable):
    """
    Network is a visualization to display networks and networks consisting of nodes and edges. 
    The visualization is easy to use and supports custom shapes, styles, colors, sizes, images, and more. 
    The network visualization works smooth on any modern browser for up to a few thousand nodes and edges. 
    Network uses HTML canvas for rendering.
    """
    def __init__(self, name="Network", nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        only_use_data_attr = lambda attr: attr == "_data"
        super().__init__(attr_filter_func=only_use_data_attr)
        self.name = name
        self._initialize_data(nodes, edges, options)
        self.env = Environment(
            loader=PackageLoader("pyvisjs"),
            autoescape=select_autoescape()
        )

    @property
    def options(self) -> Options:
        opt = self._data["options"]   
        return opt if isinstance(opt, Options) else None
    
    @options.setter
    def options(self, val:Options):
        self._data["options"] = val
    
    @property
    def nodes(self) -> List[Node]: 
        return self._data["nodes"]  
    
    @property
    def edges(self) -> List[Edge]: 
        return self._data["edges"]  

    def _initialize_data(self, nodes:List[Node]=None, edges:List[Edge]=None, options:Options=None):
        default_data = {"nodes": [], "edges": [], "options": {}}

        if nodes:
            default_data.update({
                "nodes": nodes,
            })

        if edges:
            default_data.update({
                "edges": edges,
            })

        if options:
            default_data.update({
                "options": options,
            })

        self._data = default_data

    def __repr__(self):
        return f"Network(\'{self.name}\')"
    
    def add_node(self, node_id, label=None, color=None, shape="dot", size=None, cid=None, **kwargs):
        """
        Creates a Node with node_id and adds it to the nodes list. 
        Wont add node if the nodes list alredy contains a node with the same node_id.

        Parameters
        ----------
        node_id : int or str, default undefined
            The id of the node. The id is mandatory for nodes and they have to be unique. Will be used as a node reference in edges

        label : str, default undefined
            Will be replaced with node_id if undefined) The label is the piece of text shown in or under the node, depending on the shape.
        
        color : str, default undefined
            Could be value like '#ffffff' or 'red'
        
        **kwargs : dict, optional
            Any key=value agruments could also be specified to push them into the underlying HTML template
        """
        if not [node.id for node in self.nodes if node.id == node_id]:
            self.nodes.append(Node(node_id, label, color, shape, size, cid, **kwargs))

    def add_edge(self, from_id, to_id, **kwargs):
        """Creates an Edge which connects two nodes using from_id and to_id and adds it to the edges list.
        If you provide node ID which is not presented in the nodes list such a node will be automatically created and added to the nodes list.
        
        Parameters
        ----------
        from_id : int or str, default undefined
            Edges are between two nodes, one to and one from. This is where you define the from node. You have to supply the corresponding node ID.
        
        to_id -- int or str, default undefined
            Edges are between two nodes, one to and one from. This is where you define the to node. You have to supply the corresponding node ID.

        **kwargs : dist, Optional
            Any key=value agruments could also be specified to push them into the underlying HTML template
        """
        self.add_node(from_id)
        self.add_node(to_id)

        if not [edge.start for edge in self.edges if edge.start == from_id and edge.end == to_id]:
            self.edges.append(Edge(from_id, to_id, **kwargs))

    def to_dict(self):
        return super().to_dict()["_data"]

    def show(self, file_name):
        self.render_template(open_in_browser=True, output_filename=file_name)

    def render_template(self, open_in_browser=False, save_to_output=False, output_filename="default.html", template_filename="basic.html") -> str:
        network_dict = self.to_dict()
        
        html_output = self.env \
            .get_template(template_filename) \
            .render(
                width=network_dict["options"].get("width", "100%"),
                height=network_dict["options"].get("height", "100%"),
                data=network_dict
            )

        if save_to_output or open_in_browser:
            file_path = save_file(output_filename, html_output)

        if open_in_browser:
            open_file(file_path)

        return html_output
        
