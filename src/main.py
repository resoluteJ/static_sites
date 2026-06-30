
import os,shutil,sys

from copystatic import copy_files_recursive
from gencontent import generate_pages_recursive

dir_path_static = "./static"
dir_path_public = "./docs"



def main():

    basepath = sys.argv[0] if sys.argv != '' else "/"

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_files_recursive(dir_path_static, dir_path_public)

    # generate_page("content/index.md","template.html","public/index.html")
    #def generate_page(from_path, template_path, dest_path):
    
    

    generate_pages_recursive("content",dir_path_public,"template.html",basepath)
    



main()



