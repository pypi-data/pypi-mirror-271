from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
import re

_code_open = re.compile('(?P<backticks>`+)(?P<syntax>\w*)\s*$')

class MermaidPreProcessor(Preprocessor):
    def run(self, lines):
        new_lines = []
        in_code_block = False
        in_mermaid = False

        for line in lines:
            # Code block opened
            if (not in_code_block) and (open_match := _code_open.match(line)):
                # Code block is mermaid
                if open_match["syntax"] == "mermaid":
                    line = '<div class="mermaid">'
                    in_mermaid = True

                in_code_block = True
                backticks = open_match["backticks"]

            # Code block close found
            elif in_code_block and re.match(backticks + '\s*$', line):
                # Replace with closing div to close mermaid
                if in_mermaid:
                    line = '</div>'
                    in_mermaid = False

                in_code_block = False

            new_lines.append(line)

        return new_lines

class MarkdownMermaid(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(
            MermaidPreProcessor(md),
            'mermaid',
            35
        )


def makeExtension(**kwargs):
    return MarkdownMermaid(**kwargs)

