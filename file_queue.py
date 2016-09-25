import os

class FileQueue():
    """
    Simple queue using a file as storage, for persistence and accessibility. Accepts and returns strings.
    """
    def __init__(self, filename):
        self.filename = filename
        
    def touch_file(self):
        open(self.filename, 'a').close()

    def get(self):
        self.touch_file()
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        result = lines[:1]
        with open(self.filename, 'w') as f:
            f.writelines(lines[1:])
        result = result[0].rstrip() if result else None
        return result

    def put(self, str):
        self.touch_file()
        with open(self.filename, 'r') as f:
            lines = f.readlines()
        lines.append(str+os.linesep)
        with open(self.filename, 'w') as f:
            f.writelines(lines)

if __name__ == "__main__":
    q = FileQueue("test_queue")
