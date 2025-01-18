import os

class FileHandle:
    def __init__(self, file_name):
        self.file_name = file_name
        self.check_file = self.check_file_name()
        self.file_contents = []

    def check_file_name(self):
        if os.path.exists(self.file_name):
            return True
        else:
            return False



    def write_to_file(self, text_array):
        with open(self.file_name, "w") as file:
            for text in text_array:
                file.write(f"{text}\n")
        print("The information is written successfully")

    def append_to_file(self, text_array):
        with open(self.file_name, "a") as file:
            for text in text_array:
                file.write(f"{text}\n")
        print("The information is added successfully")

    def update_file(self, line_update, new_data):
        status = False

        if self.check_file:
            # read file
            with open(self.file_name, "r") as file:
                # convert file into array for each line
                lines = [line.strip() for line in file]

                # check if line that need to be updated is exists if so, get the index of this
                # line in array
                for index, line in enumerate(lines):
                    if line_update in line:
                        line_index = index
                        # replace the old line with new data
                        lines[line_index] = new_data
                        # write data into file
                        with open(self.file_name, "w") as file:
                            for new_line in lines:
                                file.write(f"{new_line}")
                        print("The information is updated successfully")
                        status = True
                if not status:
                    print("The data is provided is not exists in the file")
        else:
            print("File not found")

    def delete_line(self, line_index):
        if self.check_file:
            # read file
            with open(self.file_name, "r") as file:
                # convert file into array for each line
                lines = [line.strip() for line in file]
                lines.pop(line_index)
                print(lines)
                # write data into file
                with open(self.file_name, "w") as file:
                    for line in lines:
                        file.write(f"{line}\n")
            print("The line is deleted successfully")
        else:
            print("File not found")


