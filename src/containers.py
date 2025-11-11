from dataclasses import dataclass, field
import re

@dataclass
class Farm:
    """
    all values except catalogue_reference will be instantiated from the raw csv data and then validated in a later step
    all fields after primary_farm_number are lists to accomodate variation in names and addresses when original forms were filled out 
    e.g., "Mr D. Smith", "D. Smith", "Dennis Smith Esq" entered as names for same person
    These fields will be merged later to create a single name/address so are declared as either lists of strings or single strings
    """
    catalogue_reference: str
    forms: dict[list] = field(default={'C51/SSY': [], 'B496/EI': [], 'C 47/SSY': [], 'C 49/SSY': [], 'SF': [], 'SF C69/SSY': [], 'Other': [], 'Cover': []})
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: list[str]
    farm_names: list[str]
    # occupier details
    addressee_title: list[str] | str
    addressee_individual_name: list[str] | str
    addressee_group_names: list[str]
    address: list[str] | str
    # owner details
    owner_title: list[str] | str
    owner_individual_name: list[str] | str
    owner_group_names: list[str]
    owner_address: list[str] | str
    # farmer details
    farmer_title: list[str] | str
    farmer_individual_name: list[str] | str
    farmer_group_names: list[str]
    farmer_address: list[str] | str
    acreage: list[str] | str
    OS_map_sheet: list[str] | str
    field_info_date: list[str] | str
    primary_record_date: list[str] | str

    def split_and_strip_value(self, field_value: str) -> list[str]:
        """Utility method to split a field value by commas and strip whitespace."""
        return [item.strip() for item in re.split(r", *", field_value)]


