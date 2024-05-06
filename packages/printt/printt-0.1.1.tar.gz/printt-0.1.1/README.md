# **Printt (Detailed print)**

**Description**

This Python library, `printt` (**printt**), offers a convenient way to print detailed information about variables during development and debugging. It leverages the rich library for visually appealing output in your terminal.

**Features**

* **Variable Name Detection:** Attempts to automatically identify the variable name using introspection.
* **Human-Readable Size Conversion:** Converts raw byte sizes of variables into human-readable formats like KB, MB, GB, etc.
* **Customizable Printing:** Control whether to print the actual variable value or a placeholder message using the `print_variable` flag.
* **Exception Handling:** Gracefully handles potential exceptions during information retrieval, providing informative error messages.
* **Rich Formatting:** Employs rich library for visually-appealing output in your terminal.

**Installation**

Install `printt` using Poetry:

``` bash
poetry install printt
```

**Usage**

1. **Import**:

``` python
from printt import printt
```

2. **Print Variable Details**:

``` python
my_list = [1, 2, 3]
printt(my_list)
```

This will output details like variable name (if found), class type, size, and results of attempting to call `type`, `dir`, `len`, and a function to calculate memory usage.

**Enabling/Disabling Printing**

* **Enable printing:**

``` python
from printt import enable_printt
enable_printt()
```

* **Disable printing:**

``` python
from printt import disable_printt
disable_printt()
```

**Additional Notes**

* The automatic variable name detection might not work in all cases.
* Exception handling helps prevent unexpected errors while debugging.

**Contributing**

We welcome contributions to improve `printt`. Please feel free to submit pull requests!

**License**

This project is licensed under the terms of the MIT License (see LICENSE.md for details).