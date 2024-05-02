from .base_dictable import BaseDictable
from typing import Dict, Self

# Options
# ├─── set_configure
# ├─── set_interaction
# ├── Nodes
# │   └── set_scaling
# ├── Edges
# │   ├── set_color
# │   └── set_smooth
# ├── Physics
# │   ├── set_barnesHutKV
# │   ├── set_barnesHut
# │   └── set_stabilization
# └── 


class Options(BaseDictable):
    """
    Parameters
    ----------
    height : str, default='100%'
        the height of the canvas. Can be in percentages or pixels (ie. `'400px'`).

    width : str, default='100%'
        the width of the canvas. Can be in percentages or pixels (ie. `'400px'`).
    """

    def __init__(self, height:str=None, width:str=None):
        super().__init__()
        if height: self.height = height
        if width: self.width = width

        self.configure = {}
        self.interaction = {}

        self.nodes = Options.Nodes()
        self.edges = Options.Edges()
        self.physics = Options.Physics()

    def set_configure(self, enabled:bool=None) -> Self:
        """
        Handles the HTML part of the canvas.

        Parameters
        ----------
        enabled : bool, default=true
            Toggle the configuration interface on or off. This is an optional parameter. If left undefined and any of the other properties of this object are defined, this will be set to true.
            So you can switch it on if you just want to use defaults for all other options
        """
        self._update_dict_with_locals(self.configure, locals())
        return self

    def set_interaction(self, dragNodes:bool=None, dragView:bool=None, hideEdgesOnDrag:bool=None, hideEdgesOnZoom:bool=None, hideNodesOnDrag:bool=None) -> Self:
        """
        Used for all user interaction with the network. Handles mouse and touch events as well as the navigation buttons and the popups.
       
        Parameters
        ----------
        dragNodes : bool, default=True
            When true, the nodes that are not fixed can be dragged by the user.

        dragView : bool, default=True
            When true, the view can be dragged around by the user.
        
        hideEdgesOnDrag : bool, default=False
            When true, the edges are not drawn when dragging the view. This can greatly speed up responsiveness on dragging, improving user experience.

        hideEdgesOnZoom : bool, default=False
            When true, the edges are not drawn when zooming the view. This can greatly speed up responsiveness on zooming, improving user experience.

        hideNodesOnDrag : bool, default=False
            When true, the nodes are not drawn when dragging the view. This can greatly speed up responsiveness on dragging, improving user experience.
            
        """
        self._update_dict_with_locals(self.interaction, locals())
        return self

    class Nodes(BaseDictable):
        def __init__(self):
            super().__init__()
            self.scaling = {}

        def set_scaling(self, min:int=None, max:int=None, label:bool=None) -> Self:
            """
            Parameters
            ----------
            min : int, default=10
                If nodes have a value, their sizes are determined by the value, the scaling function and the min max values. The min value is the minimum allowed value.
            
            max : int, default=30
                This is the maximum allowed size when the nodes are scaled using the value option.

            label : bool, default true
                This can be false if the label is not allowed to scale with the node. If true it will scale using default settings
            """
            self._update_dict_with_locals(self.scaling, locals())
            return self
        
    class Edges(BaseDictable):
        def __init__(self):
            super().__init__()
            self.color = {}
            self.smooth = {}
        
        def set_color(self, color:str=None, highlight:str=None, hover:str=None, inherit:str=None, opacity:float=None, dashes:bool=None) -> Self:
            """
            Parameters
            ----------
            color : str, default='#848484'
                The color of the edge when it is not selected or hovered over (assuming hover is enabled in the interaction module).

            highlight : str, default='#848484'
                The color the edge when it is selected.

            hover : str, default='#848484'
                The color the edge when the mouse hovers over it (assuming hover is enabled in the interaction module).

            inherit : str, default='from'
                When color, highlight or hover are defined, inherit is set to false!

                Supported options are: `'from','to','both'`.
                The default value is 'from' which does the same as true: the edge will inherit the color from the border of the node on the 'from' side.

                When set to 'to', the border color from the 'to' node will be used.

                When set to 'both', the color will fade from the from color to the to color. `'both' is computationally intensive` because the gradient is recomputed every redraw. This is required because the angles change when the nodes move.
            
            opacity : float, default=1.0
                It can be useful to set the opacity of an edge without manually changing all the colors. The opacity option will convert all colors (also when using inherit) to adhere to the supplied opacity. The allowed range of the opacity option is between 0 and 1. This is only done once so the performance impact is not too big.
            
            dashes : bool, default=False
                When true, the edge will be drawn as a dashed line. When using dashed lines in IE versions older than 11, the line will be drawn straight, not smooth.
            """
            self._update_dict_with_locals(self.color, locals())
            return self

        def set_smooth(self, enabled:bool=None, type:str=None, roundness:float=None) -> Self:
            """
            Parameters
            ----------
            enabled : bool, default
                Toggle smooth curves on and off. This is an optional option. If any of the other properties in this object are set, this option will be set to true.
                So you can switch it on if you just want to use defaults for all other options

            type : str, default='dynamic'
                Possible options: `'dynamic', 'continuous', 'discrete', 'diagonalCross', 'straightCross', 'horizontal', 'vertical', 'curvedCW', 'curvedCCW', 'cubicBezier'`.            
            
            roundness : float, default=0.5
                Accepted range: `0 .. 1.0`. This parameter tweaks the roundness of the smooth curves for all types EXCEPT dynamic.
            """
            self._update_dict_with_locals(self.smooth, locals())
            return self

    class Physics(BaseDictable):
        """
        Handles the physics simulation, moving the nodes and edges to show them clearly.
        """
        def __init__(self):
            super().__init__()

            self.enabled:bool = None
            self.minVelocity:float = None
            self.maxVelocity:float = None

            self.barnesHut = {}
            self.stabilization = {}

        def set(self, enabled:bool=None, minVelocity:float=None, maxVelocity:float=None) -> Self:
            """
            Parameters
            ----------
            enabled : bool, default=True
                Toggle the physics system on or off. This property is optional. If you define any of the options below and enabled is undefined, this will be set to true.
                So you can switch it on if you just want to use defaults for all other options
            
            minVelocity : float, default=0.1
                Once the minimum velocity is reached for all nodes, we assume the network has been stabilized and the simulation stops.

            maxVelocity : float, default=50.0
                The physics module limits the maximum velocity of the nodes to increase the time to stabilization. This is the maximum value.

            """
            if enabled: self.enabled = enabled
            if minVelocity: self.minVelocity = minVelocity
            if maxVelocity: self.maxVelocity = maxVelocity

            return self

        def set_barnesHutKV(self, key:str, value):
            """
            You can use set_barnesHut function instead, if you dont know parameters names
            """
            self.barnesHut.update({ key: value })

        def set_barnesHut(self, theta:float=None, gravitationalConstant:int=None, centralGravity:float=None, springLength:int=None, springConstant:float=None, damping:float=None, avoidOverlap:float=None) -> Self:
            """
            Parameters
            ----------
            theta : float, default=0.5
                This parameter determines the boundary between consolidated long range forces and individual short range forces. To oversimplify higher values are faster but generate more errors, lower values are slower but with less errors.
            
            gravitationalConstant : int, default=-2000
                Gravity attracts. We like repulsion. So the value is negative. If you want the repulsion to be stronger, decrease the value (so -10000, -50000).
            
            centralGravity : float, default=0.3
                There is a central gravity attractor to pull the entire network back to the center.
            
            springLength : int, default=95
                The edges are modelled as springs. This springLength here is the rest length of the spring.
            
            springConstant : float, default=0.04
                This is how 'sturdy' the springs are. Higher values mean stronger springs.
            
            damping : float, default=0.09
                Accepted range: [0 .. 1]. The damping factor is how much of the velocity from the previous physics simulation iteration carries over to the next iteration.
            
            avoidOverlap : float, default=0
                Accepted range: [0 .. 1]. When larger than 0, the size of the node is taken into account. The distance will be calculated from the radius of the encompassing circle of the node for both the gravity model. Value 1 is maximum overlap avoidance.
            """

            self._update_dict_with_locals(self.barnesHut, locals())
            return self

        def set_stabilization(self, enabled:bool=None, iterations:int=None, updateInterval:int=None, onlyDynamicEdges:bool=None, fit:bool=None) -> Self:
            """
            Parameters
            ----------
            enabled : bool, default=True
                Toggle the stabilization. This is an optional property. If undefined, it is automatically set to true when any of the properties of this object are defined.
                So you can switch it on if you just want to use defaults for all other options

            iterations : int, default=1000
                The physics module tries to stabilize the network on load up til a maximum number of iterations defined here. If the network stabilized with less, you are finished before the maximum number.
            
            updateInterval : int, default=50
                When stabilizing, the DOM can freeze. You can chop the stabilization up into pieces to show a loading bar for instance. The interval determines after how many iterations the `stabilizationProgress` event is triggered.
            
            onlyDynamicEdges : bool, default=False
                If you have predefined the position of all nodes and only want to stabilize the dynamic smooth edges, set this to true. It freezes all nodes except the invisible dynamic smooth curve support nodes. If you want the visible nodes to move and stabilize, do not use this.
            
            fit : bool, default=True
                Toggle whether or not you want the view to zoom to fit all nodes when the stabilization is finished.

            """
            self._update_dict_with_locals(self.stabilization, locals())
            return self

    


    