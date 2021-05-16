# IMPORTS
import os
from tkinter import filedialog
from tkinter import *
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import itertools
plt.style.use('ggplot')
import glob

class Tester(object):

    def __init__(self):

        self._tested_path = None
        self.root_dataframe = None

        self.office_f_lst = []
        self.office_type_occurrneces_dct = {}
        self.office_types_dataframe = None
        self.office_ext_lst = ["dot", "doc", "wbk", "dotx", "docm", "dotm", "docb", "xls", "xlt",
                               "xlm", "xlsm", "xltx", "xltm", "xlsb", "xla", "xlam", "xll", "xlw",
                               "ppt", "pot", "pps", "pptm", "potx", "potm", "docx", "pptx", "xlsx",
                               "ppam", "ppsx", "ppsm", "sldx", "sldm", "ACCDB", "ACCDE", "ACCDT",
                               "ACCDR", "one", "pub", "xps", "txt"]

        self.img_f_lst = []
        self.img_type_occurrneces_dct = {}
        self.img_types_dataframe = None
        self.img_ext_lst = ["jpg", "png", "gif", "webp", "tiff", "psd", "raw", "bmp", 'heif', "indd",
                            "jpeg", "jpe", "jif", "jfif", "jfi", "tiff", "tif", "arw", "cr2", "nrw", "k25",
                            "dib", "heif", "heic", "ind", "indt", "jp2", "j2k", "jpf", "jpx", "jpm", "mj2",
                            "svg", "svgz", "ai", "eps", "pdf"]
        self.gis_f_lst = []
        self.gis_type_occurrneces_dct = {}
        self.gis_types_dataframe = None
        self.gis_ext_lst = ["shp", "dbf", "shx", "geojson", "json", "gml", "kml", "kmz", "gpx", "vct", "vdc",
                            "tab", "dat", "id", "map", "ind", "osm", "dlg", "img", "asc", "tif", "tiff", "ovr",
                            "rst", "rdc", "bil", "bip", "bsq", "pix", "ecw", "jp2", "sid", "sdw", "gdb", "mdb",
                            "gpkg", "mbtiles", "vmds", "sl3", "sqlite", "las", "lasd", "laz", "xyz", "dwf", "dwg",
                            "dxf", "dgn", "dwm", "dt0", "dt1", "dt2", "url", "xml", "nc", "hdf", "grib", "mxd",
                            "qgs", "arpx", "qgz", "mxt", "wor", "mws", "3dd", "sxd", "map", "lyr", "lyrx", "qlr",
                            "styl", "stylx", "qml", "dae", "skp", "e00", "e01", "e02", "mif", "mid", "mpk", "tbx",
                            "sde", "avf"]


    def path_selection(self):

        root = Tk()
        root.withdraw()
        root.filename = filedialog.askdirectory(title="Select directory")
        self._tested_path = root.filename
        return self._tested_path

    def list_all_files(self):

        # creates multiple generators for every iteration in each list comprehension.
        it = itertools.tee(glob.iglob(self._tested_path + '/**/**', recursive=True), 3)

        self.img_f_lst = [file.replace("/", "\\") for file in it[0] if
                          len(file.split(".")) == 2 and file.split(".")[-1] in self.img_ext_lst]

        self.office_f_lst = [file.replace("/", "\\") for file in it[1] if
                             len(file.split(".")) == 2 and file.split(".")[-1] in self.office_ext_lst]

        self.gis_f_lst = [file.replace("/", "\\") for file in it[2] if
                          len(file.split(".")) == 2 and file.split(".")[-1] in self.gis_ext_lst]

        # get reed of all unnecessary duplicates.
        self.img_f_lst = list(dict.fromkeys(self.img_f_lst))
        self.office_f_lst = list(dict.fromkeys(self.office_f_lst))
        self.gis_f_lst = list(dict.fromkeys(self.gis_f_lst))

        return self.img_f_lst, self.office_f_lst, self.gis_f_lst

    def in_type_statistic(self):

        # get just the extensions
        just_office_ext = [e.split(".")[-1] for e in self.office_f_lst]
        just_img_ext = [e.split(".")[-1] for e in self.img_f_lst]
        just_gis_ext = [e.split(".")[-1] for e in self.gis_f_lst]

        # creating a dict of ext type and occurrences
        for t in self.office_ext_lst:
            occ = just_office_ext.count(t)
            self.office_type_occurrneces_dct.update({t: [occ]})

        for t in self.img_ext_lst:
            occ = just_img_ext.count(t)
            self.img_type_occurrneces_dct.update({t: [occ]})

        for t in self.gis_ext_lst:
            occ = just_gis_ext.count(t)
            self.gis_type_occurrneces_dct.update({t: [occ]})

        return self.office_type_occurrneces_dct, self.img_type_occurrneces_dct, self.gis_type_occurrneces_dct


    def general_dataframe_create(self):

        self.root_dataframe = pd.DataFrame([self.office_f_lst, self.img_f_lst, self.gis_f_lst], index=["office", "img", "gis"])
        self.office_types_dataframe = pd.DataFrame.from_dict(self.office_type_occurrneces_dct, orient='index')
        self.img_types_dataframe = pd.DataFrame.from_dict(self.img_type_occurrneces_dct, orient='index')
        self.gis_types_dataframe = pd.DataFrame.from_dict(self.gis_type_occurrneces_dct, orient='index')

        return self.root_dataframe, self.office_types_dataframe, self.img_types_dataframe, self.gis_types_dataframe

    def visualization(self):
        # because every row in the dataframe represent the oll type of files, i will plot on the counting of "axis=1"
        # which is by every row for itself and not by every column at the root_dataframe.
        # about the other dataframes, i creates them from dict, so the 'counting' have been done before the data frame
        # creates. therefor the counting will be represent by the column '0'. (for understanding, print
        # the dataframes)

        # creating a figures for every bar plot.
        fig1 = plt.figure(figsize=(10, 15))
        fig2 = plt.figure(figsize=(10, 15))
        fig3 = plt.figure(figsize=(10, 15))
        fig4 = plt.figure(figsize=(10, 15))

        # creating the axes for every figure.
        ax1 = fig1.add_subplot(1, 1, 1)
        ax2 = fig2.add_subplot(1, 1, 1)
        ax3 = fig3.add_subplot(1, 1, 1)
        ax4 = fig4.add_subplot(1, 1, 1)

        # axes 1: root bar plot (general)
        ax1.bar(self.root_dataframe.index, self.root_dataframe.count(axis=1), color=['green', 'red', 'blue'])
        ax1.set_title('General compare')
        ax1.set(xlabel='Types', ylabel='Appearances')

        # axes 2: office bar plot
        ax2.bar(self.office_types_dataframe.index, self.office_types_dataframe[0], color='green')
        ax2.set_title('Office types compare')
        ax2.tick_params(axis='x', direction='out', pad=10, labelsize='small', labelrotation=90)


        # axes 3: img bar plot
        ax3.bar(self.img_types_dataframe.index, self.img_types_dataframe[0], color='red')
        ax3.set_title('Img types compare')
        ax3.tick_params(axis='x', direction='out', pad=10, labelsize='small', labelrotation=90)


        # axes 4: gis bar plot
        ax4.bar(self.gis_types_dataframe.index, self.gis_types_dataframe[0], color='blue')
        ax4.set_title('Gis types compare')
        ax4.tick_params(axis='x', direction='out', pad=10, labelsize='small', labelrotation=90)


        plt.show()

def main():
    test = Tester()
    test.path_selection()
    test.list_all_files()
    test.in_type_statistic()
    test.general_dataframe_create()
    test.visualization()


if __name__ == '__main__':
    main()