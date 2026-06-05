import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_bold(self):
        node = TextNode("This is **bold** text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text", TextType.TEXT),
        ])

    def test_italic(self):
        node = TextNode("This is _italic_ text", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("This is ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT),
        ])

    def test_multiple_delimited_sections(self):
        node = TextNode("one `a` two `b` three", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("one ", TextType.TEXT),
            TextNode("a", TextType.CODE),
            TextNode(" two ", TextType.TEXT),
            TextNode("b", TextType.CODE),
            TextNode(" three", TextType.TEXT),
        ])

    def test_delimiter_at_start(self):
        node = TextNode("`code` then text", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("code", TextType.CODE),
            TextNode(" then text", TextType.TEXT),
        ])

    def test_delimiter_at_end(self):
        node = TextNode("text then `code`", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("text then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
        ])

    def test_non_text_node_passes_through(self):
        node = TextNode("already bold", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("already bold", TextType.BOLD)])

    def test_mixed_list_only_splits_text_nodes(self):
        nodes = [
            TextNode("plain `code` here", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("more `code` there", TextType.TEXT),
        ]
        result = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(result, [
            TextNode("plain ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" here", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("more ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" there", TextType.TEXT),
        ])

    def test_chained_calls(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = split_nodes_delimiter(result, "_", TextType.ITALIC)
        self.assertEqual(result, [
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ])

    def test_unclosed_delimiter_raises(self):
        node = TextNode("missing `closing delimiter", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_no_delimiter_in_text(self):
        node = TextNode("plain text no delimiters", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(result, [TextNode("plain text no delimiters", TextType.TEXT)])

    def test_empty_list(self):
        self.assertEqual(split_nodes_delimiter([], "`", TextType.CODE), [])


if __name__ == "__main__":
    unittest.main()
