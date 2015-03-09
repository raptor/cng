'''
This script will extract all files from .tar files in the Complete National
Geographic set as well decode the .cng files into .jpg files.

This script can also copy all resources from one directory to another,
decoding the cng files as it goes.

# TODO - develop a process to properly merge resources from a .tar file
into a folder where CNG resources are already found - this includes merging
of sqlite data, etc.
'''
import os
import sys
import tarfile


def decode_write_file(fileobj, path, output_path):
    b = bytearray(fileobj.read())
    
    # Handle CNG files differently, we'll convert to JPG
    if path[-4:].lower() == '.cng':
        jpg_file_name = path[:-4] + ".jpg"
        output_file = os.path.join(output_path, jpg_file_name)
    
        # Decoding is super simple
        for i in range(len(b)):
            b[i] ^= 0xEF
        
    else:
        output_file = os.path.join(output_path, path)
        
    # Create intermediate paths
    if not os.path.exists(os.path.dirname(output_file)):
        os.makedirs(os.path.dirname(output_file))
        
    print output_file
    
    # Now write out to file
    with open(output_file, "wb") as f:
        f.write(b)
        
    pass


def extract_decode_tar(tar_file_path, output_path):

    with tarfile.open(tar_file_path) as tar_file:
        for entry in tar_file:
            fileobj = tar_file.extractfile(entry)

            if not fileobj:
                continue
            
            decode_write_file(fileobj, entry.path, output_path)
                
    pass


def copy_decode_files(input_dir, output_dir):
    for root, _, filenames in os.walk(input_dir):
        for filename in filenames:
            relative_dir = os.path.relpath(root, input_dir)
            filepath = os.path.join(relative_dir, filename)
            
            with open(os.path.join(root, filename)) as fileobj:
                decode_write_file(fileobj, filepath, output_dir)
    
    pass


def main():
    # Debugging
#     input_resource = "/home/dbuck/temp/cng/disks/mnt/downloads/cngfixes2010.tar"
#     input_resource = "/home/dbuck/temp/cng/disks/mnt2/disc1"
#     output_dir = "/home/dbuck/temp/cng/output"
    
    if len(sys.argv) < 3:
        print "Usage 1: " + sys.argv[0] + " INPUT_DIR OUTPUT_DIR"
        print "Usage 2: " + sys.argv[0] + " INPUT_TAR_FILE OUTPUT_DIR"
        sys.exit(2)
          
    input_resource = sys.argv[1]
    output_dir = sys.argv[2]

    # Test if a tar file
    if input_resource[-4:].lower() == '.tar':
        print "Extracting files.  Will decode .cng to .jpg"
        extract_decode_tar(input_resource, output_dir)
        
    # Is a directory
    elif os.path.isdir(input_resource):
        print "Copying files.  Will decode .cng to .jpg"
        copy_decode_files(input_resource, output_dir)
        
    # Test if it is a single file?
    else:
        print "Input is not a .tar file or a directory!  Exiting..."
    
    pass


if __name__ == '__main__':
    main()
    pass
