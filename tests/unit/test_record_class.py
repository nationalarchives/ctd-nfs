
import pytest


_PROOF_DATA = {
    'catalogue_reference': "MAF 32/346/7/18",
    'farm_number': "RD/7/18",
    'filenames': "MAF32-346-7_67.tif, MAF32-346-7_68.tif; MAF32-346-7_25.tif, MAF32-346-7_26.tif; MAF32-346-7_123.tif, MAF32-346-7_124.tif; MAF32-346-7_47.tif, MAF32-346-7_48.tif; MAF32-346-7_51.tif, MAF32-346-7_52.tif",
    'forms': "C 47/SSY; C51/SSY; SF; B496/EI (1); B496/EI (2)",
    'farm_name': "Granby Lodge",
    'addressee': "Mr A Shephard, Granby Lodge, Bisbrooke, Uppingham, Rutland",
    'farmer': "A Shepherd, Bisbrooke, Uppingham",
    'landowner': "E C Hinch, Little Casterton, Stamford",
    'acreage': "58 A, 57 G, 115",
    'os_sheet_number': "Rutland 13 NE 1905 Edition",
    'field_info_date': "16 December 41",
    'primary_record_date': "[not specified]",
    'additional_farms': "B496/EI (1) also included in MAF 32/346/7/10",
}

@pytest.mark.skip(reason="awaiting refactoring")
def test_record_subdocument_creation():
    # test_record = Record(
    #     citableReference=_PROOF_DATA['catalogue_reference'],
    # )

    expected_result = {
            'parentId': "C7283514",
        }
    # assert expected_result['parentId'] == test_record.parentId        


@pytest.mark.skip(reason="awaiting refactoring")
def test_replica_subdocument_creation():
    # farm = get_farm_instance(_PROOF_DATA['catalogue_reference'])
    # test_replica = build_replica_subdocument(farm.forms)

    expected_result = {
        'originalName': _PROOF_DATA['filenames'].split()[0].strip(",;"),
        'name': "66/MAF/32/"}

    # assert expected_result['originalName'] == test_replica.files[0].originalName
    # assert test_replica.files[0].name.startswith(expected_result['name'])


