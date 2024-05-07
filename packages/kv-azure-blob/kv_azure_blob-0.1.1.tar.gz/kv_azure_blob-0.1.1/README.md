# Key-Value: Azure Blob

> Implementation of the `KV[T]` async Key-Value ABC, over Azure Blob Storage

([`kv-api`]((https://pypi.org/project/kv-api/)))

```bash
pip install kv-azure-blob
```

## Usage

### Raw

```python
from azure.storage.blob.aio import ContainerClient
from kv.azure.blob import BlobKV

cc: ContainerClient = ...
kv = BlobKV[bytes](cc)
await kv.insert('img1', b'...')
await kv.read('img2')
await kv.keys()
# etc.
```

### Pydantic-validated

```python
from dataclasses import dataclass

@dataclass
class User:
  username: str
  email: str

cc: ContainerClient = ...
kv = BlobKV.validated(User, cc)
await kv.insert('user1', User(username='user1', email='...'))
# etc.
```