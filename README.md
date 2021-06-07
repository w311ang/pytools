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
        curl -O https://raw.githubusercontent.com/w311ang/pytools/main/pytools.py
        curl -O https://raw.githubusercontent.com/w311ang/pytools/main/aes.py
    - name: Run
      env:
        jmail: ${{ secrets.jmail }}
      run: |
```
```python
import pytools

pytools.jmail('fromName','subject','content')
```
`requirements.txt`
```
PyCryptodome
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
  schedule:
    - cron: 0 0 * * *
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: 
        run: |
```
