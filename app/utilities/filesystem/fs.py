import os
import pathlib
import shutil
import tempfile
from os.path import basename
from pathlib import Path
from typing import Union, List
from zipfile import ZipFile

# from utilities.exceptions.exceptions import NestBaseException


def getDirPath(dir_name):
    """Returns the path to the dir_name

    Parameters
    ----------
    dir_name : str
        Name of the dir_name file

    Returns
    -------
    str
        Path to the dir_name file
    """
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + dir_name


def createDirectory(dir_or_file_path: str) -> str:
    if dir_or_file_path is None:
        raise
    print(f"Creating directories over the path: {dir_or_file_path}")
    file_dir_path = os.path.abspath(dir_or_file_path)
    Path(file_dir_path).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(file_dir_path):
        raise
    return file_dir_path


def copyFile(src: str, dst: str):
    if src is None or dst is None:
        raise
    return shutil.copy2(src, dst)


def fileSize(file_path: str) -> int:
    if file_path is None or os.path.exists(file_path) == False:
        raise
    fp = os.path.abspath(file_path)
    fs = os.path.getsize(fp)
    return fs


def exists(file_path: str) -> bool:
    if file_path is None:
        return False
    return os.path.exists(file_path)


def folderPath(file_path: str) -> bool:
    if file_path is None:
        return ""
    return str(Path(file_path).parent)


def extractFileExtension(file_path: str) -> Union[str, None]:
    if file_path is None:
        return None
    # function to return the file extension
    file_extension = pathlib.Path(file_path).suffix
    print(f"File Extension: {file_extension}")
    return file_extension


def extractFileNameWithoutExtension(file_path: str) -> Union[str, None]:
    if file_path is None:
        return None
    # function to return the file extension
    file_name_wo_ext = pathlib.Path(file_path).stem
    print(f"File name: {file_name_wo_ext}")
    return file_name_wo_ext


# Zip the files from given directory that matches the filter
# Example Usage:
#   zipFilesInDir('sampleDir', 'sampleDir2.zip', lambda name : 'csv' in name)
def zipFilesInDir(dirName, zipFileName, filter):
    # create a ZipFile object
    with ZipFile(zipFileName, 'w') as zipObj:
        # Iterate over all the files in directory
        for folderName, subfolders, filenames in os.walk(dirName):
            for filename in filenames:
                if filter(filename):
                    # create complete filepath of file in directory
                    filePath = os.path.join(folderName, filename)
                    # Add file to zip
                    zipObj.write(filePath, basename(filePath))


def zip(files_to_compress: List[str], zip_output_file: str):
    """
    Compresses given files-list in the given output file
    :param files_to_compress:
    :param zip_output_file:
    :return:
    """
    print(f"Files to compress: {files_to_compress} in {zip_output_file}")
    zip_obj = ZipFile(zip_output_file, 'w')
    for file_to_comp in files_to_compress:
        zip_obj.write(file_to_comp, basename(file_to_comp))
    return zip_output_file


def getTempDir():
    dn = tempfile.gettempdir()
    return dn
