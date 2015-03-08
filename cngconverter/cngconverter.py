'''
This script will extract all files from .tar files in the Complete National
Geographic set as well decode the .cng files into .jpg files.
'''
import fnmatch
import os
import sys
import tarfile


def extract_decode_tar(tar_file_path, output_path):

    print "Extracting files.  Will decode .cng to .jpg: " + tar_file_path
    with tarfile.open(tar_file_path) as tar_file:
        for entry in tar_file:
            fileobj = tar_file.extractfile(entry)

            if not fileobj:
                continue
            
            b = bytearray(fileobj.read())
            
            # Handle CNG files differently, we'll convert to JPG
            if fnmatch.fnmatch(entry.path, '*.cng'):
                path_array = entry.path.split(os.sep)
                file_name = os.path.splitext(path_array[-1])[0] + ".jpg"
                output_file = output_path + os.sep + path_array[-3] + os.sep + path_array[-2] + os.sep + file_name
            
                # Decoding is super simple
                for i in range(len(b)):
                    b[i] ^= 0xEF
                
            else:
                output_file = output_path + os.sep + entry.path
                
            # Create intermediate paths
            if not os.path.exists(os.path.dirname(output_file)):
                os.makedirs(os.path.dirname(output_file))
                
            print output_file
            
            # Now write out to file
            with open(output_file, "wb") as f:
                f.write(b)
                
    pass


def main():
    if len(sys.argv) < 3:
        print "Usage: " + sys.argv[0] + " INPUT_TAR_FILE OUTPUT_DIR"
        sys.exit(2)
         
    input_tar = sys.argv[1]
    output_dir = sys.argv[2]

    extract_decode_tar(input_tar, output_dir)
    
    pass


if __name__ == '__main__':
    main()
    pass
