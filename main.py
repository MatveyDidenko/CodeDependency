import os

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp']

def WriteToFile(string):     #this overwrites everything that is currently in the file
    f = open("pipe.dot", 'w')
    f.write(string)
    f.close()


rootdir = 'C:/Users/matve/Documents/AmazonCppFileSystem'
folders = []
headerSourceList = []
headerNameList = []


for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if ".git" not in subdir:
            print(os.path.join(subdir, file))

            for header in valid_headers:
                if header in file:
                    headerSourceList.append(os.path.join(subdir, file))
                    headerNameList.append(file)

res = "digraph {\n\trankdir=LR\n\n\t"

res += "subgraph cluster_0 {\n\t\tlabel=\"Header Files\";\n\t\t"

for name in headerNameList:
    res += name[:len(name)-2] + "; "

res += "\n"
res += "\t}\n\n"


res += "}"
WriteToFile(res)
