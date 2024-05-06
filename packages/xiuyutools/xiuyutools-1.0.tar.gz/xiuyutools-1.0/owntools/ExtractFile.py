import os
import shutil

class ExtractFile:
    """ 
    Input Path & Pattern to extract files the match the pattern from the path's folders into this path 
    
    If pattern is none, extrcat all kind of files. 
    """

    def __init__(self, path, pattern):
        self.path = self._changePathForm(path)
        self.pattern = pattern

    def __call__(self, *args, **kwds):
        self.main()

    def _changePathForm(self, path: str):
        new_path = eval(repr(path).replace('\\', '/'))
        return new_path

    def _getCurrentFiles(self):
        return os.listdir(self.path)

    def _getFolders(self):
        currentFiles = self._getCurrentFiles()

        folderList = list()
        for file in currentFiles:
            if os.path.isdir(self._changePathForm(os.path.join(self.path, file))):
                print(file)
                folderList.append(file)

        return folderList

    def _extractFile(self, folder):
        forlderPath = self._changePathForm(os.path.join(self.path, folder))
        folderFiles = os.listdir(forlderPath)

        for file in folderFiles:
            if file.find(self.pattern) != -1:
                shutil.move(self._changePathForm(os.path.join(forlderPath, file)), self.path)
                print(f"Move: {file}")

    def main(self):
        forlders = self._getFolders()
        for forlder in forlders:
            self._extractFile(forlder)
