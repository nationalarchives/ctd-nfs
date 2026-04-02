from src.harvester.form_setup import Filename


def test_valid_filename():
    test_name = "MAF32-194-1_59.tif"

    assert isinstance(Filename(test_name), Filename)


def test_cover_image():
    test_name = "MAF32-51-285_0001.tif"

    assert isinstance(Filename(test_name), Filename)


