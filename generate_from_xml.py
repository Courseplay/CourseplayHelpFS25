#!/usr/bin/env python3
"""
generate_from_xml.py

Directly parses Courseplay FS25 XML configuration and translation files,
crops DDS textures to PNG (using an in-memory DDS cache for performance while
guaranteeing update safety), and generates multilingual Markdown documentation for MkDocs.
"""

import re
import sys
import shutil
import subprocess
import argparse
import logging
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO, format='%(message)s')
from pathlib import Path
from dataclasses import dataclass
from typing import Optional
from PIL import Image as PIL_Image

CURRENT_DIR: Path = Path.cwd()
GAME_REPO_DIR: Path = CURRENT_DIR / "game_repo"
CONFIG_FILE: Path = GAME_REPO_DIR / "config" / "HelpMenu.xml"
TRANSLATIONS_DIR: Path = GAME_REPO_DIR / "translations"
OUTPUT_DIR: Path = CURRENT_DIR / "docs"
IMAGES_DIR: Path = OUTPUT_DIR / "assets" / "images"

FS25_TO_MKDOCS_LOCALE_MAP: dict[str, str] = {
    "br": "pt-BR",
    "cs": "zh",
    "ct": "zh-TW",
    "cz": "cs",
    "ea": "es-BR",
    "fc": "fr-CA",
    "jp": "ja",
    "kr": "ko",
    "no": "nb",
}


@dataclass
class HelpParagraph:
    raw_title: str
    raw_text: str
    image_filename: Optional[str] = None


@dataclass
class HelpPage:
    raw_title: str
    paragraphs: list[HelpParagraph]


def setup_game_repo(force_update: bool = False) -> None:
    """Clones or updates the Courseplay_FS25 repository using shallow sparse-checkout."""
    if not GAME_REPO_DIR.exists() or force_update:
        logging.info("Setting up shallow sparse-checkout of Courseplay FS25...")
        if GAME_REPO_DIR.exists():
            shutil.rmtree(GAME_REPO_DIR)
        GAME_REPO_DIR.mkdir(parents=True, exist_ok=True)
        
        # Sequential execution without shell=True guarantees reliability on Windows, Linux and CI
        try:
            subprocess.run(
                ["git", "clone", "--filter=blob:none", "--no-checkout", "--depth", "1",
                 "https://github.com/Courseplay/Courseplay_FS25.git", str(GAME_REPO_DIR)],
                check=True
            )
            subprocess.run(
                ["git", "-C", str(GAME_REPO_DIR), "sparse-checkout", "set",
                 "config/HelpMenu.xml", "translations", "img"],
                check=True
            )
            subprocess.run(
                ["git", "-C", str(GAME_REPO_DIR), "checkout"],
                check=True
            )
        except subprocess.CalledProcessError as e:
            logging.error(f"Git operation failed: {e}")
            sys.exit(1)
        logging.info("Game repository cloned successfully.")
    else:
        logging.info("Using existing local game_repo directory. (Use --update to force refresh)")


def escape_attribute_newlines(xml_string: str) -> str:
    """Replaces newlines inside XML attribute values with '&#xA;' to preserve linebreaks during parsing."""
    xml_string = re.sub(r"<\?.+\?>", "", xml_string)  # Removes the xml declaration
    regex = r'((?<=((=")))[^"]+(?<!"))'
    matches = list(re.finditer(regex, xml_string))
    for match in reversed(matches):
        s = re.sub(r"\r\n|\n\r|\n|\r|&#10;", "&#xA;", match.group())
        xml_string = xml_string[:match.start()] + s + xml_string[match.end():]
    return xml_string


# Backward-compatibility alias
filter_xml_text = escape_attribute_newlines


def load_translations() -> dict[str, dict[str, str]]:
    """Loads all language translation XML files from the game repo into dictionaries."""
    translations: dict[str, dict[str, str]] = {}
    if not TRANSLATIONS_DIR.exists():
        raise FileNotFoundError(f"Translations directory not found: {TRANSLATIONS_DIR}")

    for file_path in TRANSLATIONS_DIR.iterdir():
        if file_path.name.startswith("translation_") and file_path.name.endswith(".xml"):
            lang_code_raw = file_path.name.split("_")[1][:-4]
            lang_code = FS25_TO_MKDOCS_LOCALE_MAP.get(lang_code_raw, lang_code_raw)
            content = file_path.read_text(encoding="utf-8")
            content_filtered = escape_attribute_newlines(content)
            try:
                root = ET.fromstring(content_filtered)
            except Exception as e:
                logging.error(f"Error parsing {file_path.name}: {e}")
                continue
            
            translations[lang_code] = {}
            for entry in root.iter("text"):
                name = entry.attrib.get("name")
                val = entry.attrib.get("text", "")
                if name:
                    translations[lang_code][name] = val
    return translations


def process_image(
    image_elem: ET.Element,
    used_images: set[str],
    dds_cache: dict[Path, PIL_Image.Image]
) -> Optional[str]:
    """Extracts image metadata, converts DDS texture to cropped PNG using in-memory caching, and returns markdown filename."""
    raw_filename = image_elem.attrib.get("filename")
    if not raw_filename:
        return None
    
    uvs_str = image_elem.attrib.get("uvs", "")
    uvs = [int(val) for val in uvs_str.replace("px", "").split()]
    if len(uvs) != 4:
        logging.warning(f"Warning: Invalid UV coordinates for {raw_filename}: {uvs_str}")
        return None

    base_name = Path(raw_filename).stem
    cropped_filename = f"{base_name}_{uvs[0]}_{uvs[1]}_{uvs[2]}_{uvs[3]}.png"
    dest_path = IMAGES_DIR / cropped_filename

    # If this exact snippet hasn't been generated in the current run yet, generate it now.
    # This guarantees that updated source DDS graphics are always exported on every new run,
    # while preventing duplicate file saving within the same execution loop.
    if cropped_filename not in used_images:
        source_path = GAME_REPO_DIR / Path(*raw_filename.split("/"))
        if source_path.exists():
            try:
                if source_path not in dds_cache:
                    dds_cache[source_path] = PIL_Image.open(source_path)
                
                img = dds_cache[source_path]
                box = (uvs[0], uvs[1], uvs[0] + uvs[2], uvs[1] + uvs[3])
                cropped = img.crop(box)
                cropped.save(dest_path)
            except Exception as e:
                logging.error(f"Failed to convert/crop image {source_path}: {e}")
        else:
            logging.warning(f"Warning: Source image not found at {source_path}")

    used_images.add(cropped_filename)
    return cropped_filename


def load_help_menu_config(used_images: set[str]) -> list[HelpPage]:
    """Parses HelpMenu.xml and returns structured HelpPage models while processing required images."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(f"Configuration file not found: {CONFIG_FILE}")

    content = CONFIG_FILE.read_text(encoding="utf-8")
    content_filtered = re.sub(r"<\?.+\?>", "", content)
    root = ET.fromstring(content_filtered)

    dds_cache: dict[Path, PIL_Image.Image] = {}
    pages: list[HelpPage] = []

    try:
        for category in root.iter("category"):
            for page in category.iter("page"):
                raw_title = page.attrib.get("title", "").replace("$l10n_", "")
                paragraphs: list[HelpParagraph] = []

                for paragraph in page.iter("paragraph"):
                    para_title_elem = paragraph.find("title")
                    para_text_elem = paragraph.find("text")
                    para_image_elem = paragraph.find("image")

                    para_title = ""
                    if para_title_elem is not None and "text" in para_title_elem.attrib:
                        para_title = para_title_elem.attrib["text"].replace("$l10n_", "")

                    para_text = ""
                    if para_text_elem is not None and "text" in para_text_elem.attrib:
                        para_text = para_text_elem.attrib["text"].replace("$l10n_", "")

                    cropped_img: Optional[str] = None
                    if para_image_elem is not None:
                        cropped_img = process_image(para_image_elem, used_images, dds_cache)

                    paragraphs.append(HelpParagraph(
                        raw_title=para_title,
                        raw_text=para_text,
                        image_filename=cropped_img
                    ))

                pages.append(HelpPage(raw_title=raw_title, paragraphs=paragraphs))
    finally:
        # Clean up open PIL image file handles
        for img_handle in dds_cache.values():
            try:
                img_handle.close()
            except Exception:
                pass

    return pages


def create_markdown_file(
    language_code: str,
    page: HelpPage,
    translations_lang: dict[str, str],
    output_dir: Path,
    file_index: int,
    is_index: bool = False
) -> None:
    """Creates a localized Markdown file for a single help menu page."""
    file_name = "index.md" if is_index else f"{file_index:02d}_page_{page.raw_title}.md"
    file_path = output_dir / file_name

    page_title = translations_lang.get(page.raw_title, page.raw_title)
    
    lines: list[str] = [f"# {page_title}\n\n"]
    for para in page.paragraphs:
        if para.raw_title:
            title = translations_lang.get(para.raw_title, para.raw_title)
            if title:
                lines.append(f"## {title}\n\n")
        if para.raw_text:
            text = translations_lang.get(para.raw_text, para.raw_text)
            if text:
                formatted_text = text.replace("\n", "  \n")
                lines.append(f"{formatted_text}\n\n")
        if para.image_filename:
            image_path = f"../assets/images/{para.image_filename}"
            lines.append(f"![Image]({image_path})\n\n")

    file_path.write_text("".join(lines), encoding="utf-8")


def delete_unused_images(used_images: set[str]) -> None:
    """Removes any unused images from the docs/assets/images directory."""
    if IMAGES_DIR.exists():
        for file_path in IMAGES_DIR.glob("*.png"):
            if file_path.name not in used_images:
                try:
                    file_path.unlink(missing_ok=True)
                    logging.info(f"Deleted unused image asset: {file_path.name}")
                except OSError as e:
                    logging.error(f"Failed to delete {file_path.name}: {e}")


def generate_docs(force_update: bool = False) -> None:
    """Main routine to set up repository, extract translation dictionaries and output markdown documentation."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    setup_game_repo(force_update=force_update)
    
    used_images: set[str] = set()
    pages = load_help_menu_config(used_images)
    translations = load_translations()

    logging.info(f"Loaded {len(pages)} help pages and {len(translations)} languages.")

    for lang_code, trans_dict in translations.items():
        lang_output_dir = OUTPUT_DIR / lang_code
        lang_output_dir.mkdir(parents=True, exist_ok=True)

        for index, page in enumerate(pages, start=1):
            is_index = (index == 1)
            create_markdown_file(lang_code, page, trans_dict, lang_output_dir, index, is_index=is_index)

    delete_unused_images(used_images)
    logging.info("Documentation generated successfully!")


# Alias for backward compatibility if imported externally
generate_site = generate_docs


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Courseplay FS25 documentation from game XMLs.")
    parser.add_argument("--update", action="store_true", help="Force update of local game_repo sparse checkout.")
    args = parser.parse_args()
    generate_docs(force_update=args.update)
