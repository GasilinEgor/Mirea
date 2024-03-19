import zipfile
import argparse
import os


class VShell:
    def __init__(self, fileSystem):
        self.currentDirectory = 'directory/'
        self.fileSystem = fileSystem
        self.files = []
        self.zipFile = None

    def run(self):
        self.open()
        while True:
            command = input(f"{self.currentDirectory} $ ")
            if command == "exit":
                break
            self.commands(command)
        self.close()

    def commands(self, command):
        com = command.split()
        if len(com) > 0:
            if com[0] == 'pwd':
                print("Текущая директория:", self.currentDirectory)
            elif com[0] == 'ls':
                self.allFiles()
            elif com[0] == 'cd' and len(com) > 1:
                self.next(com[1])
            elif com[0] == 'cat' and len(com) > 1:
                self.read(com[1])
            else:
                print(f"Command {com[0]} not found")

    def allFiles(self):
        files = self.getLevelFiles()
        for item in files:
            if item != '':
                print(item)

    def next(self, directory):
        if directory == '..' and self.currentDirectory != 'directory/':
            newDirectory = ""
            dirs = self.currentDirectory.split('/')
            for i in range(len(dirs) - 2):
                newDirectory += dirs[i] + '/'
            self.currentDirectory = newDirectory
            return
        elif directory == '..':
            print("Вы находитесь в начальной директории!")
            return
        files = self.getLevelFiles()
        for item in files:
            if directory == item and len(directory.split('.')) < 2:
                self.currentDirectory += directory + '/'
                return
            elif len(directory.split('.')) >= 2:
                print("Файл не является директорией!")
                return

        print(f"Директория {directory} не найдена!")

    def getLevelFiles(self):
        files = set()
        level = self.currentDirectory.split('/')
        for item in self.zipFile.namelist():
            file = item.split('/')
            if len(file) >= len(level) and file[len(level) - 2] == level[-2]:
                files.add(file[len(level) - 1])
        return files

    def read(self, filename):
        file_path = os.path.join(self.currentDirectory, filename)
        if file_path in self.zipFile.namelist():
            with self.zipFile.open(file_path) as file:
                content = file.read()
                print(content.decode('utf-8', errors='replace'))
        else:
            print("Файл не найден!")

    def open(self):
        self.zipFile = zipfile.ZipFile(self.fileSystem, 'r')

    def close(self):
        if self.zipFile is not None:
            self.zipFile.close()
            self.zipFile = None


def readTextFile(name):
    with open(name, "r", encoding='UTF-8') as file:
        f = file.read()
        print(f)


def main():
    print("Hello, World!")
    parser = argparse.ArgumentParser(description="VShell")
    parser.add_argument('file', type=str, help='Описание позиционного аргумента')
    parser.add_argument('--script', type=str, help='Описание опционального аргумента')

    args = parser.parse_args()

    readTextFile(args.script)
    shell = VShell(args.file)
    shell.run()


if __name__ == '__main__':
    main()
