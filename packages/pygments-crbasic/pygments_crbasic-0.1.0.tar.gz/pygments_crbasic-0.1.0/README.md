[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/jkittner/pygments-crbasic/main.svg)](https://results.pre-commit.ci/latest/github/jkittner/pygments-crbasic/main)

# pygments-crbasic

A `pygments` lexer for the [CRBasic Programming Language](https://help.campbellsci.com/crbasic/landing/Content/crbasic-help-home.htm) by [Campbell Scientific](https://www.campbellsci.com/).

## Installation

```bash
pip install pygments-crbasic
```

### Usage

### pygments

This can basically used with everything that uses `pygments`.

### sphinx

This can be used in [sphinx](https://www.sphinx-doc.org/en/master/)/`rst` code blocks:

```rst
.. code-block:: crbasic

    Public PanelT, TCTemp
```

## Disclaimer

This is not an official product and not associated with Campbell Scientific Ltd. in any way.

## Credits

The package is based on the TextMate Syntax regexes as provided here:

https://github.com/daiwalkr/cr-basic-ms-vscode/blob/aa03907c52f98d2ee360ef2bf31df1d6b490c6f1/syntaxes/cr-basic.tmLanguage.json
