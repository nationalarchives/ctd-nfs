import pytest

from src._tools.helpers import DomainRuleValidationException
from src.harvester.form_setup import Filename


def test_valid_filename():
    fixture = "MAF32-194-1_59.tif"
    test = Filename(fixture)

    assert isinstance(test, Filename)
    assert test.is_cover is False


def test_cover_image_1():
    fixture = "MAF32-51-285_0001.tif"
    test = Filename(fixture)

    assert isinstance(test, Filename)
    assert test.is_cover


def test_cover_image_2():
    fixture = "MAF32-51-285.tif"
    test = Filename(fixture)

    assert isinstance(test, Filename)
    assert test.is_cover
    assert test.image_number is None


def test_bad_image_name():
    fixture = "MAF3251286.tif"

    with pytest.raises(DomainRuleValidationException):
        Filename(fixture)


def test_properties():
    fixture = "MAF32-194-1_59.tif"
    test = Filename(fixture)

    assert isinstance(test, Filename)
    assert test.image_number == 59
    assert test.piece == "194"
    assert test.parish_number == "1"



