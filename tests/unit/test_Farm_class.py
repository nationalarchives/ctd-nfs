from src.containers import Farm


def test_farm_dataclass_instantiation(farms):
    for farm in farms:
        new_farm = Farm(farm)        
        assert isinstance(new_farm, Farm)

