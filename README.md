```yaml
    - name: Setup pytools
      run: |
        curl -O https://raw.githubusercontent.com/w311ang/pytools/main/pytools.py
```
```python
import pytools

pytools.update(qpass='',qfrom='')
pytools.qmail('fromName','content','subject')
