import os
from pathlib import Path
from json import load, dump
from uuid import uuid4
from typing import Dict, List, Any, Type, Callable, Generic
from ....application.services import TenantProvider
from ....application.utilities import (
    T, QueryDomain, ExpressionParser, EntityNotFoundError)
from ....application.repositories import Repository


class JsonRepository(Repository, Generic[T]):
    def __init__(self, data_path: str, parser: ExpressionParser,
                 tenant_provider: TenantProvider,
                 collection: str, item_class: Callable[..., T]) -> None:
        self.data_path = data_path
        self.parser = parser
        self.collection = collection
        self.item_class: Callable[..., T] = item_class
        self.tenant_provider = tenant_provider

    def get(self, id: str) -> T:
        with self._file_path.open() as f:
            data = load(f)
            items = data.get(self.collection, {})
            item_dict = items.get(id)
            if not item_dict:
                raise EntityNotFoundError(
                    f"The entity with id {id} was not found.")
            return self.item_class(**item_dict)

    def add(self, item: T) -> T:
        data: Dict[str, Any] = {}
        with self._file_path.open() as f:
            data = load(f)
        setattr(item, 'id', getattr(item, 'id') or str(uuid4()))
        data[self.collection].update({getattr(item, 'id'): vars(item)})
        with self._file_path.open('w') as f:
            dump(data, f, indent=2)
        return item

    def update(self, item: T) -> bool:
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection)

        id = getattr(item, 'id')
        if id not in items_dict:
            return False

        items_dict[id] = vars(item)

        with self._file_path.open('w') as f:
            dump(data, f, indent=2)
        return True

    def search(self, domain: QueryDomain, limit=0, offset=0) -> List[T]:
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection, {})

        items = []
        limit = int(limit) if limit > 0 else 10000
        offset = int(offset) if offset > 0 else 0
        filter_function = self.parser.parse(domain)
        for item_dict in items_dict.values():
            item = self.item_class(**item_dict)

            if filter_function(item):
                items.append(item)

        items = items[:limit]
        items = items[offset:]

        return items

    def remove(self, item: T) -> bool:
        with self._file_path.open() as f:
            data = load(f)
            items_dict = data.get(self.collection)

        id = getattr(item, 'id')
        if id not in items_dict:
            return False

        del items_dict[id]

        with self._file_path.open('w') as f:
            dump(data, f, indent=2)
        return True

    @property
    def _file_path(self) -> Path:
        location = self.tenant_provider.tenant.location
        path = Path(self.data_path) / location / f"{ self.collection}.json"
        return path
