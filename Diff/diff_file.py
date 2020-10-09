import difflib
import sys

try:
    text_file1 = sys.argv[1]
    text_file2 = sys.argv[2]
except Exception as e:
    print("Error: {}".format(str(e)))
    print("Usage: diff_module.py filename1 filename2")
    sys.exit()


def readfile(filename):
    try:
        with open(filename) as f_obj:
            text = f_obj.read().splitlines()
        return text
    except IOError as ee:
        print("Read file Error: {}".format(str(ee)))
        sys.exit()


if not all([text_file1, text_file2]):
    print("Usage: diff_module.py filename1 filename2")
    sys.exit()

text1_lines = readfile(text_file1)
text2_lines = readfile(text_file2)

d = difflib.HtmlDiff()
print(d.make_file(text1_lines, text2_lines))
