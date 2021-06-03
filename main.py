import os

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp', '.py']
valid_extensions = valid_headers + valid_sources

rootdir = 'C:\\Users\\matve\\Documents\\AmazonCppFileSystem\\src'
dot_file = ""
folders = []
headerSourceList = []
headerNameList = []
fileSourceList = []
fileNameList = []

def strip_cluster(path):
    return path[len(rootdir):].replace("\\", "_").replace(".", "_")

def strip_file(path):
    head_tail = os.path.split(path)
    return path[len(head_tail[0])+1:].replace(".", "_")

def strip_label(path):
    return path[path.rfind("\\")+1:]

def get_extension(path):
    """ Return the extension of the file targeted by path. """
    return path[path.rfind('.'):]

def find_all_files(path, recursive=True):
    global dot_file
    """
    Return a list of all the files in the folder.
    If recursive is True, the function will search recursively.
    """
    for entry in os.scandir(path):
        if entry.is_dir() and recursive:
            #createdot_file with name entry
            dot_file += "\n\tsubgraph cluster"+strip_cluster(str(entry.path))+" {\n\t\tlabel=\""+strip_label(str(entry.path))+"\";\n\t\t"

            find_all_files(entry.path)

            #add }
            dot_file += "\n}"
        elif get_extension(entry.path) in valid_extensions:
            #add todot_file
            dot_file += strip_file(str(entry.path)) + "; "

def WriteToFile(string):     #this overwrites everything that is currently in the file
    f = open("pipe.dot", 'w')
    f.write(string)
    f.close()

def main():
    res = ""
    res += "digraph {\n\trankdir=LR\n\n"

    find_all_files(rootdir)

    res += dot_file

    res += "\n}"
    WriteToFile(res)

main()
