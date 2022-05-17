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

There is also a docker image available to start in server mode.
    
    docker pull acdhtech/elexis-edie
    docker run -d -p 5000:5000  acdhtech/elexis-edie

## Author

* John P. McCrae <john@mccr.ae>
