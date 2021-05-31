import os

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp']

rootdir = 'C:/Users/matve/Documents/AmazonCppFileSystem'
folders = []
headerSourceList = []
headerNameList = []
cppSourceList = []
cppNameList = []



def WriteToFile(string):     #this overwrites everything that is currently in the file
    f = open("pipe.dot", 'w')
    f.write(string)
    f.close()

def init():
    for subdir, dirs, files in os.walk(rootdir):
        for file in files:
            if ".git" not in subdir:
                print(os.path.join(subdir, file)[len(rootdir):])

                for h in valid_headers:
                    if (h in file) and ("." not in file[:len(file)-len(h)]): #this checks whether or not it chooses a smaller h than needed for a file. Ex: rand.hh will trigger with ".h" AND with ".hh"
                        headerSourceList.append(os.path.join(subdir, file)[len(rootdir):])
                        headerNameList.append(file[:len(file)-len(h)]+"_"+h[1:])

                for cpp in valid_sources:
                    if (cpp in file) and ("." not in file[:len(file)-len(cpp)]): #this checks whether or not it chooses a smaller cpp than needed for a file. Ex: rand.cpp will trigger with ".c" AND with ".cpp"
                        cppSourceList.append(os.path.join(subdir, file)[len(rootdir):])
                        cppNameList.append(file[:len(file)-len(cpp)]+"_"+cpp[1:])


def create_cluster(name, fileNameList):
    cluster = ""
    cluster += "\tsubgraph cluster_"+name+" {\n\t\tlabel=\""+name+"\";\n\t\t"

    for fileName in fileNameList:
        cluster += fileName + "; "

    cluster += "\n"
    cluster += "\t}\n\n"

    return cluster


def main():
    init()

    res = ""
    res += "digraph {\n\trankdir=LR\n\n"

    res += create_cluster("header", headerNameList)
    res += create_cluster("sources", cppNameList)

    res += "}"
    WriteToFile(res)


main()
