import os
import subprocess
import sys

def main():
    lib_directory = None

    # All Python Version that will be searched
    lib_major_version = 'lib_{}'.format(sys.version_info.major)
    lib_minor_version = '{}.{}'.format(lib_major_version, sys.version_info.minor)
    lib_micro_version = '{}.{}'.format(lib_minor_version, sys.version_info.micro)

    # Get all "lib" directories
    app_path = os.getcwd()
    contents = os.listdir(app_path)
    lib_directories = []
    for c in contents:
        # ensure content starts with lib, is directory, and is readable
        if c.startswith('lib') and os.path.isdir(c) and (os.access(c, os.R_OK)):
            lib_directories.append(c)

    # Find most appropriate FULL version
    if lib_micro_version in lib_directories:
        lib_directory = lib_micro_version
    elif lib_minor_version in lib_directories:
        lib_directory = lib_minor_version
    elif lib_major_version in lib_directories:
        lib_directory = lib_major_version
    else:
        # file most appropriate PARTIAL version
        for ld in lib_directories:
            if lib_micro_version in ld:
                lib_directory = ld
            elif lib_minor_version in ld:
                lib_directory = ld
            elif lib_major_version in ld:
                lib_directory = ld

    # No reason to continue if no valid lib directory found
    if lib_directory is None:
        print('Failed to find lib directory ({}).'.format(lib_directories))
        sys.exit(1)

    # Use this if you want to include modules from a subfolder
    # lib_path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile(inspect.currentframe()))[0], lib_directory)))
    lib_path = os.path.join(app_path, lib_directory)
    if 'PYTHONPATH' in os.environ:
        os.environ['PYTHONPATH'] = '{}{}{}'.format(lib_path, os.pathsep, os.environ['PYTHONPATH'])
    else:
        os.environ['PYTHONPATH'] = '{}'.format(lib_path)

    # Update system arguments
    sys.argv[0] = sys.executable
    sys.argv[1] = '{}.py'.format(sys.argv[1])

    # Make sure to exit with the return value from the subprocess call
    ret = subprocess.call(sys.argv)
    sys.exit(ret)

if __name__ == '__main__':
    main()
