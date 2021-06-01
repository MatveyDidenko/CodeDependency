import os

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp', '.py']
valid_extensions = valid_headers[0] + valid_sources[2]

rootdir = 'C:/Users/matve/Documents/AmazonCppFileSystem'
folders = []
headerSourceList = []
headerNameList = []
fileSourceList = []
fileNameList = []

def get_extension(path):
	""" Return the extension of the file targeted by path. """
	return path[path.rfind('.'):]

def find_all_files(path, recursive=True):
	"""
	Return a list of all the files in the folder.
	If recursive is True, the function will search recursively.
	"""
	files = []
	cluster = ""
	for entry in os.scandir(path):
		if entry.is_dir() and recursive:
			#create cluster with name entry
			cluster += "\n\tsubgraph cluster_"+str(entry.path)+" {\n\t\tlabel=\""+str(entry.path)+"\";\n\t\t"

			files += find_all_files(entry.path)

			#add }
			cluster += "\n}"
		elif get_extension(entry.path) in valid_extensions:
			#add to cluster
			cluster += str(entry.path) + "; "

			files.append(entry.path)
	return cluster

def WriteToFile(string):     #this overwrites everything that is currently in the file
    f = open("pipe.dot", 'w')
    f.write(string)
    f.close()

def stringInFile(string):
    with open('pipe.dot') as f:
        if string in f.read():
            return True

def create_cluster(name, fileNameList):
    cluster = ""
    cluster += "\n\tsubgraph cluster_"+name+" {\n\t\tlabel=\""+name+"\";\n\t\t"

    for fileName in fileNameList:
        cluster += fileName + "; "

    cluster += "\n"
    cluster += "\t}\n\n"

    return cluster

def create_file(name):
    file = name + "; "
    return file

def init():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if len(file.split(".")) == 2:
                extension = "."+file.split(".")[1]

            if ".git" not in subdir and (extension in valid_headers or extension in valid_sources):
                path = os.path.join(subdir, file)[len(rootdir):]
                #print(path)
                head_tail = os.path.split(path)

                #print(head_tail)
                head = head_tail[0]
                tail = head_tail[1]

                if head == '\\': #not in any folder
                    fileNameList.append(file)
                else:
                    for folder in head.split('\\'):
                        if folder not in folders and folder != '':
                            folders.append(folder)






def main():
    res = ""
    res += "digraph {\n\trankdir=LR\n\n"

    res += find_all_files(rootdir)

    res += "\n}"
    WriteToFile(res)

main()
