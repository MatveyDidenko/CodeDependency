import os

valid_headers = ['.h', '.hh', '.hpp']
valid_sources = ['.c', '.cc', '.cpp']

def WriteToFile(string):     #this overwrites everything that is currently in the file
    f = open("pipe.dot", 'w')
    f.write(string)
    f.close()


rootdir = 'C:/Users/matve/Documents/AmazonCppFileSystem'
fileList = []

for subdir, dirs, files in os.walk(rootdir):
    for file in files:
        if ".git" not in str(subdir):
            print(os.path.join(subdir, file))

        for header in valid_headers:
            if header in file:
                fileList += file

print(fileList)
