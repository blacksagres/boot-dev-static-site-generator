import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_several_nodes(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )

        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_to_html_without_tag_should_raise(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                None,  # type: ignore[arg-type]
                [
                    LeafNode("b", "Bold text"),
                ],
            )

            node.to_html()

    def test_to_html_without_children_should_raise(self):
        with self.assertRaises(ValueError):
            node = ParentNode(
                "p",
                [],
            )

            node.to_html()


if __name__ == "__main__":
    unittest.main()
