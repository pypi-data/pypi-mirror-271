import pkg_resources
import sys

def main():
    # Printing the libraries used
    print("Listing all installed libraries:")
    installed_packages = pkg_resources.working_set
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    for m in installed_packages_list:
        print(m)
    
    # Thanking the authors
    print("\nThank you to all the authors of the libraries used in this project!")

if __name__ == '__main__':
    sys.exit(main())
