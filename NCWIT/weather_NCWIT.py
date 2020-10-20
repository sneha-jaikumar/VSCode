"""Collects data from a real-world weather dataset: JFK, New York."""

import sys
from typing import List, Dict
from csv import DictReader

__author__ = "730395204"

NUM_ARGS: int = 4
FILE_INDEX: int = 1
COLUMN_INDEX: int = 2
OPERATION_INDEX: int = 3
VALID_OPERATIONS: List[str] = ["list", "min", "max", "avg", "chart", "repeats"]
READ_FILE: str = "r" 
BOTTOM_SUBPLOT_PARAM: float = 0.30
ROTATION_DEGREES: float = 90
FIGURE_LENGTH: float = 9
FIGURE_WIDTH: float = 4


def main() -> None:
    """Entrypoint of program run as module."""
    args: Dict[str, str] = read_args()
    search_file(args["FILE"], args["COLUMN"], args["OPERATION"])

    
def read_args() -> Dict[str, str]:
    """Checks for a valid operation."""
    if len(sys.argv) != NUM_ARGS:
        print("Usage: python -m projects.pj01.weather [FILE] [COLUMN] [OPERATION]")
        exit() 
    if sys.argv[OPERATION_INDEX] not in VALID_OPERATIONS:
        print("Invalid operation: " + sys.argv[OPERATION_INDEX])
        exit()
    return{
        "FILE": sys.argv[FILE_INDEX],
        "COLUMN": sys.argv[COLUMN_INDEX],
        "OPERATION": sys.argv[OPERATION_INDEX]
    }


def sod_rows(file_path: str, column_name: str) -> List[Dict[str, str]]:
    """Checks to see if column_name is in CSV file and returns the rows that have SOD as the REPORT_TYPE."""
    table: List[Dict[str, str]] = []
    SOD_rows: List[Dict[str, str]] = []
    file_handle = open(file_path, READ_FILE, encoding="utf8")
    csv_reader = DictReader(file_handle)

    for row in csv_reader:
        str_row: Dict[str, str] = {}
        for column in row:
            str_row[column] = row[column]  
        table.append(str_row) 

    not_in_CSV: bool = True
    for row in table:
        for key in row:
            if column_name == key: 
                not_in_CSV = False
    if not_in_CSV:
        print("Invalid column: " + sys.argv[COLUMN_INDEX]) 
        exit() 
    
    for row in table:
        if row["REPORT_TYPE"] == "SOD  ":
            SOD_rows.append(row)
    file_handle.close()
    return SOD_rows


def list(file_path: str, column: str, sod_list: List[Dict[str, str]]) -> List[float]:
    """Produces a list of values in the provided column."""
    values_in_column: List[float] = []
    file_handle = open(file_path, READ_FILE, encoding="utf8")
    
    for row in sod_list:
        try:
            values_in_column.append(float(row[column]))
        except ValueError:
            ...

    file_handle.close()        
    return values_in_column


def chart_dates(file_path: str, column: str, sod_list: List[Dict[str, str]], column_vals: List[float]) -> List[str]:
    """Produces a list of relevant dates."""
    dates_list: List[str] = []
    final_dates_list: List[str] = []
    file_handle = open(file_path, READ_FILE, encoding="utf8")
    
    for row in sod_list:
        will_work: bool = False
        for val in column_vals:
            try:
                if float(row[column]) == val:
                    will_work = True
            except ValueError:
                ...

        if will_work:        
            dates_list.append(row["DATE"]) 

    for date in dates_list:
        final_date: str = ""
        char: int = 0
        while date[char] != "T":
            final_date += date[char]
            char += 1
        final_dates_list.append(final_date)

    file_handle.close()
    return final_dates_list


def chart_data(data: List[float], column: str, dates: List[str]) -> None:
    """Constructs a chart given data, dates, and the column."""
    import matplotlib.pyplot as plt
    plt.figure(figsize=(FIGURE_LENGTH, FIGURE_WIDTH))
    plt.subplots_adjust(bottom=BOTTOM_SUBPLOT_PARAM)
    # plot the values of our data over time
    plt.plot(dates, data)
    # label the x-axis Date
    plt.xlabel("Date")
    plt.xticks(rotation=ROTATION_DEGREES)
    # label the y-axis whatever column we are analyzing
    plt.ylabel(column)
    # plot!
    plt.show()

def dupes(duped: List[float]) -> List[float]:
    """Returns a list of duplicates."""
    dupes: List[float] = []
    result: List[float]= []
    for x in duped:
        exists: bool = False

        for y in result:
            if x == y:
                exists = True   
                dupes.append(y)

        if not exists:
            result.append(x)

    return dupes


def noDupes(duped: List[float]) -> List[float]:
    """Returns a list of no duplicates."""
    result: List[float]= []
    for x in duped:
        exists: bool = False

        for y in result:
            if x == y:
                exists = True   

        if not exists:
            result.append(x)

    return result


def search_file(file: str, column_name: str, operation: str) -> None:
    """Performs the necessary operation (list, max, min, avg, chart) and prints the result."""
    SOD_rows: List[Dict[str, str]] = sod_rows(file, column_name)
    if operation == VALID_OPERATIONS[0]:
        print(list(file, column_name, SOD_rows))

    elif operation == VALID_OPERATIONS[1]:
        print(min(list(file, column_name, SOD_rows)))

    elif operation == VALID_OPERATIONS[2]:
        print(max(list(file, column_name, SOD_rows)))

    elif operation == VALID_OPERATIONS[3]:
        print(sum(list(file, column_name, SOD_rows)) / len(list(file, column_name, SOD_rows)))

    elif operation == VALID_OPERATIONS[4] :
        dates: List[str] = chart_dates(file, column_name, SOD_rows, list(file, column_name, SOD_rows))
        chart_data(list(file, column_name, SOD_rows), column_name, dates)
    else:
        print(noDupes(dupes(list(file, column_name, SOD_rows))))
        



if __name__ == "__main__":
    main()