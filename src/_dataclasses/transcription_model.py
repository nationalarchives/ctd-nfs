from dataclasses import dataclass, InitVar
import re

from src._tools.helpers import DomainRuleValidationException, ValueObject
from src._tools.constants import REGEX, DATA


def page_pattern_match(filename: str) -> re.Match:
    return REGEX.FORM_PATTERN.match(filename)


def cover_pattern_match(filename: str) -> re.Match:
    return REGEX.COVER_PATTERN.match(filename)


@dataclass(frozen=True)
class Filename(ValueObject):
    name: str

    def __post_init__(self):
        if not (page_pattern_match(self.name) or cover_pattern_match(self.name)):
            raise DomainRuleValidationException(f"{self.name} does not match expected pattern for form images or cover.")

    @property   
    def is_cover(self) -> bool:
        if cover_pattern_match(self.name) or page_pattern_match(self.name)['image_number'] == "0001":
            return True

        return False
    
    @property
    def image_number(self) -> int | None:
        if match := page_pattern_match(self.name):
            return int(match['image_number'])
    
    @property
    def piece(self) -> str:
        match = (page_pattern_match(self.name) or cover_pattern_match(self.name))
        return match['piece']
    
    @property
    def parish_number(self) -> str:
        match = (page_pattern_match(self.name) or cover_pattern_match(self.name))
        return match['parish_number']


@dataclass(frozen=True)
class FormType(ValueObject):
    name: str

    def __post_init__(self):
        if self.name not in DATA.FORM_TYPES:
            raise DomainRuleValidationException(f"Form type '{self.name}' is not a recognised form.")

@dataclass
class Details:
    title: str
    individual_name: str
    group_names: str
    address: str
    full_address: str = ""


def _normalize_date(candi_date: str) -> str:
    """Normalize date strings to a standard format day month year format e.g. 1 January 1941.
    Note: day must not have leading zeros.

    Args:
        date_str (str): The date string to normalize.

    Returns:
        str: The normalized date string.
    """

    if REGEX.MONTH.match(candi_date) or REGEX.MON.match(candi_date):
        if REGEX.MON.match(candi_date):
            index = DATA.ABBR_MONTH_NAMES.index(candi_date)
            candi_date = DATA.MONTH_NAMES[index]
        return f"{candi_date}"

    if REGEX.DAYMONTH.match(candi_date) or REGEX.DAYMON.match(candi_date):
        day, month = candi_date.split()
        if REGEX.DAYMON.match(candi_date):
            index = DATA.ABBR_MONTH_NAMES.index(month)
            month = DATA.MONTH_NAMES[index]
        return f"{int(day)} {month}"

    candi_date = REGEX.REMOVE_DELIMITERS.sub(' ', candi_date)
    date_match: dict[re.Match] = {
        'daymonthyear': REGEX.DAYMONTHYEAR.match(candi_date),
        'ddmmyyyy': REGEX.DDMMYYYY.match(candi_date),
    }
    if not (date_match['daymonthyear'] or date_match['ddmmyyyy']):
        return candi_date

    for fmt in DATA.DATE_FORMATS:
        try:
            parsed_date = datetime.strptime(candi_date, fmt)
            day, month, year = parsed_date.strftime("%d %B %Y").split()
            break
        except ValueError:
            continue

    return f"{int(day)} {month} {re.sub(r"^20", "19", year)}"


@dataclass
class Form:
    """
    all values except catalogue_reference will be instantiated from the raw csv data and then validated in a later step
    all fields after primary_farm_number are lists to accomodate variation in names and addresses when original forms were filled out 
    e.g., "Mr D. Smith", "D. Smith", "Dennis Smith Esq" entered as names for same person
    These fields will be merged later to create a single name/address so are declared as either lists of strings or single strings
    """
    filename_1: InitVar[Filename]
    filename_2: InitVar[Filename | None]
    document_type: FormType
    county: str
    parish: str
    primary_farm_number: str
    additional_farms: list[str]
    farm_name: list[str]
    addressee_title: InitVar[str]
    addressee_individual_name: InitVar[str]
    addressee_group_names: InitVar[str]
    address: InitVar[str]
    owner_title: InitVar[str]
    owner_individual_name: InitVar[str]
    owner_group_names: InitVar[str]
    owner_address: InitVar[str]
    farmer_title: InitVar[str]
    farmer_individual_name: InitVar[str]
    farmer_group_names: InitVar[str]
    farmer_address: InitVar[str]
    acreage: str
    OS_map_sheet: str
    field_info_date: str
    primary_record_date: str

    def __post_init__(self):
        self.file1 = self.filename_1
        self.file2 = self.filename_2
        self.addressee = Details(
            title=self.addressee_title,
            individual_name=self.addressee_individual_name,
            group_names=self.addressee_group_names,
            address=self.address,
        )
        self.owner = Details(
            title=self.owner_title,
            individual_name=self.owner_individual_name,
            group_names=self.owner_group_names,
            address=self.owner_address,
        )
        self.farmer = Details(
            title=self.farmer_title,
            individual_name=self.farmer_individual_name,
            group_names=self.farmer_group_names,
            address=self.farmer_address,
        )
