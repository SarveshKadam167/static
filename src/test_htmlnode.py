import unittest
from htmlnode import HTMLNode
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_single(self):
        node = HTMLNode("a", "click", props={"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_props_to_html_multiple(self):
        node = HTMLNode("a", "click", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_props_to_html_none(self):
        node = HTMLNode("p", "hello")
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode("p", "hello", props={})
        self.assertEqual(node.props_to_html(), "")

    def test_all_defaults_none(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_to_html_raises(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_repr(self):
        node = HTMLNode("p", "hello", None, {"class": "intro"})
        self.assertEqual(repr(node), "HTMLNode(p, hello, None, {'class': 'intro'})")


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "raw text")
        self.assertEqual(node.to_html(), "raw text")

    def test_leaf_to_html_bold(self):
        node = LeafNode("b", "bold text")
        self.assertEqual(node.to_html(), "<b>bold text</b>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "", {"src": "image.png", "alt": "a photo"})
        self.assertEqual(node.to_html(), '<img src="image.png" alt="a photo"></img>')

    def test_leaf_no_value_raises(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()

    def test_leaf_no_children(self):
        node = LeafNode("span", "text")
        self.assertIsNone(node.children)

    def test_leaf_repr(self):
        node = LeafNode("a", "click", {"href": "https://boot.dev"})
        self.assertEqual(repr(node), "LeafNode(a, click, {'href': 'https://boot.dev'})")


if __name__ == "__main__":
    unittest.main()
