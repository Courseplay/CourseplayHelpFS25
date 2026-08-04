#!/usr/bin/env python3
"""
generate_from_xml.py

Directly parses Courseplay FS25 XML configuration and translation files,
crops DDS textures to PNG, and generates multilingual Markdown documentation for MkDocs.
"""

import os
import re
import shutil
import subprocess
import argparse
import xml.etree.ElementTree as ET
from PIL import Image as PIL_Image

CURRENT_DIR = os.getcwd()
GAME_REPO_DIR = os.path.join(CURRENT_DIR, "game_repo")
CONFIG_FILE = os.path.join(GAME_REPO_DIR, "config", "HelpMenu.xml")
TRANSLATIONS_DIR = os.path.join(GAME_REPO_DIR, "translations")
OUTPUT_DIR = os.path.join(CURRENT_DIR, "docs")
IMAGES_DIR = os.path.join(OUTPUT_DIR, "assets", "images")

MAPPING = {
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

def setup_game_repo(force_update=False):
    """Clones or updates the Courseplay_FS25 repository using shallow sparse-checkout."""
    if not os.path.exists(GAME_REPO_DIR) or force_update:
        print("Setting up shallow sparse-checkout of Courseplay FS25...")
        if os.path.exists(GAME_REPO_DIR):
            shutil.rmtree(GAME_REPO_DIR)
        os.makedirs(GAME_REPO_DIR, exist_ok=True)
        cmd = (
            "git clone --filter=blob:none --no-checkout --depth 1 https://github.com/Courseplay/Courseplay_FS25.git game_repo && "
            "git -C game_repo sparse-checkout set config/HelpMenu.xml translations img && "
            "git -C game_repo checkout"
        )
        subprocess.run(cmd, shell=True, check=True)
        print("Game repository cloned successfully.")
    else:
        print("Using existing local game_repo directory. (Use --update to force refresh)")

def filter_xml_text(string):
    """Replaces newlines inside XML attribute values with '&#xA;' to preserve linebreaks during parsing."""
    string = re.sub(r"<\?.+\?>", "", string)  # Removes the xml declaration
    regex = r'((?<=((=")))[^"]+(?<!"))'
    matches = list(re.finditer(regex, string))
    for _, match in reversed(list(enumerate(matches, start=1))):
        s = re.sub(r"\r\n|\n\r|\n|\r|&#10;", "&#xA;", match.group())
        string = string[:match.start()] + s + string[match.end():]
    return string

def load_translations():
    """Loads all language translation XML files from the game repo into dictionaries."""
    translations = {}
    if not os.path.exists(TRANSLATIONS_DIR):
        raise FileNotFoundError(f"Translations directory not found: {TRANSLATIONS_DIR}")

    for filename in os.listdir(TRANSLATIONS_DIR):
        if filename.startswith("translation_") and filename.endswith(".xml"):
            lang_code_raw = filename.split("_")[1][:-4]
            lang_code = MAPPING.get(lang_code_raw, lang_code_raw)
            file_path = os.path.join(TRANSLATIONS_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            content_filtered = filter_xml_text(content)
            try:
                root = ET.fromstring(content_filtered)
            except Exception as e:
                print(f"Error parsing {filename}: {e}")
                continue
            
            translations[lang_code] = {}
            for entry in root.iter('text'):
                name = entry.attrib.get('name')
                val = entry.attrib.get('text', "")
                if name:
                    translations[lang_code][name] = val
    return translations

def process_image(image_elem, used_images):
    """Extracts image metadata, converts DDS texture to cropped PNG, and returns markdown filename."""
    raw_filename = image_elem.attrib.get('filename')
    if not raw_filename:
        return None
    
    uvs_str = image_elem.attrib.get('uvs', '')
    uvs = [int(val) for val in uvs_str.replace("px", "").split()]
    if len(uvs) != 4:
        print(f"Warning: Invalid UV coordinates for {raw_filename}: {uvs_str}")
        return None

    base_name = os.path.splitext(os.path.basename(raw_filename))[0]
    cropped_filename = f"{base_name}_{uvs[0]}_{uvs[1]}_{uvs[2]}_{uvs[3]}.png"
    dest_path = os.path.join(IMAGES_DIR, cropped_filename)
    used_images.add(cropped_filename)

    source_path = os.path.join(GAME_REPO_DIR, raw_filename.replace("/", os.sep))
    if os.path.exists(source_path):
        try:
            img = PIL_Image.open(source_path)
            box = (uvs[0], uvs[1], uvs[0] + uvs[2], uvs[1] + uvs[3])
            img = img.crop(box)
            img.save(dest_path)
        except Exception as e:
            print(f"Failed to convert/crop image {source_path}: {e}")
    else:
        print(f"Warning: Source image not found at {source_path}")

    return cropped_filename

def load_help_menu_config(used_images):
    """Parses HelpMenu.xml and returns structured pages data along with processing required images."""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")

    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        content = f.read()
    content_filtered = re.sub(r"<\?.+\?>", "", content)
    root = ET.fromstring(content_filtered)

    pages = []
    for category in root.iter('category'):
        for page in category.iter('page'):
            raw_title = page.attrib.get('title', '').replace("$l10n_", "")
            page_data = {
                "raw_title": raw_title,
                "paragraphs": []
            }

            for paragraph in page.iter('paragraph'):
                para_title_elem = paragraph.find('title')
                para_text_elem = paragraph.find('text')
                para_image_elem = paragraph.find('image')

                para_title = ""
                if para_title_elem is not None and 'text' in para_title_elem.attrib:
                    para_title = para_title_elem.attrib['text'].replace("$l10n_", "")

                para_text = ""
                if para_text_elem is not None and 'text' in para_text_elem.attrib:
                    para_text = para_text_elem.attrib['text'].replace("$l10n_", "")

                cropped_img = None
                if para_image_elem is not None:
                    cropped_img = process_image(para_image_elem, used_images)

                page_data["paragraphs"].append({
                    "raw_title": para_title,
                    "raw_text": para_text,
                    "image": cropped_img
                })
            pages.append(page_data)
    return pages

def create_markdown_file(language_code, page_data, translations_lang, output_dir, file_index, is_index=False):
    """Creates a localized Markdown file for a single help menu page."""
    file_name = "index.md" if is_index else f"{file_index:02d}_page_{page_data['raw_title']}.md"
    file_path = os.path.join(output_dir, file_name)

    page_title = translations_lang.get(page_data["raw_title"], page_data["raw_title"])
    
    with open(file_path, "w", encoding="utf-8") as md_file:
        md_file.write(f"# {page_title}\n\n")
        for para in page_data["paragraphs"]:
            if para["raw_title"]:
                title = translations_lang.get(para["raw_title"], para["raw_title"])
                if title:
                    md_file.write(f"## {title}\n\n")
            if para["raw_text"]:
                text = translations_lang.get(para["raw_text"], para["raw_text"])
                if text:
                    formatted_text = text.replace('\n', '  \n')
                    md_file.write(f"{formatted_text}\n\n")
            if para["image"]:
                image_path = f"../assets/images/{para['image']}"
                md_file.write(f"![Image]({image_path})\n\n")

def delete_unused_images(used_images):
    """Removes any unused images from the docs/assets/images directory."""
    if os.path.exists(IMAGES_DIR):
        for filename in os.listdir(IMAGES_DIR):
            if filename not in used_images and filename.endswith(".png"):
                file_path = os.path.join(IMAGES_DIR, filename)
                os.remove(file_path)
                print(f"Deleted unused image asset: {filename}")

def generate_site(force_update=False):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)
    
    setup_game_repo(force_update=force_update)
    
    used_images = set()
    pages = load_help_menu_config(used_images)
    translations = load_translations()

    print(f"Loaded {len(pages)} help pages and {len(translations)} languages.")

    for lang_code, trans_dict in translations.items():
        lang_output_dir = os.path.join(OUTPUT_DIR, lang_code)
        os.makedirs(lang_output_dir, exist_ok=True)

        for index, page in enumerate(pages, start=1):
            is_index = (index == 1)
            create_markdown_file(lang_code, page, trans_dict, lang_output_dir, index, is_index=is_index)

    delete_unused_images(used_images)
    print("Documentation generated successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Courseplay FS25 documentation from game XMLs.")
    parser.add_argument("--update", action="store_true", help="Force update of local game_repo sparse checkout.")
    args = parser.parse_args()
    generate_site(force_update=args.update)
