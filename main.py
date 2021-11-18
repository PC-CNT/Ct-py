import os
import re
import argparse

class frame:
    """クラス変数：parser, args
    インスタンス変数：
    """
    parser = argparse.ArgumentParser(description="""簡易的なコマンドライン操作のテキスト置換（正規表現での検索、指定の行に挿入するモード付き）.py""")
    parser.add_argument("-m", "--edit_mode", help="Edit mode", choices=["replace", "regex", "insert"], default="replace")
    parser.add_argument("-i", "--input", help="Input file", required=True)
    parser.add_argument("-ow", "--overwrite", help="Overwrite input file", action="store_true")
    parser.add_argument("-s", "--search_word", help="Search word")
    parser.add_argument("-p", "--regex_pattern", help="Regex pattern")
    parser.add_argument("-l", "--insert_line", help="Insert line number (works with insert mode)", type=int)
    parser.add_argument("-r", "--replace_word", help="Replace word", required=True)
    parser.add_argument("-d", "--debug", help="Debug mode", action="store_true")
    args = parser.parse_args()

    def __init__(self):
        pass

    def debug(self):
        print(type(self.args))
        print("args:" + self.args)

    def escape(self, input_text : str) -> str:
        return input_text.replace("__quotation__", "\"")

    def text_write(self, input_text, replace_text, overwrite : bool):
        if overwrite:
            with open(input_text, "w") as f:
                f.write(replace_text)
        else:
            text_dir = os.path.dirname(self.args.input)
            text_name = os.path.splitext(os.path.basename(self.args.input))[0]
            replace_text_path = os.path.join(text_dir, text_name + "_replace.txt")
            with open(replace_text_path, "w") as f:
                f.write(replace_text)

    def text_Replace(self, input_text, search_word, replace_word):
        """テキストファイルを読み込んで文字列を置換、元のファイルを上書きする
        """
        with open(input_text, "r") as f:
            source_text = f.read()  # ファイルを読み込む
        replace_text = source_text.replace(search_word, replace_word)  # 文字列を置換
        self.text_write(input_text, replace_text, self.args.overwrite)

    def text_Regex(self, input_text, regex_pattern, replace_word):
        """TODO テキストファイルを読み込んで正規表現で置換、元のファイルを上書きする
        """
        with open(input_text, "r") as f:
            source_text = f.read()
        replace_text = re.sub(regex_pattern, replace_word, source_text)
        with open(input_text, "w") as f:
            f.write(replace_text)

    def text_insert(self, input_text, insert_line, insert_word):
        """TODO テキストファイルを読み込んで指定の行に文字列を挿入する
        """
        with open(input_text, "r") as f:
            source_text = f.readlines()
        replace_text_list = source_text.insert(insert_line, insert_word)
        replace_text = "\n".join(replace_text_list)
        self.text_write(input_text, replace_text, self.args.overwrite)
        # with open(input_text, "w") as f:
        #     f.writelines(replace_text)

    def main(self):
        if self.args.debug:
            self.debug()
        if self.args.edit_mode == "replace":
            self.text_Replace(self.args.input, self.escape(self.args.search_word), self.escape(self.args.replace_word))
        elif self.args.edit_mode == "regex":
            self.text_Regex(self.args.input, self.escape(self.args.regex_pattern), self.escape(self.args.replace_word))
        elif self.args.edit_mode == "insert":
            self.text_insert(self.args.input, self.args.insert_line, self.escape(self.args.replace_word))

if __name__ == '__main__':
    main = frame()
    main.main()