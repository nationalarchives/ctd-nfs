from src.containers import Farm


def test_farm_dataclass_instantiation(farms):
    for farm_fixture in farms:
        new_farm = Farm(farm_fixture)        
        assert isinstance(new_farm, Farm)

