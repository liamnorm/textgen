import sys
import re


# This script takes a text input and outputs an SVG, "output.svg", with that text in Jenkins font.

origin_x = -227.45483
origin_y = -163.26117

start = """
<svg version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="300" height="300" viewBox="0,0,300,300">
"""

end = "</svg>"

# we want to get rid of all instances of this box in our output
stupid_invisible_box = '<path d="M227.45485,196.73885v-33.47767h25.09035v33.47767z" fill="none" stroke-width="0"/>'

group_pattern = re.compile("<g data-paper-data=.*\/><\/g>")
inv_box_pattern = re.compile('<path d="M227.*fill="none" stroke-width="0"\/>')

# given a character, get the svg file for it, and then get the text representing the group shape for it.
def get_group(char):
    ascii_code = ord(char)
    if ascii_code < 32 or ascii_code > 127:
        return ""
    svg_path = f"chars/{ascii_code}.svg"
    try:
        f = open(svg_path, "r")
        text = f.read()

        text = group_pattern.findall(text)[0]
        to_remove = inv_box_pattern.findall(text)[0]

        text = text.replace(to_remove, "")

        return text
    except:
        return ""

CHARWIDTHS = [
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,
	0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,
	# ! to 0
	4, 8, 8, 8, 8, 8, 4, 8, 8, 8, 8, 6, 8, 5, 8, 8,
	# 1 to @
	8, 8, 8, 10, 8, 8, 8, 8, 8, 5, 6, 8, 8, 8, 8, 8,
	# A to P
	9, 8, 8, 8, 9, 8, 10, 8, 7, 10, 9, 8, 11, 10, 10, 8,
	# Q to `
	10, 8, 8, 8, 8, 8, 12, 8, 8, 9, 8, 8, 8, 9, 8, 8,
	# a to p
	8, 8, 8, 9, 7, 8, 8, 8, 4, 6, 8, 4, 11, 8, 8, 8,
	# q to 
	10, 8, 8, 7, 7, 8, 11, 8, 9, 8, 8, 8, 8, 8, 8, 8
]

def translate(x, y, middle): 
    return "<g transform=\"translate(" + str(origin_x + x) + "," + str(origin_y + y) + ")\">" + middle + "</g>"


def main(args):

    # arg 0 being 0 means type the text you want.
    # arg 0 being 1 means the input is a file.
    text = ""

    if args[0] == "0":
        text = args[1]
    else:
        filename = args[1]
        text = ""
        lines = []
        with open(filename) as file:
            lines = [line.rstrip() for line in file]
        for line in lines:
            text += line + "\n"

    svg_text = start 

    x = 0
    y = 0
    for char in text:
        if char == "\n":
            y += 16
            x = 0
        else:
            char_group_text = get_group(char)
            svg_text += translate(x, y, char_group_text)
            x += CHARWIDTHS[ord(char)-1] * .9

    svg_text += end
    with open("output.svg", "w") as f:
        f.write(svg_text)

    print("Generated SVG!")


if __name__ == "__main__":
   main(sys.argv[1:])