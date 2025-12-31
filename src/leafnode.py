from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)
