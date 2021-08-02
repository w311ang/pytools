## qmail
```yaml
    - name: Setup pytools
      run: |
        curl -O https://raw.githubusercontent.com/w311ang/pytools/main/pytools.py
```
```python
import pytools

pytools.update(qpass='',qfrom='')
pytools.qmail('fromName','content','subject')
```

## jmail
```yaml
    - name: Setup pytools
      run: |
        pip install --upgrade git+https://github.com/w311ang/pytools.git@package
    - name: Run
      env:
        jmail: ${{ secrets.jmail_password }}
      run: |
```
```python
from pytools import pytools

pytools.jmail('fromName','subject','content')
```

## echo
```yaml
    - name: Setup pytools
      run: |
        curl -O https://raw.githubusercontent.com/w311ang/pytools/main/pytools.py
```
```python
from pytools import echo as print
```

## main.yml
```yaml
name: 

on:
  push:
    paths-ignore:
      - 'README.md'
  schedule:
    - cron: 0 12 * * *
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python 3.9
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
      - name: Run
        run: |
          python -u 
```
