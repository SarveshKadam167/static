import unittest
from markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType


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


class TestBlockToBlockType(unittest.TestCase):
    # headings
    def test_heading_h1(self):
        self.assertEqual(block_to_block_type("# Heading"), BlockType.HEADING)

    def test_heading_h3(self):
        self.assertEqual(block_to_block_type("### Heading"), BlockType.HEADING)

    def test_heading_h6(self):
        self.assertEqual(block_to_block_type("###### Heading"), BlockType.HEADING)

    def test_heading_too_many_hashes(self):
        self.assertEqual(block_to_block_type("####### Not a heading"), BlockType.PARAGRAPH)

    def test_heading_no_space(self):
        self.assertEqual(block_to_block_type("#NoSpace"), BlockType.PARAGRAPH)

    # code
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\nsome code\n```"), BlockType.CODE)

    def test_code_block_with_language(self):
        self.assertEqual(block_to_block_type("```python\nprint('hi')\n```"), BlockType.CODE)

    def test_code_block_unclosed(self):
        self.assertEqual(block_to_block_type("```\nsome code"), BlockType.PARAGRAPH)

    # quote
    def test_quote_single_line(self):
        self.assertEqual(block_to_block_type(">quote text"), BlockType.QUOTE)

    def test_quote_with_space(self):
        self.assertEqual(block_to_block_type("> quote text"), BlockType.QUOTE)

    def test_quote_multiline(self):
        self.assertEqual(block_to_block_type("> line one\n> line two\n> line three"), BlockType.QUOTE)

    def test_quote_missing_marker_on_one_line(self):
        self.assertEqual(block_to_block_type("> line one\nline two"), BlockType.PARAGRAPH)

    # unordered list
    def test_unordered_list_single(self):
        self.assertEqual(block_to_block_type("- item"), BlockType.UNORDERED_LIST)

    def test_unordered_list_multiple(self):
        self.assertEqual(block_to_block_type("- first\n- second\n- third"), BlockType.UNORDERED_LIST)

    def test_unordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("-item"), BlockType.PARAGRAPH)

    def test_unordered_list_mixed_markers(self):
        self.assertEqual(block_to_block_type("- first\n* second"), BlockType.PARAGRAPH)

    # ordered list
    def test_ordered_list_single(self):
        self.assertEqual(block_to_block_type("1. item"), BlockType.ORDERED_LIST)

    def test_ordered_list_multiple(self):
        self.assertEqual(block_to_block_type("1. first\n2. second\n3. third"), BlockType.ORDERED_LIST)

    def test_ordered_list_wrong_start(self):
        self.assertEqual(block_to_block_type("2. first\n3. second"), BlockType.PARAGRAPH)

    def test_ordered_list_skipped_number(self):
        self.assertEqual(block_to_block_type("1. first\n3. third"), BlockType.PARAGRAPH)

    def test_ordered_list_missing_space(self):
        self.assertEqual(block_to_block_type("1.item\n2.item"), BlockType.PARAGRAPH)

    # paragraph
    def test_paragraph(self):
        self.assertEqual(block_to_block_type("Just a normal paragraph."), BlockType.PARAGRAPH)

    def test_paragraph_multiline(self):
        self.assertEqual(block_to_block_type("line one\nline two"), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
