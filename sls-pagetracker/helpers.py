# helpers for the web tracking functions

from datetime import datetime
from functools import reduce

def parse_date_string_or_timestamp(date_string, timestamp_string=''):
    ''' Try to parse the given date_string into a (YYYYMM, DD) tuple. If it does not exist, do the
        same for the timestamp from the timestamp_string. If that fails, return None.'''
    TIME_STRING_FMT = "%Y-%m-%d"
    t = None
    if date_string:
        # Try to parse the date
        try:
            t = datetime.strptime(date_string, TIME_STRING_FMT).strftime("%Y%m D%d").split()
        except Exception as e:
            print(f"Unable to parse provided 'from_date' parameter: {date_string}")

    if not t:
        # Try timestamp string
        try:
            t = datetime.fromtimestamp(int(timestamp_string)).strftime("%Y%m D%d").split()
        except (ValueError, TypeError) as e:
            print(f"Invalid timestamp string given: {timestamp_string}")

    return tuple(t) if t else t

def sparse_dict_to_array(sd, offset=0):
    ''' Converts a dict of the form {'idx': val,...} where idx is an integer index to an array where
        the appropriate indices contain the values and all missing indices are zero.
        keys and values in the sparse-defined dictionary must be either ints or string representations
        of ints.
    '''
    # Get the largest index, define the array
    array = [0,] * (max(map(int, sd)) + 1 - offset)

    # Define a reducer function to fill (index, val) tuples into the array
    def populate(acc, val):
        acc[int(val[0]) - offset] = int(val[1])
        return acc

    return reduce(populate, sorted(sd.items()), array)
