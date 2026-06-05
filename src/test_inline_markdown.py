import unittest
from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


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


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_single_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_multiple_images(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")],
            matches,
        )

    def test_extract_images_no_match(self):
        self.assertListEqual([], extract_markdown_images("no images here"))

    def test_extract_images_ignores_plain_links(self):
        text = "[not an image](https://example.com)"
        self.assertListEqual([], extract_markdown_images(text))

    def test_extract_images_empty_alt(self):
        matches = extract_markdown_images("![](https://example.com/img.png)")
        self.assertListEqual([("", "https://example.com/img.png")], matches)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_single_link(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_multiple_links(self):
        text = "[to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")],
            matches,
        )

    def test_extract_links_no_match(self):
        self.assertListEqual([], extract_markdown_links("no links here"))

    def test_extract_links_ignores_images(self):
        text = "![alt text](https://example.com/img.png)"
        self.assertListEqual([], extract_markdown_links(text))

    def test_extract_links_mixed_with_images(self):
        text = "![img](https://img.url) and [link](https://link.url)"
        matches = extract_markdown_links(text)
        self.assertListEqual([("link", "https://link.url")], matches)

    def test_extract_links_empty_anchor(self):
        matches = extract_markdown_links("[](https://example.com)")
        self.assertListEqual([("", "https://example.com")], matches)


if __name__ == "__main__":
    unittest.main()
