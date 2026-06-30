import os
from markdown_blocks import markdown_to_html_node


def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")   


def generate_pages_recursive(source_dir_path,dest_dir_path,template_path,basepath):
#generate all plages in source directory to destination directory using template
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)            
        dest_path = os.path.join(dest_dir_path, filename)

        print(f"looking from {from_path} and to: {dest_path}")
        if os.path.isfile(from_path):
            if from_path.endswith(".md"):
                html_filename = dest_path.replace(".md",".html") 
                print(f"generating page (from: {from_path}, template:{template_path},dest: {dest_path})")
                generate_page(from_path,template_path,html_filename,basepath)
            else:
                print(f"not coyping {filename} from {from_path} as it's not at markdown file")
        else:
            generate_pages_recursive(from_path, dest_path,template_path,basepath)


def generate_page(from_path, template_path, dest_path,basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}\n")
    
    with open(from_path,"r") as f:
        extracted_md = f.read()
    with open(template_path,"r") as g:
        extracted_template = g.read()

    html_node = markdown_to_html_node(extracted_md)
    html_string = html_node.to_html()
    title = extract_title(extracted_md)

    new_template = extracted_template.replace("<title>{{ Title }}</title>",f"<title>{title}</title>",1)
    new_template = new_template.replace("<article>{{ Content }}</article>",f"<article>{html_string}</article>",1)
    new_template = new_template.replace('href="/',f'href="' + basepath)
    new_template = new_template.replace('src="/',f'src="' + basepath)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path,exist_ok =True)
        
    with open(dest_path,"w") as h:
        h.write(new_template)