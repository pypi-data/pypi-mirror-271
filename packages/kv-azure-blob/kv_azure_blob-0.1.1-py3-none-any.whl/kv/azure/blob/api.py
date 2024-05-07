from typing import TypeVar, Generic, Callable, ParamSpec, Awaitable, Never, Sequence, AsyncIterable
from functools import wraps
from dataclasses import dataclass
from haskellian import either as E, promise as P, Either, Left, Right, asyn_iter as AI
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob.aio import ContainerClient
from kv.api import KV, DBError, InvalidData, InexistentItem

A = TypeVar('A')
Ps = ParamSpec('Ps')

def azure_safe(coro: Callable[Ps, Awaitable[A]]) -> Callable[Ps, Awaitable[Either[DBError, A]]]:
  @E.do()
  @wraps(coro)
  async def wrapper(*args: Ps.args, **kwargs: Ps.kwargs) -> A:
    try:
      return await coro(*args, **kwargs)
    except ResourceNotFoundError as e:
      Left(InexistentItem(detail=e)).unsafe()
    except Exception as e:
      Left(DBError(e)).unsafe()
    return Never
  return wrapper

@dataclass
class BlobKV(KV[A], Generic[A]):

  @classmethod
  def validated(cls, Type: type[A], client: ContainerClient) -> 'BlobKV[A]':
    from pydantic import RootModel
    Model = RootModel[Type]
    return BlobKV(
      client=client,
      parse=lambda b: E.validate_json(b, Model).fmap(lambda x: x.root).mapl(InvalidData),
      dump=lambda x: Model(x).model_dump_json(exclude_none=True)
    )

  client: ContainerClient
  parse: Callable[[bytes], E.Either[InvalidData, A]] = lambda x: E.Right(x) # type: ignore
  dump: Callable[[A], bytes | str] = lambda x: x # type: ignore

  def __del__(self):
    import asyncio
    asyncio.create_task(self.client.close())

  @P.lift
  @azure_safe
  async def read(self, key: str):
    r = await self.client.download_blob(key)
    data = await r.readall()
    return self.parse(data).unsafe()

  @P.lift
  @azure_safe
  async def insert(self, key: str, value: A):
    await self.client.upload_blob(key, self.dump(value), overwrite=True)

  @P.lift
  @azure_safe
  async def has(self, key: str) -> bool:
    return await self.client.get_blob_client(key).exists()

  @P.lift
  @azure_safe
  async def delete(self, key: str):
    await self.client.delete_blob(key)
  
  @P.lift
  @azure_safe
  async def keys(self) -> Sequence[str]:
    return await AI.syncify(self.client.list_blob_names())

  @AI.lift
  async def items(self, batch_size: int | None = None) -> AsyncIterable[Either[DBError, tuple[str, A]]]:
    keys = await self.keys()
    if keys.tag == 'left':
      yield Left(keys.value)
      return
    for key in keys.value:
      item = await self.read(key)
      if item.tag == 'left':
        yield Left(item.value)
      else:
        yield Right((key, item.value))