from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        value: str,
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self):
        # If the leaf node has no value, it should raise a ValueError. All leaf nodes must have a value.
        # If there is no tag (e.g. it's None), the value should be returned as raw text.

        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")

        if self.tag is None:
            return self.value

        return f"<{self.tag}>{self.value}</{self.tag}>"
