import os

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp', '.py']
valid_extensions = valid_headers + valid_sources

rootdir = 'C:\\Users\\matve\\Documents\\AmazonCppFileSystem\\src'
dot_file = ""
files = {}

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

def connections(dict):
    connections_dot = ""

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
            dot_file += "\n}"
        elif get_extension(entry.path) in valid_extensions:
            #create file with the correct notation fo
            stripped_file = strip_file(str(entry.path))

            #if there is a file with the same name as another file, we have to add something that makes it different in order for the .dot file to show it
            while stripped_file in dot_file:
                stripped_file += "_"

            # parse file cpp or h to get list of includes
            # add to global dictionary with unique path
            file = open(entry.path, 'r')
            lines = file.readlines()
            include_notation = "#include \""
            list_of_includes = []

            for line in lines:
                if include_notation in line:
                    list_of_includes.append(line[len(include_notation):].replace("\"", "").replace(".", "_").replace("\n", ""))

            files[stripped_file] = list_of_includes

            #add todot_file
            dot_file += stripped_file + "; "

def WriteToFile(string):     #this overwrites everything that is currently in the file
    f = open("pipe.dot", 'w')
    f.write(string)
    f.close()

def main():
    res = ""
    res += "digraph {\n\trankdir=LR\n\n"

    find_all_files(rootdir)

    res += dot_file
    res += connections(files)

    res += "\n}"

    WriteToFile(res)

main()
