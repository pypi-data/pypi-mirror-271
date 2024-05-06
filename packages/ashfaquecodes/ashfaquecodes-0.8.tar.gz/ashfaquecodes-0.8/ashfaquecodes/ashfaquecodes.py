'''
    Author : Ashfaque Alam
    Date : June 22, 2022
    Colors the printed outputs
'''
from collections import OrderedDict
import re
import colorama
from colorama import Fore
from colorama import Style

colorama.init()

def blue_print_start():
    print(Style.RESET_ALL)
    print(Fore.BLUE + Style.BRIGHT)


def red_print_start():
    print(Style.RESET_ALL)
    print(Fore.RED + Style.BRIGHT)


def green_print_start():
    print(Style.RESET_ALL)
    print(Fore.GREEN + Style.BRIGHT)


def color_print_reset():
    print(Style.RESET_ALL)


#################
##### USAGE #####
#################

# import pprint
# pp = pprint.PrettyPrinter(indent=4)
# red_print_start()
# pp.pprint("--------------------------")
# color_print_reset()

### or, ###

# import pprint
# print(f'{Style.RESET_ALL} {Fore.LIGHTMAGENTA_EX}')
# print(">>>>>>>>><<<<<<<<")
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(VARIABLE_NAME)
# print(f'{Style.RESET_ALL}')

'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : July 17, 2022
    Pass a list of non-unique elements in this function and get a unique list returned.
'''
def unique_list(non_unique_list : list) -> list:
    import time

    start_time = time.time()
    # unique_lst = sorted(set(non_unique_list))    # ? This approach is a few mili-secs faster than: `list(set(non_unique_list))`
    unique_lst = list(set(non_unique_list))    # ? This approach is a few mili-secs slower than: `sorted(set(non_unique_list))`
    end_time = time.time()
    # print("Time taken to sort the list -----> ", end_time - start_time)

    return unique_lst
'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : October 1, 2022
    Pass a list of duplicate dictionaries in this function and get a unique list of dictionaries returned.
'''
def unique_list_of_dicts(non_unique_list_of_dicts : list) -> list:
    import time
    start_time = time.time()

    unique_lst_of_dicts = [dict(sub) for sub in set(frozenset(dct.items()) for dct in non_unique_list_of_dicts)]
    # unique_lst_of_dicts = list(map(dict, set(tuple(sorted(sub.items())) for sub in non_unique_list_of_dicts)))

    end_time = time.time()
    # print("Time taken -----> ", end_time - start_time)

    return unique_lst_of_dicts
'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : October 1, 2022
    Pass a list of empty and non-empty dictionaries in this function and get a list of non-empty dictionaries returned.
'''
def remove_empty_dicts_from_list(list_with_empty_dicts : list) -> list:
    import time
    start_time = time.time()

    list_with_no_empty_dicts = list(filter(None, list_with_empty_dicts))    # ? Fastest - 0.2ms for 300 items in list
    # list_with_no_empty_dicts = [item for item in list_with_empty_dicts if item]    # ? Second Fastest - 0.3ms for 300 items in list

    # for item in list_with_no_empty_dicts.copy():    # ? Slowest amongst the methods written above - 1.5ms for 300 items in list
    #     if item == {}: list_with_no_empty_dicts.remove(item)

    end_time = time.time()
    # print("Time taken -----> ", end_time - start_time)

    return list_with_no_empty_dicts
'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : October 1, 2022
    Pass a list of non-empty dictionaries in this function and get a sorted list of dictionaries returned according to your desired sorting key of the dict.
'''
def sort_list_of_dicts(unsorted_list : list, key : str, desc : bool = False) -> list:
    import time
    start_time = time.time()

    if desc:
        from operator import itemgetter
        sorted_list = sorted(unsorted_list, key=itemgetter(key), reverse=True)    # ? Sorting list of dicts in descending order according to the values of `key`.
    else:
        sorted_list = sorted(unsorted_list, key=lambda d: d[key])    # ? Sorting list of dicts in ascending order according to the values of `key`.

    end_time = time.time()
    # print("Time taken to sort the list -----> ", end_time - start_time)

    return sorted_list

#################
##### USAGE #####
#################

# from ashfaquecodes.ashfaquecodes import sort_list_of_dicts
# sort_list_of_dicts(unsorted_list = unsorted_lst, key = 'dict_key_name', desc = True)

'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : July 17, 2022
    Calculate execution time of your code and you can assign it in a variable and can also send it in json response.
'''
def get_execution_start_time() -> float:
    import time
    execution_start_time = time.perf_counter()
    return execution_start_time    # * Current time, BEFORE execution of our code.

def get_execution_end_time(execution_start_time : float, print_time : bool = False) -> str:
    import time
    # * Calculating execution time of our API and it's also sent in the API Response.
    execution_end_time = time.perf_counter()    # * Current time, AFTER execution of our code.
    total_execution_time = (execution_end_time - execution_start_time) * 1000
    if 1000 <= total_execution_time < 60000:    # * i.e., seconds
        total_execution_time /= 1000    # * Converting it in seconds.
        total_execution_time_str = str(round(total_execution_time, 2)) + " secs"    # * Converting it into string for API Response.
        if print_time:
            print('\n ##### Execution Time: {:.4f} secs ##### \n'.format(total_execution_time))
    elif total_execution_time >= 60000:    # * i.e., minutes
        total_execution_time /= 60000    # * Converting it in minutes.
        total_execution_time_mins_str = int(total_execution_time)    # * Extracting the decimal part (whole number)
        total_execution_time_secs_str = round((float('0' + str(total_execution_time - int(total_execution_time))[1:]) * 60), 2)    # * Converting fraction mins to secs
        total_execution_time_str = str(total_execution_time_mins_str) + " mins " + str(total_execution_time_secs_str) + " secs"    # * Converting it into string for API Response.
        if print_time:
            print('\n ##### Execution Time: {:.4f} mins ##### \n'.format(total_execution_time))
    else:    # * i.e., milliseconds
        if print_time:
            print('\n ##### Execution Time: {:.2f} ms ##### \n'.format(total_execution_time))
        total_execution_time_str = str(round(total_execution_time, 2)) + " ms"

    return total_execution_time_str


#################
##### USAGE #####
#################

# from ashfaquecodes.ashfaquecodes import (
#     execution_start_time
#     , total_execution_time_str
# )
# execution_start_time = get_execution_start_time()
# total_execution_time_str = get_execution_end_time(execution_start_time, print_time = True)

'''
    ENDS
'''



'''
    Author : Ashfaque Alam
    Date : April 19, 2022
    Custom Decorator to calculate execution time of a function.
'''
from functools import wraps
import time
import pprint
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(dict)
"""helper function to estimate view execution time"""
def timer(func):
    @wraps(func)    # used for copying func metadata
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()    # record start time
        result = func(*args, **kwargs)    # func execution
        end_time = time.perf_counter()    # record start time
        ## total_time = end_time - start_time    # Calculate time taken in secs
        total_time = (end_time - start_time) * 1000    # Calculating time taken in ms

        # output execution time to console
        if 1000 <= total_time < 60000:    # * i.e., seconds
            total_time /= 1000    # * Converting it in seconds.
            red_print_start()
            total_execution_time_str = str(round(total_time, 2)) + " secs"    # * Converting it into string for API Response.
            print('\n ##### Execution Time: {} ##### \n'.format(total_execution_time_str))
            # print('\n ##### Execution Time: {:.4f} secs ##### \n'.format(total_time))
            color_print_reset()

        elif total_time >= 60000:    # * i.e., minutes
            total_time /= 60000    # * Converting it in minutes.
            total_execution_time_mins_str = int(total_time)    # * Extracting the decimal part (whole number)
            total_execution_time_secs_str = round((float('0' + str(total_time - int(total_time))[1:]) * 60), 2)    # * Converting fraction mins to secs
            total_execution_time_str = str(total_execution_time_mins_str) + " mins " + str(total_execution_time_secs_str) + " secs"    # * Converting it into string for API Response.
            red_print_start()
            print('\n ##### Execution Time: {} ##### \n'.format(total_execution_time_str))
            # print('\n ##### Execution Time: {:.4f} mins ##### \n'.format(total_time))
            color_print_reset()

        else:    # * i.e., milliseconds
            total_execution_time_str = str(round(total_time, 2)) + " ms"
            red_print_start()
            print('\n ##### Execution Time: {} ##### \n'.format(total_execution_time_str))
            # print('\n ##### Execution Time: {:.2f} ms ##### \n'.format(total_time))
            color_print_reset()

        # ? DEPRECATED :-
        # if len(str(round(total_time))) >= 4:
        #     total_time /= 1000
        #     red_print_start()
        #     print('\n ##### Function {}{} {} took {:.4f} secs ##### \n'.format(func.__name__, args, kwargs, total_time))    # first item in the args, ie `args[0]` is `self`
        #     color_print_reset()
        # else:
        #     red_print_start()
        #     print('\n ##### Function {}{} {} took {:.2f} ms ##### \n'.format(func.__name__, args, kwargs, total_time))
        #     color_print_reset()

        return result
    return wrapper


#################
##### USAGE #####
#################

# from ashfaquecodes.ashfaquecodes import timer
# @timer
# def your_function(request):
    # pass

'''
    END
'''


'''
    Author : Ashfaque Alam
    Date : January 27, 2024
    Custom Colored Print Function
'''
# import colorama

# colorama.init()

def cprint(*args, color='white', end='\n', sep=' '):
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

    if color not in colors:
        raise ValueError("Invalid color. Choose from: " + ",".join(colors))

    colored_text = getattr(colorama.Fore, color.upper()) + colorama.Style.BRIGHT
    for arg in args:
        colored_text += str(arg)
    colored_text += colorama.Style.RESET_ALL

    print(colored_text, end=end, sep=sep)

#################
##### USAGE #####
#################
### ? (Just like the original `print` function with additinal color parameter.)

# from ashfaquecodes.ashfaquecodes import cprint

# cprint('This is ' + 'a' + ' test print statement', color='red')
# cprint('This is an error message', color='green')
# cprint("Python : %2d, Portal : %5.2f" % (1, 05.333), color='yellow')
# cprint("Total students : %3d, Boys : %2d" % (240, 120), color='blue')
# cprint("%7.3o" % (25), color='magenta')
# cprint("%10.3E" % (356.08977), color='cyan')
# cprint('I love "{}!"'.format('Python'), color='white')
# cprint(f"I love {'Python'} \"{'Language'}!\"", color='red')

# data = dict(fun ="Python", adj ="Portal")
# cprint("I love {fun} computer {adj}".format(**data), color='red')

# cstr = "I love Python"
# # Printing the center aligned string with fillchr
# cprint("Center aligned string with fillchr: ", color='green')
# cprint(cstr.center(40, '#'), color='yellow')

# # cprinting the left aligned string with "-" padding
# cprint("The left aligned string is : ", color='blue')
# cprint(cstr.ljust(40, '-'), color='magenta')

# # cprinting the right aligned string with "-" padding
# cprint("The right aligned string is : ", color='cyan')
# cprint(cstr.rjust(40, '-'), color='white')


'''
    ENDS
'''

'''
    Author : Ashfaque Alam
    Date : January 27, 2024
    Custom Colored Pretty Print Function
'''

import pprint
# import colorama

# colorama.init()

def cpprint(
        data
        , color: str = 'white'
        , indent: int = 2
        , width: int = 120    # ? width : The number of characters per line used in formatting.
        , depth: int = None    # ? depth : controls the maximum depth to print nested structures. It can be useful when dealing with deeply nested data structures to limit the output to a certain level. Setting it to `None` means no depth limit.
        , compact: bool = False    # ? When set to `True`, tries to minimize the amount of white space used in the output. When `False`, it inserts some new lines character to make the output easier to read.
        , sort_dicts: bool = False    # ? If `True`, dictionaries will be sorted by key. If `False`, the order of keys in dictionaries will be maintained.
):
    colors = ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']

    if color not in colors:
        raise ValueError("Invalid color. Choose from: " + ",".join(colors))

    # Format data using pprint.pformat
    formatted_data = pprint.pformat(data, indent=indent, width=width, depth=depth, compact=compact, sort_dicts=sort_dicts)
    # # Use pprint.PrettyPrinter for formatting with optional parameters
    # pretty_printer = pprint.PrettyPrinter(indent=indent, width=width, depth=depth, compact=compact, sort_dicts=sort_dicts)
    # formatted_data = pretty_printer.pformat(data)

    # Apply color to the formatted data
    colored_text = getattr(colorama.Fore, color.upper()) + colorama.Style.BRIGHT + formatted_data + colorama.Style.RESET_ALL

    print(colored_text)


#################
##### USAGE #####
#################

# from ashfaquecodes.ashfaquecodes import cpprint

# sample_data = {
#     'key5': 'value1',
#     'key2': 'value2',
#     'key3': {
#         'nested_key': 'nested_value',
#         'nested_dict': {
#             'deep_key': 'deep_value'
#         }
#     },
#     'key4': [1, 2, 3, 4, 5],
#     'key1': [
#         {'name': 'John', 'age': 30},
#         {'name': 'Alice', 'age': 25},
#         {'name': 'Bob', 'age': 35}
#     ]
# }

# cpprint(sample_data, indent = 4, color='green', width=80, depth=2, compact=False, sort_dicts=True)

# ? More detailed explaination of pprint can be found in this guide by Sion Chakrabarti : https://www.analyticsvidhya.com/blog/2021/05/make-your-output-prettier-using-pprint/

'''
    ENDS
'''


'''
    Author : Ashfaque Alam
    Date : May 05, 2024
    Query list of dicts with SQL-like WHERE clause.
    NB: The `query_conditions` string should be in SQL format. For example, "age == 25 OR name LIKE '%user11%'". Both AND and OR operators are supported.
'''

import sqlite3
from typing import List

def query_list_of_dicts_sqlite(data: List[dict], query_conditions: str, table_name: str = 'input_list') -> List[dict]:
    # NB: Each call to the function creates a new in-memory database, ensuring a fresh environment for each operation.
    '''
    # Example usage:-
    ```python
    query_conditions = "age > 25 OR name LIKE '%user11%'"
    filtered_data = query_list_of_dicts(input_list_of_dicts, query_conditions)
    ```
    '''
    # Create a SQLite database in memory
    conn = sqlite3.connect(':memory:')
    c = conn.cursor()

    # Create a table
    columns = ', '.join([f"{key} TEXT" for key in data[0].keys()])
    c.execute(f"CREATE TABLE {table_name} ({columns})")

    # Insert data into the table using executemany
    values = [tuple(row.values()) for row in data]
    c.executemany(f"INSERT INTO {table_name} VALUES ({', '.join(['?']*len(data[0]))})", values)

    # Commit changes
    conn.commit()

    # Query the database
    query = f"SELECT * FROM {table_name} WHERE {query_conditions}"
    c.execute(query)
    result = c.fetchall()

    # Convert the result to a list of dictionaries
    result_list = [dict(zip([column[0] for column in c.description], row)) for row in result]

    # Close the connection
    conn.close()

    return result_list

def query_list_of_dicts_pandas(data: List[dict], query_conditions: str) -> List[dict]:
    '''
    # Example usage:-
    ```python
    query_conditions = 'age == 25 or name.str.contains("user11")'
    filtered_data = query_list_of_dicts(input_list_of_dicts, query_conditions)
    ```
    '''
    # Check if pandas installed, else throw an error and ask to install it.
    try:
        import pandas as pd
    except ImportError:
        raise ImportError("The pandas library is not installed. Please install it using `pip install pandas`")

    # Create a DataFrame from the list of dictionaries
    df = pd.DataFrame(data)

    # Query the DataFrame
    result_df = df.query(query_conditions, engine='python')

    # Convert the result to a list of dictionaries
    result_list = result_df.to_dict(orient='records')

    return result_list

def query_list_of_dicts(data: List[dict], query_conditions: str, engine='sqlite', table_name: str = 'input_list') -> List[dict]:
    '''
    ### Usage
    #### sqlite engine
    ```python
    query_conditions = "age > 25 OR name LIKE '%user11%'"
    filtered_data = query_list_of_dicts(input_list_of_dicts, query_conditions)
    ```
    #### pandas engine
    ```python
    query_conditions = 'age == 25 or name.str.contains("user11")'
    filtered_data = query_list_of_dicts(input_list_of_dicts, query_conditions, engine='pandas')
    ```
    '''
    if engine == 'sqlite':    # ? This is the default engine, as it takes half the time as compared to the pandas engine.
        return query_list_of_dicts_sqlite(data, query_conditions, table_name)
    elif engine == 'pandas':
        return query_list_of_dicts_pandas(data, query_conditions)
    else:
        raise ValueError(f"Unknown engine: {engine}")

'''
    ENDS
'''

