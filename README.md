# conciliator-python
Python library for the Conciliator API

```python
import conciliator as cc
cc.connect(username, pwd, tenant)
for entity in cc.Entity.list():
  print(entity.name)
  for f in cc.File.list(entity)
    print(f.name)
```
