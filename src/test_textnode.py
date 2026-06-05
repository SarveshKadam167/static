import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("click here", TextType.LINK, "https://boot.dev")
        node2 = TextNode("click here", TextType.LINK, "https://boot.dev")
        self.assertEqual(node, node2)

    def test_url_defaults_to_none(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertIsNone(node.url)

    def test_not_eq_different_text(self):
        node = TextNode("hello", TextType.BOLD)
        node2 = TextNode("world", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_type(self):
        node = TextNode("same text", TextType.BOLD)
        node2 = TextNode("same text", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_not_eq_different_url(self):
        node = TextNode("link", TextType.LINK, "https://boot.dev")
        node2 = TextNode("link", TextType.LINK, "https://example.com")
        self.assertNotEqual(node, node2)

    def test_not_eq_url_vs_none(self):
        node = TextNode("img", TextType.IMAGE, "https://example.com/img.png")
        node2 = TextNode("img", TextType.IMAGE)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
        self.assertEqual(repr(node), "TextNode(This is some anchor text, link, https://www.boot.dev)")


if __name__ == "__main__":
    unittest.main()
