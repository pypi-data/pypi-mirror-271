from dataclasses import dataclass
import logging
import os
from typing import Union, List

from bs4 import BeautifulSoup, Tag
from mkdocs.config import config_options, config_options, base
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.structure.files import Files
from mkdocs.structure.pages import Page

DEFAULT_VERSION = "releases/2024.4.2"
SCRIPT = 'https://pyscript.net/{version}/core.js'
CSS = 'https://pyscript.net/{version}/core.css'

from . import glr_path_static

@dataclass
class Script():
    path: str
    type: str = None
    defer: bool = None
    async_: bool = None

class MyPluginConfig(base.Config):
    pyscript_version = config_options.Type(str, default=DEFAULT_VERSION)
    selective = config_options.Type(bool, default=False)

class Plugin(BasePlugin[MyPluginConfig]):
    logger = get_plugin_logger("mkdocs-pyscript")
    def __init__(self):
        self.enabled = True
        self.total_time = 0
        self.logger.setLevel(logging.DEBUG)
        

    def on_config(self, config: MkDocsConfig) -> Union[MkDocsConfig, None]:
        # Append static resources
        config["theme"].dirs.append(glr_path_static("dist/js"))
        config["theme"].dirs.append(glr_path_static("dist/css"))
        for file in os.listdir(glr_path_static("dist/css")):
            if file.endswith(".css"):
                config["extra_css"].append(file)

        for file in os.listdir(glr_path_static("dist/js")):
            if file.endswith(".js"):
                config["extra_javascript"].append(file)


        # Set version
        self.SCRIPT_LINK = SCRIPT.format(version=self.config.pyscript_version)
        self.CSS_LINK = CSS.format(version=self.config.pyscript_version)

        # Disable navigation.instant
        if 'features' in config['theme'] and 'navigation.instant' in config['theme']['features']:
            self.logger.warning("mkdocs-pyscript is not compatible with navigation.instant; instant navigation will be disabled.")
            config['theme']['features'].remove('navigation.instant')

        if 'attr_list' not in config['markdown_extensions']: config['markdown_extensions'].append('attr_list')
        
        return config
    
    def scriptize(self, soup: BeautifulSoup, block: Tag, *, script_type="unmanaged-pyscript-mkdocs", label=None, attrs: dict = None):
        #Remove linenumber links:
        lineno_links = block.find_all('a')
        for a in lineno_links:
            if 'href' in a.attrs and "codelineno" in a['href']: a.extract()

        script = soup.new_tag("script")
        script['type'] = script_type
        if label: script['id'] = label
        for k, v in attrs.items():
            script.attrs[k] = v
        script.string = block.text
        return script


    def on_page_content(self, html: str, *, page: Page, config: MkDocsConfig, files: Files) -> Union[str, None]:
        soup = BeautifulSoup(html, features="html.parser")

        tag_names = ['code', 'div']

        # Get all potential codeblocks in order:
        #code_blocks: List[Tag] = []
        #tag = soup.find(name=tag_names)
        #if tag:
        #    code_blocks.append(tag)
        #    while tag:= tag.find_next(name=tag_names):
        #        # Only include "top level" code tags
        #        if not any((tag in existing_tag.descendants) for existing_tag in code_blocks): code_blocks.append(tag)

        code_blocks: list[Tag] = soup.find_all(name=tag_names)

        # exit early if no codeblocks on page
        if not code_blocks: return html

        # Process all blocks
        for block in code_blocks:
            print(block.attrs)
            try:
                #Classless blocks cannot be handled
                classes = block.attrs['class']
            except KeyError:
                continue


            # Move classes from exterior pre/post to py-wrapper
            if block.parent.name == 'pre' and 'class' in block.parent.attrs:
                block.attrs['class'].extend(block.parent.attrs['class'])
                
            if (self.config.selective and 'pyscript' in classes) or \
                    ((not self.config.selective) and ('language-python' in classes or 'language-py' in classes or 'pyscript' in classes)):
            

                #Wrap codeblock in a new div
                div = soup.new_tag('div')
                div['class'] = "py-wrapper"
                div['style'] = "position:relative;"
                if 'setup' in block.attrs:
                    div['style'] += 'display: none;'
                #div['id'] = f"py-main-{(primary_block_index := primary_block_index + 1)}"

                block.wrap(div) # Wrap codeblock with div

                if 'setup' in block.attrs:
                    env = block.attrs['env'] if 'env' in block.attrs else ""
                    block.replace_with(self.scriptize(soup, block, script_type='py-editor', attrs={'setup': '', 'env' : env}))
                    print('Replacing with script')
            
        return str(soup)
    
    def on_post_page(self, output: str, *, page: Page, config: MkDocsConfig) -> Union[str, None]:
        soup = BeautifulSoup(output, features="html.parser")
        codeblocks = soup.find_all(attrs={"class": "py-wrapper" },)
        if (len(codeblocks)):
            # Add importmap
            script_tag = soup.new_tag("script")
            script_tag['type'] = "module"
            script_tag['src'] = self.SCRIPT_LINK
            soup.head.append(script_tag)

            css = soup.new_tag('link')
            css['rel'] = 'stylesheet'
            css['href'] = self.CSS_LINK
            soup.head.append(css)

            # Make makeblock script a module
            makeblocks = [s for s in soup.find_all("script") if 'src' in s.attrs and "makeblocks" in s['src']][0]
            makeblocks['type'] = "module"
        return str(soup)
    
