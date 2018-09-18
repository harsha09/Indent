import re
import sys

class IndexGenerator(object):
    """Class which converts * to number points and . to space indentation"""

    #pattern which matches any line starting with '.'s or '*'s
    pattern = re.compile('\s*([.*]*)\s(.*)')


    def __init__(self, text, output_file_path):
        self.outline = []
        self.text = text.readlines()
        self.output = []
        # stack ds to generate +/- index. It is used to replace previous line's - with +
        self.stack = []
        self.output_file_path = output_file_path


    @classmethod
    def split(cls, text):
        splitted_txt = re.findall(cls.pattern, text)
        if splitted_txt: return splitted_txt[0]


    def get_indent_level(self, splitted_txt):
        """ :args: splitted_txt: list
            Converts the lines to index.
            if starts with * then numbering 
            if starts with . then +/-
            if it doesn't include both considering same line continuation with previous line"""
        indent_len = len(splitted_txt[0])
        outline_len = len(self.outline)
        indentation = ''
        prev_indent = ''

        if not splitted_txt: return ''

        if self.stack:
            previous = self.stack.pop()
            previous_list = []
            prev_indent = previous[0]
            
            # if line not starting with * or . then consider it as continuation line with previous line.
            if indent_len == 0:
                previous_1 = '{}\n{}{}'.format(
                    previous[1], ' '*len(prev_indent), splitted_txt[1])
                previous = (previous[0], previous_1)
                self.stack.append(previous)
                return

            # if previous line indent has - and current line starts with .
            if ('-' in prev_indent) and ('.' in splitted_txt[0]):
                # replace previous line - with + if current line is under previous line
                operator = '+' if len(prev_indent) < (indent_len + 1) else '-'
                prev_indent = prev_indent.replace('-', operator)

            self.stack.append((prev_indent, previous[1]))

        # if line starting with . index with + or -
        if '.' in splitted_txt[0]:
            indentation = '{}{}'.format(' '*indent_len, '-')

        # if line starting with * index with numbers
        if '*' in splitted_txt[0]:
            # if current line stars len is greater than previous line then append 1.
            if outline_len < indent_len:
                self.outline.append(1)
            # if current line no of stars less than previous line
            # no of stars then increment previous number by 1.
            elif outline_len > indent_len:
                self.outline = self.outline[:indent_len]
                self.outline[-1] += 1
            else:
                self.outline[-1] += 1

            indentation = '.'.join([str(i) for i in self.outline])

        self.stack.append((indentation, splitted_txt[1]))


    def generate(self):
        """Writes to file."""
        for i in self.text:
            splitted_txt = self.split(i)
            if splitted_txt:
                indexed_text = self.get_indent_level(splitted_txt)
        self.output = ['{} {}'.format(i[0], i[1]) for i in self.stack]

        self.output_file_path.write('\n'.join(self.output))
        self.output_file_path.close()


if __name__ == '__main__':

    text = sys.stdin
    output_file_path = sys.stdout

    generator = IndexGenerator(text, output_file_path)
    generator.generate()


