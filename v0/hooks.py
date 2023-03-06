# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.

import re
import shutil
import logging
import mkdocs.config
import mkdocs.config.config_options
import mkdocs.plugins
import mkdocs.structure.files
import mkdocs.structure.nav
import mkdocs.structure.pages

log = logging.getLogger(f"mkdocs.plugins.{__name__}")
rulesItem: mkdocs.structure.nav.Section = mkdocs.structure.nav.Section("Rules", [])

# Replace MAML headers
def replace_maml(markdown: str, page: mkdocs.structure.nav.Page, config: mkdocs.config.Config, files: mkdocs.structure.files.Files, **kwargs) -> str:
    markdown = markdown.replace("## about_PSRule_Azure_Configuration", "")
    markdown = markdown.replace("# PSRule_Azure_Configuration", "# Configuration options")

    # Rules
    markdown = markdown.replace("## SYNOPSIS", "")
    markdown = markdown.replace("## DESCRIPTION", "## Description")
    markdown = markdown.replace("## RECOMMENDATION", "## Recommendation")
    markdown = markdown.replace("## NOTES", "## Notes")
    markdown = markdown.replace("## EXAMPLES", "## Examples")
    markdown = markdown.replace("## LINKS", "## Links")

    # Conceptual topics
    markdown = markdown.replace("## SHORT DESCRIPTION", "")
    markdown = markdown.replace("## LONG DESCRIPTION", "## Description")
    markdown = re.sub("(\#\#\s+(NOTE|KEYWORDS)\s+(.|\s{1,2}(?!\#))+)", "", markdown)

    return markdown

# Dynamically build reference nav
def build_reference_nav(nav: mkdocs.structure.nav.Navigation, config: mkdocs.config.Config, files: mkdocs.structure.files.Files) -> mkdocs.structure.nav.Navigation:
    build_rule_nav(nav, config, files)
    build_baseline_nav(nav, config, files)
    return nav

# Build Rules list
def build_rule_nav(nav: mkdocs.structure.nav.Navigation, config: mkdocs.config.Config, files: mkdocs.structure.files.Files):
    children = []
    item: mkdocs.structure.nav.Section = mkdocs.structure.nav.Section("Rules", children)

    for f in files:
        if not f.is_documentation_page():
            continue

        if not f._get_stem().startswith("Azure."):
            continue

        if f._get_dest_path(False).__contains__("/rules/"):
            children.append(mkdocs.structure.pages.Page(f._get_stem(), f, config))

    referenceItem: mkdocs.structure.nav.Section = next(x for x in nav if x.title == "Reference")
    referenceItem.children.append(item)
    mkdocs.structure.nav._add_parent_links(nav)

# Build Baselines list
def build_baseline_nav(nav: mkdocs.structure.nav.Navigation, config: mkdocs.config.Config, files: mkdocs.structure.files.Files):
    children = []
    item: mkdocs.structure.nav.Section = mkdocs.structure.nav.Section("Baselines", children)

    for f in files:
        if not f.is_documentation_page():
            continue

        if f._get_dest_path(False).__contains__("/baselines/"):
            children.append(mkdocs.structure.pages.Page(f._get_stem(), f, config))

    referenceItem: mkdocs.structure.nav.Section = next(x for x in nav if x.title == "Reference")
    referenceItem.children.append(item)
    mkdocs.structure.nav._add_parent_links(nav)
