import re
from datetime import datetime
import calendar

def date_check(potential_date, row_num):    
    ''' Checks if the date, given as a string, is a valid date
    
        Key Arguments:
            potential_date - string containing the date value for checking
            row_num - string with the number of the row in the source spreadsheet
            
        Returns:
            Tuple with either the date as a date object or the original string if it isn't a valid date and a set with any warnings
    '''
    
    # potential_date = potential_date.strip()

    MONTH_NAMES: list = "|".join(list(calendar.month_name)[1:])
    RGX_DAYMONTHYEAR = re.compile(fr"""^(?P<day>\d\d?) +(?P<month>{MONTH_NAMES}) +(?P<year>\d\d\d\d)$""")
    RGX_MONTHYEAR = re.compile(fr"""^(?P<month>{MONTH_NAMES}) +(?P<year>\d\d\d\d)$""")

    if rgxmatch := RGX_DAYMONTHYEAR.search(potential_date) or RGX_MONTHYEAR.search(potential_date):
        if rgxmatch['year'] not in ["1941", "1942", "1943"]:
            warning = f"Row {row_num}: Error: Date ({potential_date}) is not recognized as within the expected range."
            return (potential_date, warning)
    
    if RGX_DAYMONTHYEAR.search(potential_date):
        try:
            return (datetime.strptime(potential_date, "%d %B %Y"), "VALID")
        except ValueError as ve:
            # ve = "day is out of range for month":
            warning = f"Row {row_num}: Error: Date ({potential_date}) is invalid ({ve}). Further date checks cannot be carried out."
            return (potential_date, warning)   
                    
    if RGX_MONTHYEAR.search(potential_date):
        return (datetime.strptime(potential_date, "%B %Y"), "VALID")
                    
    else:
        warning = f"Row {row_num}: Error: Date ({potential_date}) is not in the expected format. Further date checks cannot be carried out."
        return (potential_date, warning)


if __name__ == "__main__":
    test_dates = [
        "29 February 1943",
        "15 October 1941",
        "January 1942",
        "5th 1943",
        "4th July 1942",
        "4 July 1942",
        "10 1942",
        "31 October 1940",
        "July 1941",
        "September 1945",
        "1943",
    ]
row = 5

for test in test_dates:
    candidate_date, warning = date_check(test, row)
    print(f"Test date: {test} - {candidate_date}, {warning}")
