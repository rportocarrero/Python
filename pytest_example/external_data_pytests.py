# Description: This file contains the code to test the external data using pytest
import csv
import pytest

# load data from csv file
def load_csv_data(file_name):
    with open(file_name) as csvfile:
        reader = csv.DictReader(csvfile)
        data = []
        for row in reader:
            data.append((row['a'], row['b'], row['expected']))
        return data
    
test_data = load_csv_data("data.csv")

# test the data with parameterized decorators
@pytest.mark.parametrize("a, b, expected", test_data)
def test_function(a, b, expected):
    assert int(a) + int(b) == int(expected)
