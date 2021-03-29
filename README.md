```yaml
    - name: Checkout pytools
      uses: actions/checkout@v2
      with:
        repository: 'w311ang/pytools'
        path: './pytools'
    - name: Setup pytools
      run: |
        cp ./pytools/pytools.py .
```
