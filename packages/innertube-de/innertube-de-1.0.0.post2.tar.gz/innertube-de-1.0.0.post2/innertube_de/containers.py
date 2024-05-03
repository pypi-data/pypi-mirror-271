from typing import List, Dict, Optional
from innertube_de.endpoints import Endpoint
from innertube_de.items import Item
from innertube_de.types import ShelfType
from innertube_de.utils import get_endpoint, get_item, get_items


class Shelf(List[Item]):
    """ Class for containing Item objects. """
    def __init__(
            self, 
            name: Optional[str] = None, 
            endpoint: Optional[Endpoint] = None, 
            *args, 
            **kwargs
    ) -> None:
        """
        Initialize this object with the specified parameters.
        @param name: The name of this shelf.
        @param endpoint: The Endpoint object associated with this shelf.
        @param args: The positional arguments to pass to the constructor of the list class.
        @param kwargs: The key arguments to pass to the constructor of the list class.
        """
        super().__init__(*args, **kwargs)
        self.name = name
        self.endpoint = endpoint

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return (
                self.name == __value.name
                and self.endpoint == __value.endpoint
                and super().__eq__(__value)
            )
        else:
            return False

    def __repr__(self) -> str:
        return (
            "Shelf{"
            f"name={self.name}, "
            f"endpoint={self.endpoint}, "
            f"items={super().__repr__()}"
            "}"
        )

    def dump(self) -> Dict:
        """
        Serialize this object.
        @return: A dictionary that describes the state of this object.
        """
        return {
            "type": ShelfType.SHELF.value,
            "name": self.name,
            "endpoint": None if self.endpoint is None else self.endpoint.dump(),
            "items": [item.dump() for item in self]
        }

    def load(self, data: Dict) -> None:
        """
        Deserialize this object with the specified dictionary.
        @param data: The dictionary containing the data.
        @return: None
        """
        self.name = data["name"]
        self.endpoint = None if data["endpoint"] is None else get_endpoint(data["endpoint"])
        for item in get_items(data["items"]):
            self.append(item)


class CardShelf(Shelf):
    def __init__(self, item: Optional[Item] = None, *args, **kwargs) -> None:
        """
        Initialize this object with the specified parameters.
        @param item:
        @param args: The positional arguments to pass to the constructor of the Shelf class.
        @param kwargs: The key arguments to pass to the constructor of the Shelf class.
        """
        super().__init__(*args, **kwargs)
        self.item = item

    def __eq__(self, __value: object) -> bool:
        return super().__eq__(__value) and self.item == __value.item

    def __repr__(self) -> str:
        return "Card" f"{super().__repr__()[:-1]}, item={self.item}" "}"

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


class Container:
    def __init__(self, header: Optional[Item] = None, contents: Optional[List[Shelf]] = None) -> None:
        """
        Initialize this object with the specified parameters.
        @param header: An Item object.
        @param contents: A list of Shelf objects.
        """
        self.header = header
        if contents is None:
            contents = []
        self.contents = contents

    def __eq__(self, __value: object) -> bool:
        if isinstance(__value, type(self)):
            return self.header == __value.header and self.contents == __value.contents
        else:
            return False

    def __repr__(self) -> str:
        return "Container{" f"header={self.header}, contents={self.contents}" "}"

    def dump(self) -> Dict:
        """
        Serialize this object.
        @return: A dictionary that describes the state of this object.
        """
        return {
            "header": None if self.header is None else self.header.dump(),
            "contents": None if self.contents is None else [shelf.dump() for shelf in self.contents]
        }

    def load(self, data: Dict) -> None:
        """
        Deserialize this object with the specified dictionary.
        @param data: The dictionary containing the data.
        @return: None
        """
        self.header = None if data["header"] is None else get_item(data["header"])
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
