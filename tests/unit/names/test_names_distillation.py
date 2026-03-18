from src.harvester.distillation.distiller import distill_single_name_and_address, distill_multiple_details


def test_name_with_address_both_specified():
    name = "Sherlock Holmes"
    address = "221B Baker Street"

    full_address = distill_single_name_and_address(name, address)
    
    assert full_address == "Sherlock Holmes, 221B Baker Street"


def test_only_name_specified():
    name = "Sherlock Holmes"
    address = "[not specified]"
    full_address = distill_single_name_and_address(name, address)
    
    assert full_address == "Sherlock Holmes"


def test_only_address_specified():
    name = "[not specified]"
    address = "221B Baker Street"
    full_address = distill_single_name_and_address(name, address)
    
    assert full_address == "[not specified], 221B Baker Street"


def test_both_not_specified():
    name = "[not specified]"
    address = "[not specified]"
    full_address = distill_single_name_and_address(name, address)
    
    assert full_address == "[not specified]"


def test_multiple_on_single_form_all_values():
    name = "Sherlock Holmes; John Watson"
    address = "221B Baker Street; 222B Baker Street"
    full_address = distill_multiple_details(name, address)
    
    assert full_address == "Sherlock Holmes, 221B Baker Street; John Watson, 222B Baker Street"


