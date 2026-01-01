import unittest

from textnode import TextNode, TextType
from utils import text_node_to_html_node


class TestUtils(unittest.TestCase):

    # text_node_to_html_node

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode(
            "This is a text node", TextType.IMAGE, url="https://scryfall.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://scryfall.com", "alt": node.text}
        )

    # split_nodes_delimiter

    def test_split_nodes_delimiter_raises_if_delimiter_not_found(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "impossible_delimiter", TextType.CODE)

