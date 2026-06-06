import unittest
from generate_page import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_simple_h1(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Spaced Title   "), "Spaced Title")

    def test_h1_among_other_content(self):
        md = "Some text\n\n# The Real Title\n\nMore text"
        self.assertEqual(extract_title(md), "The Real Title")

    def test_h1_not_first_line(self):
        md = "## Not this one\n# This one"
        self.assertEqual(extract_title(md), "This one")

    def test_ignores_h2_and_below(self):
        md = "## Section\n### Subsection"
        with self.assertRaises(ValueError):
            extract_title(md)

    def test_no_header_raises(self):
        with self.assertRaises(ValueError):
            extract_title("Just a paragraph with no headings.")

    def test_empty_string_raises(self):
        with self.assertRaises(ValueError):
            extract_title("")

    def test_hash_without_space_not_h1(self):
        with self.assertRaises(ValueError):
            extract_title("#NoSpace")


if __name__ == "__main__":
    unittest.main()
