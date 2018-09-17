import re

class IndexGenerator(object):
    """Class which converts * to number points and . to space indentation"""

    #pattern which matches any line starting with '.'s or '*'s
    pattern = re.compile('\s*([.*]*)\s(.*)')


    def __init__(self, text, output_file_path):
        self.outline = []
        self.text = text
        self.output = []
        self.stack = []
        self.output_file_path = output_file_path


    @classmethod
    def split(cls, text):
        splitted_txt = re.findall(cls.pattern, text)
        if splitted_txt: return splitted_txt[0]


    def get_indent_level(self, splitted_txt):
        indent_len = len(splitted_txt[0])
        outline_len = len(self.outline)
        indentation = ''
        prev_indent = ''

        if not splitted_txt: return ''

        if self.stack:
            previous = self.stack.pop()
            previous_list = []
            prev_indent = previous[0]
            
            if indent_len == 0:
                previous_1 = '{}\n{}{}'.format(
                    previous[1], ' '*len(prev_indent), splitted_txt[1])
                previous = (previous[0], previous_1)
                self.stack.append(previous)
                return

            if ('-' in prev_indent) and ('.' in splitted_txt[0]):
                operator = '+' if len(prev_indent) < (indent_len + 1) else '-'
                prev_indent = prev_indent.replace('-', operator)

            self.stack.append((prev_indent, previous[1]))

        if '.' in splitted_txt[0]:
            indentation = '{}{}'.format(' '*indent_len, '-')

        if '*' in splitted_txt[0]:
            if outline_len < indent_len:
                self.outline.append(1)
            elif outline_len > indent_len:
                self.outline = self.outline[:indent_len]
                self.outline[-1] += 1
            else:
                self.outline[-1] += 1

            indentation = '.'.join([str(i) for i in self.outline])

        self.stack.append((indentation, splitted_txt[1]))


    def generate(self):
        for i in self.text.split('\n'):
            splitted_txt = self.split(i)
            if splitted_txt:
                indexed_text = self.get_indent_level(splitted_txt)
        self.output = ['{} {}'.format(i[0], i[1]) for i in self.stack]

        with open(output_file_path, 'w') as fh:
            fh.write('\n'.join(self.output))


if __name__ == '__main__':
    import sys
    text = sys.argv[0]
    output_file_path = sys.argv[1]

    generator = IndexGenerator(text, output_file_path)
    generator.generate()


