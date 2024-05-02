from pyvisjs.base_dictable import BaseDictable

def test_basedictable_init_default():
    # init
    class D(BaseDictable):
        def __init__(self):
            super().__init__()

    # mock

    # call
    d = D()
    
    # assert
    assert d.to_dict() == {}

def test_basedictable_instance_attr():
    # init
    class D(BaseDictable):
        def __init__(self):
            super().__init__()

    NAME = "AM"
    # mock

    # call
    d = D()
    d.name = NAME
    
    # assert
    assert d.to_dict() == {"name": NAME}

def test_basedictable_attr_filter_func():
    # init
    class ME(BaseDictable):
        def __init__(self, name, age):
            only_show_name_and_age = lambda attr: attr in ["name", "age"]
            super().__init__(attr_filter_func=only_show_name_and_age)

            self.name = name
            self.age = age
            self.country = "LV"
            self.city = "Jurmala"

    NAME = "AM"
    AGE = 44
    ME_DICT = {
        "name": NAME,
        "age": AGE,
    }

    # mock

    # call
    me = ME(NAME, AGE)
    
    # assert
    assert me.to_dict() == ME_DICT

def test_basedictable_attr_map_func():
    # init
    class ME(BaseDictable):
        def __init__(self, name, age, country, city):
            mapping = {
                "name": "firstname",
                "age": "age_years"
            }
            change_name_and_age = lambda attr: mapping.get(attr, attr)
            super().__init__(attr_map_func=change_name_and_age)

            self.name = name
            self.age = age
            self.country = country
            self.city = city

    NAME = "AM"
    AGE = 44
    COUNTRY = "LV"
    CITY = "Jurmala"
    ME_DICT = {
        "firstname": NAME,
        "age_years": AGE,
        "country": COUNTRY,
        "city": CITY
    }

    # mock

    # call
    me = ME(NAME, AGE, COUNTRY, CITY)
    
    # assert
    assert me.to_dict() == ME_DICT