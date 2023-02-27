# Test the helpers.py function

import pytest

from helpers import parse_date_string_or_timestamp, sparse_dict_to_array

@pytest.mark.parametrize("date_str,expected",
    [("2022-08-07", ("202208", "D07")), ("2023-01-14", ("202301", "D14")), ("1234567", None)])
def test_parse_date_string(date_str, expected):
    assert parse_date_string_or_timestamp(date_str) == expected

@pytest.mark.parametrize("ts_str,expected",
    [("1659881100", ("202208", "D07")), ("1673673420", ("202301", "D14")), ("ERROR", None)])
def test_parse_timestamp_string(ts_str, expected):
    assert parse_date_string_or_timestamp(None, ts_str) == expected

@pytest.mark.parametrize("test_dict,expected",
    [
        ({1: 1, 2: 2, 3: 3}, [0,1,2,3]),
        ({'5': '5', '4': 4, '1': '1', '8': 8}, [0,1,0,0,4,5,0,0,8]),
    ])
def test_sparse_dict_to_array(test_dict,expected):
    assert sparse_dict_to_array(test_dict) == expected

def test_sparse_dict_to_array_offset():
    test_dict = {4: 4, 2: 2, 1: 1}
    assert sparse_dict_to_array(test_dict, offset=1) == [1,2,0,4]
