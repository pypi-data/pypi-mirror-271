# loadspinner
![Pepy Total Downlods](https://img.shields.io/pepy/dt/loadspinner)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/loadspinner)
![GitHub repo size](https://img.shields.io/github/repo-size/xyzpw/loadspinner)

A CLI based loading spinner.

> [!WARNING]
> Code is subject to change

## Prerequisites
- Terminal that accepts ANSI codes

## Usage
Creating and using a spinner:
```python
import loadspinner
spinner = loadspinner.Spinner(spinner_type="classic")
spinner.start() #starts the spinner
spinner.stop() #stops the spinner
```
Optionally, you can set a time limit for the spinner, e.g. `spinner.start(5) #5 seconds`.
