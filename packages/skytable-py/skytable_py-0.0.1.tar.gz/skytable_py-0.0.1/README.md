# Skytable Python Client

This is an alpha version of Skytable's official connector for Python 3.X.

## Example

```python
import asyncio
from skytable import Config

c = Config(username="root", password="password")
db = await c.connect()

# ... use the db
```
