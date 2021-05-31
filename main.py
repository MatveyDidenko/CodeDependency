import os

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp', '.py']

rootdir = 'C:/Users/matve/Documents/AmazonCppFileSystem'
folders = []
headerSourceList = []
headerNameList = []
fileSourceList = []
fileNameList = []



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
                print(path)
                head_tail = os.path.split(path)

                print(head_tail)
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

    init()

    print(folders)

    res += "}"
    WriteToFile(res)


main()
