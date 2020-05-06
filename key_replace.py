import os
import sys

print("""
### Warning!!!! 
1) Destination files will be replaced.........
2) Key pattern should not be present inside any value.
    Example:
        Content of key map file is as below. 
            abc Hello
            llo Hi
        if we have key 'abc' present any where, the value will be replaced as 'HeHi'.('llo' of 'Hello' will be replaced as 'Hi'.)
3) Only a single key and single value should be present in a single line.               
""")

proceed = input("press enter to continue.... or enter q to exit: ")
if proceed.strip() == 'q':
    print("Operation is cancelled!!!!!!!!!!!!!")
    exit(2)
print("\n")
if len(sys.argv) == 1:
    key_map = os.path.realpath(input("Enter the key-value pair file: ").strip())
    project_files = os.path.realpath(input("Enter the project directory: ").strip())
elif len(sys.argv) == 2:
    key_map = os.path.realpath(sys.argv[1])
    project_files = os.path.realpath(input("Enter the project directory: ").strip())
else:
    key_map = os.path.realpath(sys.argv[1])
    project_files = os.path.realpath(sys.argv[2])

print("\n")
print("Key-Value pair file: {}".format(key_map))
print("Project Directory: {}".format(project_files))
print("\n")

def get_dictionary_from_keys_file(key_map_file):
    try:
        key_map_data = {}
        fd = open(key_map_file, 'r')
        while True:
            msg = fd.readline().strip("\n").strip("\r").strip()
            if msg == '':
                break
            msg_tmp = msg.split(" ")
            msg_tmp = [x for x in msg_tmp if x != '']
            if len(msg_tmp) == 2:
                print("Key found {} with value {}".format(msg_tmp[0], msg_tmp[1]))
                key_map_data[msg_tmp[0]] = msg_tmp[1]
            else:
                print("Mapping error in line '{}'. Please mention single key and single value per line".format(msg))
        return key_map_data
    except Exception as ex:
        print("!!!!! Failed to check key_map file. {} !!!!!".format(ex.args))
        exit(1)


def replace_file(file_location, key_map_data):
    try:
        fd = open(file_location, 'r')
        msg = fd.read()
        fd.close()
        for key in key_map_data.keys():
            msg = msg.replace(key, key_map_data[key])
        fd = open(file_location,'w')
        fd.write(msg)
        fd.close()
        print("***** Successfully updated {} *****".format(file_location))
    except Exception as ex:
        print("!!!!! Failed to update {}.{} !!!!!".format(file_location,ex.args))

def recursive_update(destination,key_map_data):
    try:
        if os.path.isdir(destination):
            inside_files = os.listdir(destination)
            inside_files = [os.path.join(destination,x) for x in inside_files]
            for each_file in inside_files:
                recursive_update(each_file,key_map_data)
        else:
            replace_file(destination,key_map_data)
    except Exception as ex:
        print("!!!!! Failed to check {}.{} !!!!!!".format(destination,ex.args))



key_map_data = get_dictionary_from_keys_file(key_map)
print("\n")
recursive_update(project_files,key_map_data)
