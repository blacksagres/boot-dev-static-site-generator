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
            return LeafNode(
                "img", text_node.text, {"src": text_node.url} if text_node.url else None
            )

    raise ValueError(f"{text_node.text_type} this text type is not supported.")
