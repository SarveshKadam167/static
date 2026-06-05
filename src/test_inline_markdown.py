import unittest
from textnode import TextNode, TextType
from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    extract_markdown_images,
    extract_markdown_links,
)


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


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode("before ![cat](https://cat.com/cat.png) after", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("before ", TextType.TEXT),
                TextNode("cat", TextType.IMAGE, "https://cat.com/cat.png"),
                TextNode(" after", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_image_at_start(self):
        node = TextNode("![img](https://x.com/img.png) trailing text", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://x.com/img.png"),
                TextNode(" trailing text", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_split_image_at_end(self):
        node = TextNode("leading text ![img](https://x.com/img.png)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("leading text ", TextType.TEXT),
                TextNode("img", TextType.IMAGE, "https://x.com/img.png"),
            ],
            split_nodes_image([node]),
        )

    def test_split_image_only(self):
        node = TextNode("![img](https://x.com/img.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("img", TextType.IMAGE, "https://x.com/img.png")],
            split_nodes_image([node]),
        )

    def test_split_image_no_images_passthrough(self):
        node = TextNode("no images here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_image_non_text_passthrough(self):
        node = TextNode("bold node", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_split_image_multiple_nodes(self):
        nodes = [
            TextNode("text ![a](https://a.com/a.png) middle", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
            TextNode("![b](https://b.com/b.png)", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("text ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://a.com/a.png"),
                TextNode(" middle", TextType.TEXT),
                TextNode("already bold", TextType.BOLD),
                TextNode("b", TextType.IMAGE, "https://b.com/b.png"),
            ],
            split_nodes_image(nodes),
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_single(self):
        node = TextNode("click [here](https://boot.dev) now", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("click ", TextType.TEXT),
                TextNode("here", TextType.LINK, "https://boot.dev"),
                TextNode(" now", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_at_start(self):
        node = TextNode("[boot dev](https://boot.dev) is great", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("boot dev", TextType.LINK, "https://boot.dev"),
                TextNode(" is great", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_at_end(self):
        node = TextNode("visit [boot dev](https://boot.dev)", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("visit ", TextType.TEXT),
                TextNode("boot dev", TextType.LINK, "https://boot.dev"),
            ],
            split_nodes_link([node]),
        )

    def test_split_link_only(self):
        node = TextNode("[boot dev](https://boot.dev)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("boot dev", TextType.LINK, "https://boot.dev")],
            split_nodes_link([node]),
        )

    def test_split_link_no_links_passthrough(self):
        node = TextNode("no links here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_link_non_text_passthrough(self):
        node = TextNode("italic node", TextType.ITALIC)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_split_link_multiple_nodes(self):
        nodes = [
            TextNode("[a](https://a.com) and text", TextType.TEXT),
            TextNode("code node", TextType.CODE),
            TextNode("plain", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("a", TextType.LINK, "https://a.com"),
                TextNode(" and text", TextType.TEXT),
                TextNode("code node", TextType.CODE),
                TextNode("plain", TextType.TEXT),
            ],
            split_nodes_link(nodes),
        )

    def test_split_link_ignores_images(self):
        node = TextNode("![img](https://img.com/i.png) [link](https://link.com)", TextType.TEXT)
        result = split_nodes_link([node])
        link_nodes = [n for n in result if n.text_type == TextType.LINK]
        self.assertEqual(len(link_nodes), 1)
        self.assertEqual(link_nodes[0].text, "link")


class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("just plain text", TextType.TEXT)],
            text_to_textnodes("just plain text"),
        )

    def test_bold_only(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)],
            text_to_textnodes("**bold**"),
        )

    def test_italic_only(self):
        self.assertListEqual(
            [TextNode("italic", TextType.ITALIC)],
            text_to_textnodes("_italic_"),
        )

    def test_code_only(self):
        self.assertListEqual(
            [TextNode("code", TextType.CODE)],
            text_to_textnodes("`code`"),
        )

    def test_image_only(self):
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://example.com/img.png")],
            text_to_textnodes("![alt](https://example.com/img.png)"),
        )

    def test_link_only(self):
        self.assertListEqual(
            [TextNode("boot dev", TextType.LINK, "https://boot.dev")],
            text_to_textnodes("[boot dev](https://boot.dev)"),
        )

    def test_multiple_bold(self):
        result = text_to_textnodes("**a** and **b**")
        self.assertListEqual(
            [
                TextNode("a", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
            ],
            result,
        )

    def test_bold_and_italic(self):
        result = text_to_textnodes("**bold** and _italic_")
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            result,
        )


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
