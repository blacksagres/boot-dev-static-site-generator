from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(
        self,
        tag: str,
        children: list[HTMLNode],
        props: dict[str, str] | None = None,
    ) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("A parent node must always have a tag.")

        if self.children is None or len(self.children) == 0:
            raise ValueError("A parent node must always have at least one child.")

        output = [f"<{self.tag}>"]

        for child in self.children:
            output.append(child.to_html())

        output.append(f"</{self.tag}>")

        return "".join(output)
