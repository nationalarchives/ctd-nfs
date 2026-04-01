from collections import namedtuple
import pytest

from src.harvester.details_still import distill_details


Form = namedtuple('Form', ['type', 'title', 'name', 'address'])

@pytest.mark.skip(reason="names and address distillation functions have been changed")
def test_same_details_across_all_forms() -> None:
    Forms = [
        Form('C51/SSY', "[not specified]", "Katharine Duncombe", "The Old Hall, Ashwell, Oakham, Rutland"),
        Form('C 47/SSY', "Miss", "H Duncombe", "Old Hall, Ashwell, Oakham, Rutland"),
        Form('SF', "Miss", "K Duncombe", "Old Hall, Ashwell, Oakham, Rutland")
    ]

    assert distill_details(Forms) == \
        "Miss H Duncombe, Old Hall, Ashwell, Oakham, Rutland | " \
        "Katharine Duncombe, The Old Hall, Ashwell, Oakham, Rutland | " \
        "Miss K Duncombe, Old Hall, Ashwell, Oakham, Rutland"



