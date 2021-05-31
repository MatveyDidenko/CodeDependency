import os

valid_headers = ['.h']
valid_sources = ['.cpp']

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
                    if h in file:
                        headerSourceList.append(os.path.join(subdir, file)[len(rootdir):])
                        headerNameList.append(file[:len(file)-2]+"_h")

                for cpp in valid_sources:
                    if cpp in file:
                        cppSourceList.append(os.path.join(subdir, file)[len(rootdir):])
                        cppNameList.append(file[:len(file)-4]+"_cpp")


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
