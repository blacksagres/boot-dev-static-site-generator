from leafnode import LeafNode
from textnode import TextNode, TextType
import re


def text_to_text_nodes(text: str):
    result: list[TextNode] = []

    initial_text_node = TextNode(text, TextType.TEXT)

    result = split_nodes_delimiter([initial_text_node], "**", TextType.BOLD)

    result = split_nodes_delimiter(result, "_", TextType.ITALIC)

    result = split_nodes_delimiter(result, "`", TextType.CODE)

    result = split_nodes_image(result)
    result = split_nodes_link(result)

    return result


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
) -> list[TextNode]:
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

    result: list[TextNode] = []

    for node in old_nodes:
        if node.text.count(delimiter) % 2 > 0:
            raise ValueError("Found an open delimiter in the text, invalid markdown.")

        # odd indexed items are the ones that contain text between delimiters.

        split_node_text = node.text.split(delimiter)

        for child_node_text in split_node_text:
            between_delimiter = split_node_text.index(child_node_text) % 2 == 1

            text_node_to_append = TextNode(
                child_node_text, text_type if between_delimiter else node.text_type
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

    # if len(markdown_image_descriptions) != len(markdown_image_urls):
    #     raise IndexError(
    #         "There is a malformed markdown image url in this string, please fix it."
    #     )

    result = []

    for index in range(len(markdown_image_descriptions)):
        result.append((markdown_image_descriptions[index], markdown_image_urls[index]))

    return result


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """
    Checks a string for markdown links and extracts those
    into a tuple.

    :param text: The string to be checked
    :type text: str
    """

    markdown_link_descriptions = re.findall(r"\[(.*?)\]", text)
    markdown_link_urls = re.findall(r"\((.*?)\)", text)

    if len(markdown_link_descriptions) != len(markdown_link_urls):
        raise IndexError(
            "There is a malformed markdown link url in this string, please fix it."
        )

    result = []

    for index in range(len(markdown_link_descriptions)):
        result.append((markdown_link_descriptions[index], markdown_link_urls[index]))

    return result


def split_nodes_image(old_nodes: list[TextNode]):
    result: list[TextNode] = []

    image_link_delimiter = "!["

    for text_node in old_nodes:
        current_text = text_node.text

        if image_link_delimiter in current_text:
            markdown_image_links = extract_markdown_images(current_text)

            for alt, url in markdown_image_links:
                image_md = f"![{alt}]({url})"

                """
                By splitting this just once we are absolutely sure of where to 
                insert the link text between the text.

                If we end up with an empty `before`, this means that 
                the link was split in the beginning of the string.
                """
                before, after = current_text.split(image_md, 1)

                if before:
                    result.append(TextNode(before, TextType.TEXT))

                result.append(TextNode(alt, TextType.IMAGE, url))

                current_text = after

            if current_text:
                result.append(TextNode(current_text, TextType.TEXT))

        else:
            result.append(text_node)

    return result


def split_nodes_link(old_nodes: list[TextNode]):
    result: list[TextNode] = []

    image_link_delimiter = "["

    for text_node in old_nodes:
        current_text = text_node.text

        if image_link_delimiter in current_text:
            markdown_image_links = extract_markdown_links(current_text)

            for alt, url in markdown_image_links:
                image_md = f"[{alt}]({url})"

                """
                By splitting this just once we are absolutely sure of where to 
                insert the link text between the text.

                If we end up with an empty `before`, this means that 
                the link was split in the beginning of the string.
                """
                before, after = current_text.split(image_md, 1)

                if before:
                    result.append(TextNode(before, TextType.TEXT))

                result.append(TextNode(alt, TextType.LINK, url))

                current_text = after

            if current_text:
                result.append(TextNode(current_text, TextType.TEXT))

        else:
            result.append(text_node)

    return result
