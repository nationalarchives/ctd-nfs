from src.harvester.distillation.distiller import \
    distill_single_name_and_address, \
    distill_multiple_details, \
    distill_single_title_and_name


def test_single_person_with_full_details():
    title = "Mr"
    name = "Sherlock Holmes"
    address = "221B Baker Street"

    full_address = distill_single_name_and_address(title, name, address)
    
    assert full_address == "Mr Sherlock Holmes, 221B Baker Street"


def test_single_person_with_full_details_and_appended_title():
    title = "KC"
    name = "Sherlock Holmes"
    address = "221B Baker Street"

    full_address = distill_single_name_and_address(title, name, address)
    
    assert full_address == "Sherlock Holmes, KC, 221B Baker Street"


def test_single_person_with_only_name_specified():
    title = "[not specified]"
    name = "Sherlock Holmes"
    address = "[not specified]"
    full_address = distill_single_name_and_address(title, name, address)
    
    assert full_address == "Sherlock Holmes"


def test_single_person_with_only_address_specified():
    title = "[not specified]"
    name = "[not specified]"
    address = "221B Baker Street"
    full_address = distill_single_name_and_address(title, name, address)
    
    assert full_address == "[not specified], 221B Baker Street"


def test_single_person_with_only_title_specified():
    title = "Mr"
    name = "[not specified]"
    address = "[not specified]"
    full_address = distill_single_name_and_address(title, name, address)
    
    assert full_address == "[not specified]"


def test_single_person_with_no_details():
    title = "[not specified]"
    name = "[not specified]"
    address = "[not specified]"
    full_address = distill_single_name_and_address(title, name, address)
    
    assert full_address == "[not specified]"


def test_full_details_for_two_people():
    titles = "Mr; Dr"
    names = "Sherlock Holmes; John Watson"
    addresses = "221B Baker Street; 222B Baker Street"
    full_address = distill_multiple_details(titles, names, addresses)
    
    assert full_address == "Mr Sherlock Holmes, 221B Baker Street; Dr John Watson, 222B Baker Street"


def test_full_details_for_two_people_with_missing_address():
    titles = "Mr; Dr"
    name = "Sherlock Holmes; John Watson"
    address = "221B Baker Street; [not specified]"
    full_address = distill_multiple_details(titles, name, address)
    
    assert full_address == "Mr Sherlock Holmes, 221B Baker Street; Dr John Watson"


def test_full_details_for_two_people_with_missing_name():
    titles = "Mr; Dr"
    name = "[not specified]; John Watson"
    address = "221B Baker Street; 221B Baker Street"
    full_address = distill_multiple_details(titles, name, address)
    
    assert full_address == "[not specified], 221B Baker Street; Dr John Watson, 221B Baker Street"


def test_full_details_for_two_people_with_name_and_address_v1():
    titles = "Mr; Dr"
    name = "[not specified]; John Watson"
    address = "221B Baker Street; [not specified]"
    full_address = distill_multiple_details(titles, name, address)
    
    assert full_address == "[not specified], 221B Baker Street; Dr John Watson"


def test_full_details_for_two_people_with_missing_title_and_address_v2():
    titles = "Mr; [not specified]"
    name = "Sherlock Holmes; John Watson"
    address = "[not specified]; 221B Baker Street"
    full_address = distill_multiple_details(titles, name, address)
    
    assert full_address == "Mr Sherlock Holmes; John Watson, 221B Baker Street"


def test_title_and_name_both_specified():
    title = "Mr"
    name = "Sherlock Holmes"

    full_address = distill_single_title_and_name(title, name)
    
    assert full_address == "Mr Sherlock Holmes"


def test_title_wihtout_name():
    title = "Mr"
    name = "[not specified]"

    full_address = distill_single_title_and_name(title, name)
    
    assert full_address == "[not specified]"


def test_name_without_title():
    title = "[not specified]"
    name = "Sherlock Holmes"

    full_address = distill_single_title_and_name(title, name)
    
    assert full_address == "Sherlock Holmes"


def test_without_name_nor_title():
    title = "[not specified]"
    name = "[not specified]"

    full_address = distill_single_title_and_name(title, name)
    
    assert full_address == "[not specified]"


def test_title_after_name():
    title = "Esq"
    name = "Sherlock Holmes"

    full_address = distill_single_title_and_name(title, name)
    
    assert full_address == "Sherlock Holmes, Esq"


def test_full_details_for_multiple_people():
    titles = "Esq.; Dr; Insp; Prof"
    names = "Sherlock Holmes; John Watson; Baynes; James Moriarty"
    addresses = "221B Baker Street; 222B Baker Street; Surrey Constabulary, Guildford; London"
    full_address = distill_multiple_details(titles, names, addresses)
    
    assert full_address == "Sherlock Holmes, Esq., 221B Baker Street; Dr John Watson, 222B Baker Street; Insp Baynes, Surrey Constabulary, Guildford; Prof James Moriarty, London"
