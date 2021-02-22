# ConfigParser

### A tool to parse and load key/value config files into native and json formats.

## Usage

### Dependencies

In order to run this application you need:
- MacOS(<span style="color:#3D9970">Fully Tested</span>)/Linux(<span style="color:#FF4136">Unverified</span>)
- Docker (Version 17.06.0 or higher)

Alternatively you may install python3 on your local system and follow the below instructions
- navigate to the `src` directory of this repository
- run `python3 -c "import app; app.parse_config('../config.sample')"` to parse the sample config file and print to stdout
- run `python3 tests.py` to run tests against ConfigParser and LineLexer objects


### Project structure/manifest

```
noc-list/               # Root directory.
|- run.sh               # Main application entry point. It abstracts docker commands, app startup and tests
|- README.md            # This file
|- src/                 # Main application directory
|-- src/tests.py        # Automated tests
|-- src/app.py          # Main application file
```

### Commands for running and testing application

```shell
./run.sh # Reads a sample config file and pretty prints a json version to stdout
./run.sh stop # Stops and removes dependencies
./run.sh test # runs automated tests against application
```

### Data Types

- booleans (yes, no, true, false, on, off)
- numbers (10, 2.44)
- alphanumeric strings (foo, bar, foo34)

### Assignment operators
- `=`

### Special characters
- `.` DOT is treated as a valid character and can be part of any literal name or numeric value
- `_` UNDERSCORE is treated as a valid character and can be part of any literal name but not numeric value or boolean
- `/` FORWARD SLASH is treated as a valid character and can be part of any literal name but not numeric value or boolean
- `#` HASH/NUMBER symbol is used to mark the remaining of the line as an ignorable comment (inclusive)
- `=` EQUAL sign is the assignment operator and cannot be used as literal


### The ConfigParser object
To access the values defined in a config file, you may call the get method and pass the key name to get the desired value. i.e.
~~~
txt_config = """
mykey=myvalue
"""
config = ConfigParser(txt_config)
print(config.get('mykey'))
// would output myvalue
~~~

To get a python dictionary representation of the config, you can run the to_dict method. i.e.
~~~
config.to_dict()
~~~
To get a json representation of the config, you may run to_json()
~~~
config.to_json()
~~~
