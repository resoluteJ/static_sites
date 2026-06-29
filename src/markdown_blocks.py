from enum import Enum

from htmlnode import HTMLNode,ParentNode
from textnode import text_node_to_html_node, TextNode, TextType
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    OLIST = "ordered_list"
    ULIST = "unordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = markdown.split("\n\n")
    filtered_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered_blocks.append(block)
    return filtered_blocks


def block_to_block_type(block: str) -> BlockType:
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.ULIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH



def heading_symbol_counter(heading_block:str)-> int:
    if heading_block.startswith('######'):
        return 6
    if heading_block.startswith('#####'):
        return 5
    if heading_block.startswith('####'):
        return 4
    if heading_block.startswith('###'):
        return 3
    if heading_block.startswith('##'):
        return 2
    if heading_block.startswith('#'):
        return 1
    else:
        return 0



def markdown_to_html_node(markdown:str) -> HTMLNode:
    #split markdown into blocks

    blocks:list[str] = markdown_to_blocks(markdown) #takes a string of markdown text and returns a list of blocks of markdown
    block_htmls: list[HTMLNode] = []
    

    for b in blocks: #loop thru the blocks
        bt = block_to_block_type(b)#determing the type of block
        
        #Based on the type of block, create a new HTMLNode with the proper data
        if bt == BlockType.HEADING:
            #HTML node is (tag,value,children,props) but instead ParentNode has no value and LeafNode has no children
            h_number = heading_symbol_counter(b)
            stipped_text = b.lstrip('#')
            stipped_text = stipped_text.strip()
            
            child_nodes = text_to_children(stipped_text)
            block_htmls.append(ParentNode(f"h{h_number}",child_nodes))
            

        if bt == BlockType.CODE:
            stipped_text = b.removeprefix('```\n')
            stipped_text = stipped_text.removesuffix('```')
            
            code_text_node = TextNode(stipped_text,TextType.CODE)
            code_html_node = text_node_to_html_node(code_text_node)
            block_htmls.append(ParentNode("pre",[code_html_node]))
            
        if bt == BlockType.QUOTE:
            stipped_text = b.lstrip('>')
            stipped_text = stipped_text.strip()
            child_nodes = text_to_children(stipped_text)
            block_htmls.append(ParentNode("blockquote",child_nodes))


        if bt == BlockType.OLIST:

            child_nodes = []
            li_children = []
            li_blocks = b.split("\n")
            list_index = 1
            for l in li_blocks:
                stripped_text = l.removeprefix(f"{list_index}. ")
                list_index += 1
                
                child_nodes = text_to_children(stripped_text)
                li_children.append(ParentNode("li",child_nodes))
            block_htmls.append(ParentNode("ol",li_children))
                
        if bt == BlockType.ULIST:
            child_nodes = []
            li_children = []
            li_blocks = b.split("\n")
            for l in li_blocks:
                stripped_text = l.removeprefix("- ")
                
                child_nodes = text_to_children(stripped_text)
                li_children.append(ParentNode("li",child_nodes))
            block_htmls.append(ParentNode("ul",li_children))




        if bt == BlockType.PARAGRAPH:
            stipped_text = b.replace("\n"," ")
            child_nodes = text_to_children(stipped_text)
            block_htmls.append(ParentNode("p",child_nodes)) 

    master_node = ParentNode("div",block_htmls)
    return master_node



def text_to_children(text:str) ->list[HTMLNode]: #make sure the text passed in is stripped of the markdown block stuff already
    text_nodes:list[TextNode] = text_to_textnodes(text)
    #remember TextNodes have (text, texttype, url[optional])
    html_nodes = []
    for t in text_nodes:
        html_nodes.append(text_node_to_html_node(t))
    return html_nodes
