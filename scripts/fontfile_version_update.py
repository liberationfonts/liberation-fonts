'''
Script to update fontfile version in dir
Usage : python3 fontfile_version_update.py <fontfile_dir_name> <new_version>
eg: python3 fontfile_version_update.py src 2.1.3
'''
import sys
import os

if len(sys.argv) > 1:
    try:
        
        os.chdir(sys.argv[1])
        for filename in os.listdir(os.getcwd()):
            
            to_version = sys.argv[2]
            from_version_list = to_version.split(".")
            from_version_list[-1] = str(int(from_version_list[-1])-1)
            from_version = ".".join(from_version_list)

            font_lines_list = None
            
            
            with open(filename) as fobj:
                font_lines_list = fobj.readlines()

            for x,font_line in enumerate(font_lines_list):
                if "Version: {}".format(from_version) in font_line:
                    font_lines_list[x] = font_lines_list[x].replace("Version: {}".format(from_version), "Version: {}".format(to_version))
                elif "Version {}".format(from_version) in font_line:
                    font_lines_list[x] = font_lines_list[x].replace("Version {}".format(from_version), "Version {}".format(to_version))
    
            with open(filename,"w") as fobj:
                fobj.writelines(font_lines_list)

            print("update {} form ver:{} to ver:{}".format(filename, from_version, to_version))
    except Exception as e:
        print("Invalid fontfile passed and params passed\n params <fontfile_name> <old_version> <new_version>")

else:
    print("please pass fontfile as args")