import re

from src._dataclasses.farm_combine import HarvestedFarm, PostalDetails, Respondent
from src.harvester.details_resolver import resolve_postal_details


def collate_attributes(values: list[str]) -> str:
    output = []
    for item in values:
        if item not in output and item not in ["_null_", "_not transcribed_"]:
            output.append(item)

    return output or ["[not specified]",]


def set_values_of_non_respondent_attributes(farm: HarvestedFarm, attributes: dict) -> HarvestedFarm:
    for field in ['farm_name', 'acreage', 'OS_map_sheet', 'field_info_date', 'primary_record_date']:
        if field == 'farm_name':
            unique_farm_names = []
            for names in attributes[field]:
                for _name in re.split("; *", names):
                    if _name in unique_farm_names:
                        continue
                    unique_farm_names.append(_name)
            value = unique_farm_names

        else:
            value = attributes[field]

        output_value = collate_attributes(value)
        setattr(farm, field, output_value)

    return farm


def resolve_postal_details_of_respondents(attributes: dict) -> dict:
    addressee_details, addressee_warning = resolve_postal_details(
            attributes['addressee_title'],
            attributes['addressee_individual_name'],
            attributes['addressee_group_names'],
            attributes['address'],
        )
    landowner_details, landowner_warning = resolve_postal_details(
            attributes['owner_title'],
            attributes['owner_individual_name'],
            attributes['owner_group_names'],
            attributes['owner_address'],
        )
    farmer_details, farmer_warning = resolve_postal_details(
            attributes['farmer_title'],
            attributes['farmer_individual_name'],
            attributes['farmer_group_names'],
            attributes['farmer_address'],
        )

    return {
        "details": {'addressee': addressee_details, 'farmer': farmer_details, 'landowner': landowner_details},
        "warnings": {'addressee': addressee_warning, 'farmer': farmer_warning, 'landowner': landowner_warning},
    }


def set_postal_details(values: list[dict]) -> list[PostalDetails]:
    if len(values) > 1:
        final_values = [
            item
            for item in values
            if (item['name'], item['address']) != ('[not specified]', '[not specified]')
        ]
    else:
        final_values = values

    return [
        PostalDetails(name=item['name'], address=item['address'])
        for item in final_values
    ]


def create_respondents(farm: HarvestedFarm, details: dict) -> HarvestedFarm:
    farm.addressee = Respondent(set_postal_details(details['addressee']))
    farm.farmer = Respondent(set_postal_details(details['farmer']))
    farm.landowner = Respondent(set_postal_details(details['landowner']))

    return farm


def get_postal_details_warnings(warnings: dict) -> dict:
    farm_warnings = {}
    if warnings['addressee']:
        farm_warnings.update({'Addressee name warnings': warnings['addressee']})
    if warnings['farmer']:
        farm_warnings.update({'Farmer name warnings': warnings['farmer']})
    if warnings['landowner']:
        farm_warnings.update({'Landowner name warnings': warnings['landowner']})

    return farm_warnings


def set_farm_attributes(farm, farm_data):
    farm.forms = farm_data['forms']

    farm = set_values_of_non_respondent_attributes(farm, farm_data['attributes'])

    resolution = resolve_postal_details_of_respondents(farm_data['attributes'])
    farm = create_respondents(farm, resolution['details'])

    farm.warnings = farm_data['warnings']
    farm.warnings.update(get_postal_details_warnings(resolution['warnings']))
    return farm

