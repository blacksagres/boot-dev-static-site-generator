class HTMLNode: 
    def __init__(self, 
                 tag: str | None = None, 
                 value: str | None = None, 
                 children: list["HTMLNode"] | None = None,
                 props: dict | None = None) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props