import re
from datetime import datetime

from src._config.constants import REGEX

def date_check(potential_date) -> str:    
    ''' Checks if the date, given as a string, is a valid date
    
        Key Arguments:
            potential_date - string containing the date value for checking
            
        Returns:
            Tuple with either the date as a date object or the original string if it isn't a valid date and a set with any warnings
    '''

    date_match: dict[re.Match] = {
        'daymonthyear': REGEX.DAYMONTHYEAR.match(potential_date),
        'monthyear': REGEX.MONTHYEAR.match(potential_date),
        'yearonly': REGEX.YEARONLY.match(potential_date),
        'ddmmyyyy': REGEX.DDMMYYYY.match(potential_date),
    }

    date_type = (match_key for match_key in date_match.keys() if date_match[match_key])
    if not (date_type := next(date_type, None)):
        return f"Error: '{potential_date}' is not a valid format. Further date checks cannot be performed."

    is_valid_year = REGEX.SURVEY_YEARS.match(date_match[date_type]['year'])
    if not is_valid_year:
        return f"Warning: '{potential_date}' is outside the survey timespan."

    if date_type == 'ddmmyyyy':
        potential_date = re.sub(r'[-.]', '/', potential_date)
        day = date_match[date_type]['day'].zfill(2)
        month = date_match[date_type]['month'].zfill(2)
        year = f"19{date_match[date_type]['year'][-2:]}"
        potential_date = f"{day}/{month}/{year}"

    date_format: dict[str] = {
        'daymonthyear': "%d %B %Y",
        'monthyear': "%B %Y",
        'yearonly': "%Y",
        'ddmmyyyy': "%d/%m/%Y",
    }
    try:
        datetime.strptime(potential_date, date_format[date_type])
        return "VALID"
    except ValueError as ve:
        # ve = "day is out of range for month":
        return f"Error: {ve}"


if __name__ == "__main__":
    test_dates = [
        "32/01/1942",
        "29 February 1943",
        "15 October 1941",
        "January 1942",
        "4 July 1942",
        "05 July 1942",
        "July 1941",
        "1943",
        "01/05/1942",
        "6-6-1942",
        "12.12.1943",
        "1/1/42",
        "6 June",
        "10 1942",
        "4th July 1942",
        "5th 1943",
        "September 1945",
        "31 October 1940",
    ]

for test in test_dates:
    warning = date_check(test)
    print(f"Test date: {test} - {warning}")
