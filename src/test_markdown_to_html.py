import unittest
from markdown_blocks import markdown_to_html_node


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "# Big Heading"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h1>Big Heading</h1></div>")

    def test_heading_levels(self):
        md = "## Level Two\n\n### Level Three"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h2>Level Two</h2><h3>Level Three</h3></div>")

    def test_heading_with_inline(self):
        md = "## A **bold** heading"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h2>A <b>bold</b> heading</h2></div>")

    def test_quote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><blockquote>This is a quote</blockquote></div>")

    def test_quote_with_inline(self):
        md = "> A quote with **bold** text"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><blockquote>A quote with <b>bold</b> text</blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- first\n- second\n- third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>first</li><li>second</li><li>third</li></ul></div>",
        )

    def test_unordered_list_with_inline(self):
        md = "- **bold item**\n- _italic item_"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li><b>bold item</b></li><li><i>italic item</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. one\n2. two\n3. three"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>one</li><li>two</li><li>three</li></ol></div>",
        )

    def test_ordered_list_with_inline(self):
        md = "1. `code item`\n2. **bold item**"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li><code>code item</code></li><li><b>bold item</b></li></ol></div>",
        )

    def test_mixed_blocks(self):
        md = "# Title\n\nA paragraph.\n\n- item one\n- item two"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><h1>Title</h1><p>A paragraph.</p><ul><li>item one</li><li>item two</li></ul></div>",
        )

    def test_link_in_paragraph(self):
        md = "Visit [boot dev](https://boot.dev) today."
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>Visit <a href="https://boot.dev">boot dev</a> today.</p></div>',
        )

    def test_image_in_paragraph(self):
        md = "Look: ![cat](https://cat.com/cat.png)"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            '<div><p>Look: <img src="https://cat.com/cat.png" alt="cat"></img></p></div>',
        )

    def test_code_does_not_parse_inline(self):
        md = "```\n**not bold** and _not italic_\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("**not bold**", html)
        self.assertIn("_not italic_", html)
        self.assertNotIn("<b>", html)
        self.assertNotIn("<i>", html)


if __name__ == "__main__":
    unittest.main()
