import unittest
from markdown_blocks import markdown_to_blocks


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_single_block(self):
        md = "Just one paragraph with no double newlines."
        self.assertEqual(markdown_to_blocks(md), ["Just one paragraph with no double newlines."])

    def test_strips_leading_trailing_whitespace(self):
        md = "   first block   \n\n   second block   "
        self.assertEqual(markdown_to_blocks(md), ["first block", "second block"])

    def test_removes_empty_blocks(self):
        md = "block one\n\n\n\n\n\nblock two"
        self.assertEqual(markdown_to_blocks(md), ["block one", "block two"])

    def test_empty_string(self):
        self.assertEqual(markdown_to_blocks(""), [])

    def test_only_whitespace(self):
        self.assertEqual(markdown_to_blocks("   \n\n   \n\n   "), [])

    def test_heading_and_paragraph(self):
        md = "# My Heading\n\nSome paragraph text."
        self.assertEqual(markdown_to_blocks(md), ["# My Heading", "Some paragraph text."])

    def test_three_blocks(self):
        md = "# Heading\n\nA paragraph.\n\n- item one\n- item two"
        self.assertEqual(
            markdown_to_blocks(md),
            ["# Heading", "A paragraph.", "- item one\n- item two"],
        )


if __name__ == "__main__":
    unittest.main()
