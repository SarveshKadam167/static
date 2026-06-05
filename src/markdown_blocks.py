import re
from enum import Enum

from parentnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    lines = block.split("\n")

    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE

    if all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST

    if all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH


def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]


def paragraph_to_html_node(block):
    text = " ".join(block.split("\n"))
    return ParentNode("p", text_to_children(text))


def heading_to_html_node(block):
    level = len(block) - len(block.lstrip("#"))
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))


def code_to_html_node(block):
    content = block[block.index("\n") + 1:-3]
    raw = text_node_to_html_node(TextNode(content, TextType.TEXT))
    return ParentNode("pre", [ParentNode("code", [raw])])


def quote_to_html_node(block):
    lines = block.split("\n")
    stripped = []
    for line in lines:
        if line.startswith("> "):
            stripped.append(line[2:])
        elif line.startswith(">"):
            stripped.append(line[1:])
        else:
            stripped.append(line)
    return ParentNode("blockquote", text_to_children(" ".join(stripped)))


def unordered_list_to_html_node(block):
    items = [ParentNode("li", text_to_children(line[2:])) for line in block.split("\n")]
    return ParentNode("ul", items)


def ordered_list_to_html_node(block):
    items = [
        ParentNode("li", text_to_children(line.split(". ", 1)[1]))
        for line in block.split("\n")
    ]
    return ParentNode("ol", items)


def block_to_html_node(block):
    match block_to_block_type(block):
        case BlockType.PARAGRAPH:
            return paragraph_to_html_node(block)
        case BlockType.HEADING:
            return heading_to_html_node(block)
        case BlockType.CODE:
            return code_to_html_node(block)
        case BlockType.QUOTE:
            return quote_to_html_node(block)
        case BlockType.UNORDERED_LIST:
            return unordered_list_to_html_node(block)
        case BlockType.ORDERED_LIST:
            return ordered_list_to_html_node(block)
        case _:
            raise ValueError(f"Unknown block type: {block_to_block_type(block)}")


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return ParentNode("div", [block_to_html_node(b) for b in blocks])


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]
