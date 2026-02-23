from src.combiner import distill_addresses


def test_distill_address(addresses):
    for fixture in addresses:
        assert distill_addresses(fixture['original']) == fixture['final']
