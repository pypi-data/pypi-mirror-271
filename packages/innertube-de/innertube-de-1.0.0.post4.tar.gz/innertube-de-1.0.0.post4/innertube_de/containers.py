from dataclasses import dataclass
from typing import List, Dict, Optional
from innertube_de.endpoints import Endpoint
from innertube_de.items import Item
from innertube_de.types import ShelfType
from innertube_de.utils import get_endpoint, get_item, get_items


@dataclass(kw_only=True)
class Shelf(List[Item]):
    name: Optional[str] = None
    endpoint: Optional[Endpoint] = None

    def dump(self) -> Dict:
        return {
            "type": ShelfType.SHELF.value,
            "name": self.name,
            "endpoint": None if self.endpoint is None else self.endpoint.dump(),
            "items": [item.dump() for item in self]
        }

    def load(self, data: Dict) -> None:
        self.name = data["name"]
        self.endpoint = None if data["endpoint"] is None else get_endpoint(data["endpoint"])
        for item in get_items(data["items"]):
            self.append(item)


@dataclass(kw_only=True)
class CardShelf(Shelf):
    item: Optional[Item] = None

    def dump(self) -> Dict:
        d = super().dump()
        d.update({
            "type": ShelfType.CARD_SHELF.value,
            "item": None if self.item is None else self.item.dump(),
        })
        return d

    def load(self, data: Dict) -> None:
        super().load(data)
        self.item = get_item(data["item"])


@dataclass(kw_only=True)
class Container:
    header: Optional[Item] = None 
    contents: Optional[List[Shelf]] = None

    def dump(self) -> Dict:
        return {
            "header": None if self.header is None else self.header.dump(),
            "contents": None if self.contents is None else [shelf.dump() for shelf in self.contents]
        }

    def load(self, data: Dict) -> None:
        self.header = None if data["header"] is None else get_item(data["header"])
        if data["contents"] is None:
            return
        self.contents = []
        for shelf_data in data["contents"]:
            match shelf_data["type"]:
                case ShelfType.SHELF.value:
                    shelf = Shelf()
                case ShelfType.CARD_SHELF.value:
                    shelf = CardShelf()
                case _:
                    raise TypeError(
                        f"Invalid type: {shelf_data['type']}. "
                        f"Expected type: {ShelfType.SHELF.value} or {ShelfType.CARD_SHELF.value}"
                    )
            shelf.load(shelf_data)
            self.contents.append(shelf)
