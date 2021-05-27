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

Then import the package:
```python
import openapi_client
```

### Setuptools

Install via [Setuptools](http://pypi.python.org/pypi/setuptools).

```sh
python setup.py install --user
```
(or `sudo python setup.py install` to install the package for all users)

## Getting Started

You can run the system using the command:

    python src/main.py

## Author

* John P. McCrae <john@mccr.ae>
