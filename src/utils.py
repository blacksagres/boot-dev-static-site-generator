from leafnode import LeafNode
from textnode import TextNode, TextType
import re


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


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
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

    :param old_nodes: A list of text nodes which will be checked
    for their delimiter.
    :type old_nodes: str

    :param delimiter: The delimiter to split the text up,
    for example code: '`', bold: `**`, etc.
    :type delimiter: str

    :param text_type: The text node type which will be searched in the
    text nodes to be split.
    """

    delimiter_in_node = [node for node in old_nodes if delimiter in node.text]

    if not delimiter_in_node:
        raise ValueError("The delimiter indicated was not found in the list of nodes.")

    result = []

    for node in old_nodes:
        if node.text.count(delimiter) % 2 > 0:
            raise ValueError("Found an open delimiter in the text, invalid markdown.")

        # odd indexed items are the ones that contain text between delimiters.

        split_node_text = node.text.split(delimiter)

        for child_node_text in split_node_text:
            between_delimiter = split_node_text.index(child_node_text) % 2 == 1

            text_node_to_append = TextNode(
                child_node_text, text_type if between_delimiter else TextType.TEXT
            )

            result.append(text_node_to_append)

    # find first index of delimiter
    # find last index of delimiter
    # split on delimiter
    # text in between becomes the new node

    return result


def extract_markdown_images(text: str):
    """
    Checks a string for markdown image links and extracts those
    into a tuple.

    :param text: The string to be checked
    :type text: str
    """

    markdown_image_descriptions = re.findall(r"\!\[(.*?)\]", text)
    markdown_image_urls = re.findall(r"\((.*?)\)", text)

    if len(markdown_image_descriptions) != len(markdown_image_urls):
        raise IndexError(
            "There is a malformed markdown image url in this string, please fix it."
        )

    result = []

    for index in range(len(markdown_image_descriptions)):
        result.append((markdown_image_descriptions[index], markdown_image_urls[index]))

    return result
