from pyvisjs import Edge

def test_edge_init_default():
    # init
    START_ID = 1
    END_ID = 2

    # mock

    # call
    e = Edge(START_ID, END_ID)
    
    # assert
    assert e.start == START_ID
    assert e.end == END_ID

def test_edge_init_kwargs():
    # init
    START_ID = 1
    END_ID = 2
    NODE_CATEGORY = "category1"
    NODE_AMOUNT = 1009.4
    NODE_HASVALUE = False

    # mock

    # call
    e = Edge(START_ID, END_ID, category=NODE_CATEGORY, amount=NODE_AMOUNT, has_value=NODE_HASVALUE)
    
    # assert
    assert e.start == START_ID
    assert e.end == END_ID
    assert (e.category, e.amount, e.has_value) == (NODE_CATEGORY, NODE_AMOUNT, NODE_HASVALUE)


def test_edge_to_dict():
    # init
    START_ID = 1
    END_ID = 2
    EDGE_DICT = {
            "from": START_ID,
            "to": END_ID,
        }

    # mock

    # call
    e = Edge(START_ID, END_ID)
    
    # assert
    assert e.to_dict() == EDGE_DICT
