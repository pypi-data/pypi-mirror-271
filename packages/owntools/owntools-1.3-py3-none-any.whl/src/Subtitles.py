# Imports
import os,re
from typing import TypedDict
from .Common import change_path_form

class SrtToVtt():
    """Convert .srt file to .vtt file

    Args:
        inputfilename (path): the output file name based on the inputfile name, as well as the path.
    """

    def __init__(self, inputfilename):

        self.inputfilename = self._getInputPath(inputfilename)
        self.outputfilename = self._getOutputPath()

    def __call__(self):
        self.main()

    def _getInputPath(self, inputfilename):

        if inputfilename == None:
            print("Please enter the name of the file to open:", end=" ")
            inputfilename = input()

        done = False
        while done == False:
            if os.path.isfile(inputfilename):
                done = True
            else:
                print("File not found, please enter the filename:", end=" ")
                inputfilename = input()

        return inputfilename

    def _getOutputPath(self):
        """ Return the outputfilename depend on the inputfilename """

        path, name = os.path.split(self.inputfilename)
        # Get the file name with suffix
        name = os.path.splitext(name)[0]
        outputfilename = os.path.join(path, name+".vtt")
        return outputfilename

    def _getTransformedLine(self, line):
        if "-->" in line:
            return line.replace(",", ".")
        else:
            return line

    def main(self):

        # Open the file
        inputfile = open(self.inputfilename, "rb").read().decode("utf-8-sig").splitlines()

        output = open(self.outputfilename, "w")
        output.write("WEBVTT")
        output.write("\n\n")
        for line in inputfile:
            output.write(self._getTransformedLine(line))
            output.write("\n")
        # Close our output file
        output.close()

        print(f"Write Done : {self.outputfilename}")


class SubFuncs():
    """
    Normal Subtitll functions
    : getSubFolder()

    """

    def __init__(self, path: str):
        self.path = change_path_form(path)

    def getSubFolder(self):

        """Get the folders video name and sub name

        Returns:
            [dict]: {'fileName': '', 'subName': ''}
        """

        Type_folderData = TypedDict("Type_folderData", fileName=str, subName=str)

        videoSuffix = ['mp4', 'mkv', 'mov', 'avi']
        subSuffix = ['srt', 'ass']
        folderData: Type_folderData = dict()

        fileList: [str] = os.listdir(self.path)
        for file in fileList:
            for suffix in videoSuffix:
                if re.findall(f".{suffix}$",file):
                    folderData["fileName"] = file
                    break
            for suffix in subSuffix:
                if re.findall(f".{suffix}$", file):
                    folderData["subName"] = file
                    break

        return folderData


if __name__ == "__main__":
    test = SubFuncs("E:\Videos\Friends & 老友记\S10\es1")

