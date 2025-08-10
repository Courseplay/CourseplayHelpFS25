# generate_markdown.py
# Author: Jan2903
# Date: 08/01/2025

import os
import re
import json
import shutil

# Constants for paths
CURRENT_DIR = os.getcwd()
CONFIG_FILE = os.path.join(CURRENT_DIR, "data", "config.json")
TRANSLATION_DIR = os.path.join(CURRENT_DIR, "data")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "docs")
IMAGES_DIR = os.path.join(CURRENT_DIR, "docs", "assets", "images")

# Ensure required directories exist
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(IMAGES_DIR, exist_ok=True)

def copy_image_to_docs(image_filename):
    """Copy an image from the translation_data folder to the docs/assets/images folder."""
    source_path = os.path.join(TRANSLATION_DIR, image_filename)
    destination_path = os.path.join(IMAGES_DIR, image_filename)
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_path)
    else:
        print(f"Warning: Image file '{image_filename}' not found in translation_data folder.")

def create_markdown_file(language_code, page, output_dir, file_index, is_index=False):
    """
    Create a Markdown file for a given page in a specific language.

    Args:
        language_code (str): Language code for the output file.
        page (dict): Page data containing title, paragraphs, and images.
        output_dir (str): Output directory for the Markdown file.
        file_index (int): Index number for the file name.
        is_index (bool): Whether this page should be saved as index.md.
    """
    file_name = "index.md" if is_index else f"{file_index:02d}_page_{page['raw_title']}.md"
    file_path = os.path.join(output_dir, file_name)
    
    with open(file_path, "w", encoding="utf-8") as md_file:
        # Write the page title
        md_file.write(f"# {page['title']}\n\n")
        
        # Write paragraphs
        for paragraph in page.get("paragraphs", []):
            if paragraph["title"]:
                md_file.write(f"## {paragraph['title']}\n\n")
            if paragraph["text"]:
                # Replace newlines with Markdown-compatible line breaks
                md_file.write(f"{paragraph['text'].replace('\n', '  \n')}\n\n")
            if paragraph["image"]["filename"]:
                # Copy the image to the docs/assets/images folder
                copy_image_to_docs(paragraph["image"]["filename"])
                # Adjust the image path for MkDocs
                image_path = f"../assets/images/{paragraph['image']['filename']}"
                md_file.write(f"![Image]({image_path})\n\n")

def delete_unused_images(used_images):
    """Delete all images in IMAGES_DIR that are not in the used_images set."""
    for image_file in os.listdir(IMAGES_DIR):
        if image_file not in used_images:
            image_path = os.path.join(IMAGES_DIR, image_file)
            os.remove(image_path)
            print(f"Deleted unused image: {image_file}")

def generate_site():
    """
    Main function to generate Markdown files for a multilingual site.
    Reads configuration, processes translations, and manages assets.
    """
    try:
        # Load the configuration file
        with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
            config = json.load(config_file)
        
        # Ensure config is a list and contains valid data
        if not isinstance(config, list) or not isinstance(config[0].get("pages", []), list):
            raise ValueError("Invalid config.json format. Ensure it has a list with 'pages' key.")
        
        # Load the pages from the configuration
        pages = config[0]["pages"]

        # Track used images
        used_images = set()
        
        # Loop through supported languages
        for language_file in os.listdir(TRANSLATION_DIR):
            if language_file.endswith(".json") and language_file != "config.json":
                language_code = language_file.split(".")[0]
               
                # Adjust language codes that do not match the official ISO
                mapping = {
                    "br": "pt-BR",
                    "cs": "zh",
                    "ct": "zh-TW",
                    "cz": "cs",
                    "ea": "es-BR",
                    "fc": "fr-CA",
                    "jp": "ja",
                    "kr": "ko",
                    "no": "nb"
                }
                language_code = mapping.get(language_code, language_code)

                # Create language-specific output directory
                language_output_dir = os.path.join(OUTPUT_DIR, language_code)
                os.makedirs(language_output_dir, exist_ok=True)
                
                # Load the language translation file
                with open(os.path.join(TRANSLATION_DIR, language_file), "r", encoding="utf-8") as lang_file:
                    translations = json.load(lang_file)
                    if not isinstance(translations, dict):
                        raise ValueError(f"Invalid {language_file} format. Ensure it is a JSON object.")
                
                # Generate Markdown files for each page with numbering
                for index, page in enumerate(pages, start=1):
                    # Translate titles and paragraphs
                    page_data = {
                        "raw_title": page["title"]["raw"],
                        "title": translations.get(page["title"]["raw"], page["title"]["raw"]),
                        "paragraphs": []
                    }
                    
                    for paragraph in page.get("paragraphs", []):
                        translated_paragraph = {
                            "title": translations.get(paragraph["title"]["raw"], paragraph["title"]["raw"]) if paragraph["title"].get("raw") else "",
                            "text": translations.get(paragraph["text"]["raw"], paragraph["text"]["raw"]) if paragraph["text"].get("raw") else "",
                            "image": paragraph["image"]  # Images are the same across all languages
                        }
                        if paragraph["image"].get("filename"):
                            used_images.add(paragraph["image"]["filename"])
                        page_data["paragraphs"].append(translated_paragraph)
                    
                    # Create the Markdown file
                    is_index = (index == 1)  # First page becomes index.md
                    create_markdown_file(language_code, page_data, language_output_dir, index, is_index=is_index)
        
        # Delete unused images
        delete_unused_images(used_images)
        
    except Exception as e:
        print(f"Error: {e}")
        raise

def ensure_list_rendering(file_path):
    """
    Ensures proper rendering in a Markdown file for MkDocs Material
    by adding a Markdown-compatible newline between a line ending with ':'
    and the following line if the following line contains text.
    
    Args:
        file_path (str): Path to the Markdown file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.readlines()
    
    updated_content = []
    
    for i in range(len(content) - 1):
        updated_content.append(content[i])
        # If a line ends with ':' and the next line contains text, insert a blank line
        if content[i].strip().endswith(":") and content[i + 1].strip():
            updated_content.append("\n")
    
    # Append the last line
    updated_content.append(content[-1])
    
    new_content = "".join(updated_content)
    
    with open(file_path, "r", encoding="utf-8") as file:
        original_content = file.read()
    
    if original_content != new_content:
        print(f"Updating file: {file_path}")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(new_content)
    else:
        print(f"No changes needed for: {file_path}")


def post_process_markdown_files(output_dir):
    """
    Post-processes all Markdown files in the output directory
    to ensure proper rendering in MkDocs Material.
    
    Args:
        output_dir (str): Directory containing the Markdown files.
    """
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                ensure_list_rendering(file_path)

if __name__ == "__main__":
    generate_site()
    # post_process_markdown_files(OUTPUT_DIR)
