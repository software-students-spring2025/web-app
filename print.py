import os


def print_directory_contents(path, indent=''):
    # Loop over all the items in the directory
    for item in os.listdir(path):
        if (
            item == "node_modules"
            or item.startswith('.')
            or item == "assets"
            or item == "package-lock.json"
            or item == "locale"
            or item == "utility"
            or item == "mydbengine"
            or item == "LICENSE"
            or item == "requirements"
        ):
            continue
        if item == "cancellation.py" or item == "login.py" or item == "card.py":
            continue

        if item.startswith('ios') or item.startswith('android'):
            continue

        # Construct full path
        item_path = os.path.join(path, item)

        # Print the item name with appropriate indentation
        print(indent + '|-- ' + item)

        # If the item is a directory, recursively call the function
        if os.path.isdir(item_path):
            print_directory_contents(item_path, indent + '    ')
        # If the item is a file, read and print its contents
        elif os.path.isfile(item_path):
            try:
                with open(item_path, 'r') as file:
                    print(indent + '    |-- Content:')
                    for line in file:
                        print(indent + '    |   ' + line.strip())
            except Exception as e:
                print(indent + '    |-- Could not read file: ' + str(e))


# Set the starting directory
start_directory = '.'

# Call the function to print the directory contents
print_directory_contents(start_directory)
