from pyvisjs import Options

def test_options_init_default():
    # init
    DEFAULT_DICT = {}

    # mock

    # call
    options = Options()
    
    # assert
    assert options
    assert options.to_dict() == DEFAULT_DICT 

def test_options_physics_set_barnesHut():
    # init
    EXPECTED_DICT = {
        'physics': {
            'barnesHut': {
                'gravitationalConstant': -2750, 
                'centralGravity': 0.3, 
                'springLength': 250, 
                'springConstant': 0, 
                'damping': 1
            }
        }
    }

    # mock

    # call
    options = Options()

    options.physics.set_barnesHut(
        gravitationalConstant=-2750,
        centralGravity=0.3,
        springConstant=0,
        springLength=250,
        damping=1
    )
    
    # assert
    assert options
    assert options.to_dict() == EXPECTED_DICT 

def test_options_simple_use_case():
    # init
    SCALING_MIN = 10
    SCALING_MAX = 30
    COLOR = "LIME"
    SMOOTH = False
    GR_CONSTANT = -30000
    ST_ITERATIONS = 2500
    OPTIONS_DICT = {
        'edges': {
            'color': {
                'color': COLOR
            }, 
            'smooth': {
                'enabled': SMOOTH
            }
        }, 
        'nodes': {
            'scaling': {
                'min': SCALING_MIN, 
                'max': SCALING_MAX
            }
        }, 
        'physics': {
            'barnesHut': {
                'gravitationalConstant': GR_CONSTANT
            }, 
            'stabilization': {
                'iterations': ST_ITERATIONS
            }
        }
    }

    # mock

    # call
    options = Options()
    options.nodes.set_scaling(min = SCALING_MIN, max = SCALING_MAX)
    options.edges.set_color(color = COLOR)
    options.edges.set_smooth(enabled = SMOOTH)
    options.physics.set_barnesHut(gravitationalConstant=GR_CONSTANT)
    options.physics.set_stabilization(iterations=ST_ITERATIONS)
    
    # assert
    assert options.to_dict() == OPTIONS_DICT

def test_options_bluor_use_case():
    # init
    OPTIONS_DICT = {
        "configure": {
            "enabled": False
        },
        "edges": {
            "color": {
                "inherit": True
            },
            "smooth": {
                "enabled": True,
                "type": "dynamic"
            }
        },
        "interaction": {
            "dragNodes": True,
            "hideEdgesOnDrag": False,
            "hideNodesOnDrag": False
        },
        "physics": {
            "barnesHut": {
                "avoidOverlap": 0,
                "centralGravity": 0.3,
                "damping": 1, #is_gummy=0.09
                "gravitationalConstant": -2750,
                "springConstant": 0, #is_gummy=0.05
                "springLength": 250
            },
            "enabled": True,
            "stabilization": {
                "enabled": True,
                "fit": True,
                "iterations": 1000,
                "onlyDynamicEdges": False,
                "updateInterval": 50
            }
        }
    }

    # mock

    # call
    options = Options()
    options \
        .set_configure(enabled=False) \
        .set_interaction(dragNodes=True, hideEdgesOnDrag=False, hideNodesOnDrag=False)
    options.edges \
        .set_color(inherit=True) \
        .set_smooth(type="dynamic", enabled=True)
    options.physics \
        .set(enabled=True) \
        .set_barnesHut(avoidOverlap=0, centralGravity=0.3, damping=1, gravitationalConstant=-2750, springConstant=0, springLength=250) \
        .set_stabilization(enabled=True, fit=True, iterations=1000, onlyDynamicEdges=False, updateInterval=50)
    
    # assert
    assert options.to_dict() == OPTIONS_DICT