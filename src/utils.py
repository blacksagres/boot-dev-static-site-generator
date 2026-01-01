from leafnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode(
                "a", text_node.text, {"href": text_node.url} if text_node.url else None
            )
        case TextType.IMAGE:
            normalized_src = text_node.url if text_node.url else ""

            return LeafNode("img", "", {"src": normalized_src, "alt": text_node.text})

    raise ValueError(f"{text_node.text_type} this text type is not supported.")


def split_nodes_delimiter(text: list[TextNode], delimiter: str, text_type: TextType):
    """
    Creates {TextNode} from string.

    ---

    Example:

    Input: `"This is text with a **bolded phrase** in the middle"`

    Output:

    ```
    [
        TextNode("This is text with a ", TextType.TEXT),
        TextNode("bolded phrase", TextType.BOLD),
        TextNode(" in the middle", TextType.TEXT),
    ]

    ```

    :param text: A list of text nodes which will be checked
    for their delimiter.
    :type text: str

    :param delimiter: The delimiter to split the text up,
    for example code: '`', bold: `**`, etc.
    :type delimiter: str

    :param text_type: The text node type which will be searched in the
    text nodes to be split.
    """

    raise NotImplementedError()
