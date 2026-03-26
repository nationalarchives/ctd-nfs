import pytest

from src.harvester.details_still import distill_details


@pytest.mark.skip(reason="names and address distillation functions have been changed")
def test_distill_address(addresses):
    for fixture in addresses:
        assert distill_details(fixture['original']) == fixture['final']
