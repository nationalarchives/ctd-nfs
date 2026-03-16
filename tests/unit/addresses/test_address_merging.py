from src.harvester.details_still import distill_details


def test_distill_address(addresses):
    for fixture in addresses:
        assert distill_details(fixture['original']) == fixture['final']
