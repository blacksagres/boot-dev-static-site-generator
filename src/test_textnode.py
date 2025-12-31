import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_non_eq_based_on_text(self):
        node = TextNode("This is a text no-node!", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq_based_on_type(self):
        node = TextNode("This is a text node", TextType.IMAGE)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_non_eq_based_on_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://scryfall.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://mtggoldfish.com/")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()
