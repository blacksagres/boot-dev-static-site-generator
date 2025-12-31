import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_calling_to_html_raises_error(self):
        node = HTMLNode("a", "https://scryfall.com")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_to_string_prints_correct_value(self):
        node = HTMLNode("a", "https://scryfall.com")
        self.assertEqual(str(node), "HTMLNode(a, https://scryfall.com)")

    def test_props_to_html_prints_correct_value(self):
        node = HTMLNode("a", "https://scryfall.com", None, {"href": "https://scryfall.com"})
        self.assertEqual(node.props_to_html(), "href=https://scryfall.com")

if __name__ == "__main__":
    unittest.main()
