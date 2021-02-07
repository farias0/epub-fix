# script to fix a problem found when rendering the book
# "Node.js Design Patterns" (epub) on an e-reader

# problem: code blocks are rendered as a single continuous line
# (no line breaks) and without indentation

# fix: inside each code block, add HTML-style double spaces 
# at the beggining of each line (according to the identation) and 
# add HTML-style line breaks before the end of each line

# how to use: extract the epub files (unzip book.epub),
# patch them using this script and then zip them back with:
## zip -X book.epub mimetype
## zip -rg book.epub META-INF
## zip -rg book.epub OEBPS

######

# sub-strings defining the opening and closing of block codes. not very well tested
INIT_BLOCK = "<pre class=\"programlisting code\">"
CLOSE_BLOCK = "</pre>"

LINE_BREAK = "\n"
NEW_LINE_BREAK = "<br/>"

SINGLE_SPACE = " "
DOUBLE_SPACE = SINGLE_SPACE * 2
NEW_DOUBLE_SPACE = "&#160;"

CHAPTERS_PATH = "extracted_book/OEBPS/Text/" 

def fix_line(line):
  char_number = 0
  double_space_count = 0

  # iterates over string counting the number of double spaces at the start 
  if INIT_BLOCK not in line: # the first code block lines are level 1 idented
    while char_number < len(line):
      if line[char_number] == SINGLE_SPACE:
        if line[char_number+1] == SINGLE_SPACE:
          double_space_count += 1
          char_number+=2
        else:
          break
      else:
        break
  
  line_start_index = double_space_count * 2
  line = line[:line_start_index] + NEW_DOUBLE_SPACE * double_space_count + line[line_start_index:]

  line = line[:-1] + NEW_LINE_BREAK + LINE_BREAK

  return line


def fix_chapter(file_path):
  print ("> fixing " + file_path)

  file = open(file_path, "r")
  lines = file.readlines()

  # finds a line that contains INIT_BLOCK and, for every line between it and
  # one containing CLOSE_BLOCK, fixes it with fix_line()
  line_number = 0
  while line_number < len(lines):
    if INIT_BLOCK in lines[line_number]:
      print("line " + str(line_number+1))
      while True:
        lines[line_number] = fix_line(lines[line_number])
        if CLOSE_BLOCK in lines[line_number]:
          break
        line_number+=1
    else:
      line_number+=1

  file.close()

  # write back to disk
  file = open(file_path, "w")
  file.write("".join(lines))
  file.close()
      
def main():
  fix_chapter(CHAPTERS_PATH + "Preface.xhtml")

  chapter = 1
  while chapter <= 13:
    fix_chapter(CHAPTERS_PATH + "Chapter_" + str(chapter) + ".xhtml")
    chapter+=1

main()