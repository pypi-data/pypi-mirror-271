[![License: GNU GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/ashfaque/ashfaquecodes/blob/main/LICENSE)

## How to install
```sh
pip install ashfaquecodes
```

## Documentation
- Color the printed outputs in terminal.
    ```python
    from ashfaquecodes.ashfaquecodes import (
        , blue_print_start
        , red_print_start
        , green_print_start
        , color_print_reset
    )
    import pprint
    pp = pprint.PrettyPrinter(indent=4)
    # blue_print_start()
    red_print_start()
    # green_print_start()
    pp.pprint("--------------------------")
    color_print_reset()
    ```

- Get a unique list if list of non-unique elements passed in this function.
    ```python
    from ashfaquecodes.ashfaquecodes import unique_list
    _ = unique_list(non_unique_list)
    ```

- Get unique list of dictionaries if a list of duplicate dictionaries passed in this function.
    ```python
    from ashfaquecodes.ashfaquecodes import unique_list_of_dicts
    _ = unique_list_of_dicts(non_unique_list_of_dicts)
    ```

- Get a list of non-empty dictionaries if a list of empty and non-empty dictionaries passed in this function.
    ```python
    from ashfaquecodes.ashfaquecodes import remove_empty_dicts_from_list
    _ = remove_empty_dicts_from_list(list_with_empty_dicts)
    ```

- Get a sorted list of dictionaries returned according to your desired sorting key of the dictionary if a list of non-empty dictionaries passed in this function. Supports ascending and descending order.
    ```python
    from ashfaquecodes.ashfaquecodes import sort_list_of_dicts
    _ = sort_list_of_dicts(unsorted_list = unsorted_lst, key = 'dict_key_name', desc = True)
    ```

- Get execution time of your code. Can also prints the execution time in terminal if an optional parameter `print_time = True` is passed in the function.
    ```python
    from ashfaquecodes.ashfaquecodes import (
        get_execution_start_time
        , get_execution_end_time
    )
    execution_start_time = get_execution_start_time()
    total_execution_time_str = get_execution_end_time(execution_start_time, print_time = True)
    ```

- Custom Decorator to calculate execution time of a function which will be printed in the terminal during execution of that function.
    ```python
    from ashfaquecodes.ashfaquecodes import timer
    @timer
    def your_function(request):
        pass
    ```

- Custom `cprint()` function to print output in the terminal with different colors.
    ```python
    from ashfaquecodes.ashfaquecodes import cprint

    cprint('This is ' + 'a' + ' test print statement', color='red')
    cprint('This is an error message', color='green')
    cprint("Python : %2d, Portal : %5.2f" % (1, 05.333), color='yellow')
    cprint("Total students : %3d, Boys : %2d" % (240, 120), color='blue')
    cprint("%7.3o" % (25), color='magenta')
    cprint("%10.3E" % (356.08977), color='cyan')
    cprint('I love "{}!"'.format('Python'), color='white')
    cprint(f"I love {'Python'} \"{'Language'}!\"", color='red')

    data = dict(fun ="Python", adj ="Portal")
    cprint("I love {fun} computer {adj}".format(**data), color='red')

    cstr = "I love Python"
    # Printing the center aligned string with fillchr
    cprint("Center aligned string with fillchr: ", color='green')
    cprint(cstr.center(40, '#'), color='yellow')

    # cprinting the left aligned string with "-" padding
    cprint("The left aligned string is : ", color='blue')
    cprint(cstr.ljust(40, '-'), color='magenta')

    # cprinting the right aligned string with "-" padding
    cprint("The right aligned string is : ", color='cyan')
    cprint(cstr.rjust(40, '-'), color='white')
    ```

- Custom `cpprint` function to pprint output in the terminal with different colors and different formats.
    ```python
    from ashfaquecodes.ashfaquecodes import cpprint

    sample_data = {
        'key5': 'value1',
        'key2': 'value2',
        'key3': {
            'nested_key': 'nested_value',
            'nested_dict': {
                'deep_key': 'deep_value'
            }
        },
        'key4': [1, 2, 3, 4, 5],
        'key1': [
            {'name': 'John', 'age': 30},
            {'name': 'Alice', 'age': 25},
            {'name': 'Bob', 'age': 35}
        ]
    }

    cpprint(sample_data, indent = 4, color='green', width=80, depth=2, compact=False, sort_dicts=True)
    # Available colors: ['red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'white']
    ```

- Query a large list of dicts like any SQL WHERE clause.
    ```python
    from ashfaquecodes.ashfaquecodes import query_list_of_dicts

    data = [
        {'age': 23, 'name': 'user11'},
        {'age': 27, 'name': 'user12'},
        {'age': 25, 'name': 'user13'}
    ]

    # Using the 'sqlite' engine (default)
    query_conditions = "age > 25 OR name LIKE '%user11%'"
    filtered_data = query_list_of_dicts(input_list_of_dicts, query_conditions)

    # Using the 'pandas' engine (pandas needs to be installed to use this)
    query_conditions = 'age == 25 or name.str.contains("user11")'
    filtered_data = query_list_of_dicts(input_list_of_dicts, query_conditions, engine='pandas')
    ```



## License
[GNU GPLv3](LICENSE)

