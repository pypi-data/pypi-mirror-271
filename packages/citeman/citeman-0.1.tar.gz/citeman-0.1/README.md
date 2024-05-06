![CiteMan Logo](http://cdn.jsdelivr.net/gh/dylanrussellmd/citeman/static/logo.png)

A simple command line citation manager for your academic manuscript.
---
## Installation

`citeman` can be installed using `pip` from PyPi:

```python
pip3 install citeman
```
or from GitHub

```python
pip3 install git+https://github.com/dylanrussellmd/citeman.git
```

## Usage

`citeman` is currently very early release. But even so, it still offers enough functionality to assist with basic `bibtex` bibliography management for anyone writing an academic manuscript:

- Generate `bibtex` citation for any paper by DOI (e.g., `10.1371/journal.pone.0173664`)
- Add or remove citation from `bibliography.bib`.
- Manage conflicting biliography keys.
- View all citations within `bibliography.bib`.

Start `citeman` in whichever directory you would like your `bibliography.bib` to be managed. At this time, `citeman` only allows a single bibliography file named `bibliography.bib`. If one does not exist in the working directory, it will be created. You may launch `citeman` in a directory with a `bibliography.bib` already pre-populated with entries; `citeman` will then work with these existing entries.

![citeman Example](http://cdn.jsdelivr.net/gh/dylanrussellmd/citeman/static/citeman.gif)

## Future developments

- Allow multiple `.bib` files with custom names.
- Allow search by multiple article identifiers (e.g., PMID, PMCID, ISSN, etc)
- View query history.
- Modify citations from within `citeman`.
- Preview various citation style appearances.

## Issues or ideas

Please leave your issues or ideas for future development in the [issues tracker](https://www.github.com/dylanrussellmd/citeman/issues)