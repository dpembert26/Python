# Import Regex Module
import re


# Open file and then read it. Close it afterwards
def readfile():
    file1 = r"C:\Users\darin\Documents\DellSharepointPerl.txt"
    read = 'r'
    contents = open(file1, mode=read)
    read_contents = contents.read()
    contents.close()
    read_contents = read_contents.split()
    return read_contents


# Open a file and write to it. Close it afterwards
def writefile():
    file2 = r"C:\Users\darin\Documents\TestFile.txt"
    write = 'w'
    writer = open(file2, mode=write)
    writer.write(r"The pattern for the url was matched\n")
    writer.close()


# get match for url read in from file
def geturl():
    for content in readfile():
        pattern = r"\w.+(shareperl).+"
        getpat = re.compile(pattern)
        get_content = getpat.search(content)

        if get_content:
            print("MATCHED: This is the url's name %s" % get_content.group(0))
            writefile()
            break
        else:
            print("The match came out as %s" % get_content + " for url %s" % content + ". The url is not found")


def main():
    readfile()
    geturl()

main()
