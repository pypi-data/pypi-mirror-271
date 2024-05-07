"""Useful functions"""
import os
import json
import numpy as np


def csv_to_json(file_directory, file_name, file_extension=".csv"):
    """Convert a CSV file to JSON in the same directory

    Keyword arguments:
    - file_directory -- location of file
    - file_name -- name of file
    - file_extension (Optional) -- extension of file"""

    filepath = os.path.join(file_directory, file_name + file_extension)
    filedat = np.loadtxt(filepath, delimiter=",")
    outdict = {}
    for column_index in range(filedat.shape[1]):
        outdict["column" + str(column_index + 1)] = filedat[
            :, column_index
        ].tolist()
    outfilepath = os.path.join(file_directory, file_name + ".json")
    with open(outfilepath, "w", encoding="utf8") as outfile:
        json.dump(outdict, outfile, indent=4)
