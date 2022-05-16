# ELEXIS Dictionary Evaluator (EDiE)

This is a tool for evaluating the quality and availability of dictionaries
pubilshed using the [ELEXIS dictionary API](https://elexis-eu.github.io/elexis-rest/elexis.html)

For more information, please visit [https://elex.is/](https://elex.is/)

## Requirements.

Python >= 3.6

## Installation & Usage
### pip install

If the python package is hosted on a repository, you can install directly using:

```sh
pip install git+https://github.com/elexis-eu/edie.git
```
(you may need to run `pip` with root permission: `sudo pip install git+https://github.com/elexis-eu/edie.git`)

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

## Getting Started

You can run the system using the command:

    python src/main.py

## Usage

```
usage: ELEXIS Dictionary Evaluation Tool (EDiE) [-h] [--server] [-d D [D ...]] [-e E] [-m M [M ...]] [--max-entries MAX_ENTRIES] [--api-key API_KEY]

options:
  -h, --help            show this help message and exit
  --server              Start in server mode
  -d D [D ...]          Dictionaries to evaluate
  -e E                  Endpoint to query
  -m M [M ...]          List of metrics to evaluate
  --max-entries MAX_ENTRIES
                        Maximum number of entries to evaluate
  --api-key API_KEY     The API KEY to use
```

You can test an endpoint with the following command, this is limited to a single
endpoint:

```
python src/main.py -e http://lexonomy.elex.is --api-key ASK_SOMEONE_IN_THE_PROJECT \
   --max-entries=10 -d elexis-dsl-ddo --html tmp.html
```

## Author

* John P. McCrae <john@mccr.ae>
