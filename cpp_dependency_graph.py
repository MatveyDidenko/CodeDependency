import os
import optparse

#TODO consider differnt number of spaces
include_notation = "#include \""

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp']
valid_extensions = valid_headers + valid_sources

parser = optparse.OptionParser()

parser.add_option('-s', '--source',
    action="store", dest="main_folder",
    help="Main folder that contains the secondary folder", default="src")

parser.add_option('-c', '--secondary',
    action="store", dest="source_folder",
    help="The secondary folder that contains the dir that needs to be structured", default="src")

parser.add_option('-o', '--output',
    action="store", dest="dot_file",
    help="DOT file with source dependency graph", default="src.dot")

options, args = parser.parse_args()

main_folder = options.main_folder
rootdir = options.source_folder
output_path = options.dot_file

dot_file = ""

files = {}

def strip_cluster(path):
    return path[len(rootdir):].replace(os.sep, "_").replace("-", "_").replace(".", "_")

def strip_file(path):
    head_tail = os.path.split(path)
    return path[len(head_tail[0])+1:].replace(".", "_").replace("-", "_")

def strip_label(path):
    return path[len(rootdir):]

def get_extension(path):
    """ Return the extension of the file targeted by path. """
    return path[path.rfind('.'):]

def get_list_of_includes(path):
    # parse file cpp or h to get list of includes
    # add to global dictionary with unique path
    file = open(path, 'r')
    lines = file.readlines()

    list_of_includes = []

    for line in lines:
        if include_notation in line:
            include_file = line[len(include_notation)-1:line.rfind("\"", 2)]
            list_of_includes.append(strip_file(include_file).replace(".", "_"))

    return list_of_includes

def connections(dict):
    connections_dot = "\n\n"

    for key in dict.keys():
        for include in dict[key]:
            connections_dot += key + " -> " + include + ";\n"

    return connections_dot

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
            dot_file += "\n}\n"
        elif get_extension(entry.path) in valid_extensions:
            #create file with the correct notation fo
            stripped_file = strip_file(str(entry.path))

            #if there is a file with the same name as another file, we have to add something that makes it different in order for the .dot file to show it
            while stripped_file in files:
                stripped_file += "_"

            files[stripped_file] = get_list_of_includes(entry.path)

            #add to dot_file
            if get_extension(entry.path) in valid_headers:
                dot_file += stripped_file + " [color=green]; "
            else:
                dot_file += stripped_file + " [color=blue]; "

def WriteToFile(string, output_path):     #this overwrites everything that is currently in the file
    f = open(output_path, 'w')
    f.write(string)
    f.close()

def graph(path, output_path):
    res = ""
    res += "digraph {\n\trankdir=LR\n\n"

    find_all_files(path)

    res += dot_file
    res += connections(files)

    res += "\n}"

    WriteToFile(res, output_path)

if __name__ == '__main__':
    graph(rootdir, output_path)
