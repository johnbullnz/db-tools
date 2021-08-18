# db-tools

## Installation

Install pipx (if not already installed):

```
pyenv global 3.8.6
python3 -m pip install --user pipx
python3 -m pipx ensurepath
```

Install directly from Github:

```
 pipx install git+https://github.com/johnbullnz/db-tools.git
```

Or clone repo and install using pipx:

```
cd /apps
clone git@github.com:johnbullnz/db-tools.git
cd ~/repositories/db-tools
pipx install .
```

**Note, you must have a .db-config.ini file (see repo)**

## Usage

```
db-tools --help
```

```
Usage: db-tools.py [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Commands:
  dump       Dump database DATABASE to a sql file.
  duplicate  Generate a duplicate copy of a database with '_copy' appended...
  restore    Restore database from backup file.
```