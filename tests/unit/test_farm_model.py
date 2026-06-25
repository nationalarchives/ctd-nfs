import pytest

from src._dataclasses.farm_model import Farm

def test_farm_dataclass_instantiation(capsys, farms):
	"""_summary_
	Args:
		capsys (_type_): _description_
		farms (_type_): _description_

	capsys disabled from pytest docs https://docs.pytest.org/en/stable/how-to/capture-stdout-stderr.html#
	To temporarily disable capture within a test, 
	the capture fixtures have a disabled() method that can be used as a context manager, disabling capture inside the with block
	"""	
	for farm_fixture in farms:
		new_farm = Farm(**farm_fixture)
		with capsys.disabled():
			print(f"{new_farm.catalogue_reference}")
			print(new_farm.forms)
		assert isinstance(new_farm, Farm)





