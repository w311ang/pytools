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
      - name: Set proxy
        uses: w311ang/setproxy@main
        with:
          config: ${{ secrets.ss_config }}
          password: ${{ secrets.frp_auth }}
          redirect: ${{ secrets.frp_redirect }}
      - name: Run
        env:
          : ${{ secrets. }}
        uses: nick-invision/retry@v2
        with:
          timeout_minutes: 10
          max_attempts: 5
          command: |
            proxychains python -u 
          on_retry_command: sudo systemctl restart shadowsocks-libev-local@client; sleep 5s
      - uses: gautamkrishnar/keepalive-workflow@master
```

## main.yml (pure)
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

## main.yml (with cache)
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
      - name: Set proxy
        uses: w311ang/setproxy@main
        with:
          config: ${{ secrets.ss_config }}
          password: ${{ secrets.frp_auth }}
          redirect: ${{ secrets.frp_redirect }}
      - name: Cache
        uses: actions/cache@v2
        with:
          path: |
            ./
          key: build-${{ github.run_id }}
          restore-keys: |
            build-
      - name: Run
        env:
          on: ${{ github.event_name }}
          jmail: ${{ secrets.jmail_password }}
          : ${{ secrets. }}
        uses: nick-invision/retry@v2
        with:
          timeout_minutes: 10
          max_attempts: 5
          command: |
            proxychains python -u 
          on_retry_command: sudo systemctl restart shadowsocks-libev-local@client; sleep 5s
      - uses: gautamkrishnar/keepalive-workflow@master
```
