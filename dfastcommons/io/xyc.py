import os

import geopandas
import numpy
import pandas
import shapely.geometry.linestring


class XYCModel:
    """
    Class for reading and writing XYC files.
    """

    @staticmethod
    def read_xyc(
        filename: str, ncol: int = 2, delimiter=None, has_header=False
    ) -> shapely.geometry.linestring.LineString:
        """
        Read lines from a file.

        Arguments
        ---------
        filename : str
            Name of the file to be read.
        ncol : int
            Number of columns to be read (2 or 3)

        Returns
        -------
        L : shapely.geometry.linestring.LineString
            Line strings.
        """
        fileroot, ext = os.path.splitext(filename)
        if ext.lower() == ".xyc":
            if ncol == 3:
                colnames = ["Val", "X", "Y"]
            else:
                colnames = ["X", "Y"]
            header = 0 if has_header else None
            if delimiter is not None:
                P = pandas.read_csv(
                    filename,
                    names=colnames,
                    skipinitialspace=True,
                    header=header,
                    delimiter=delimiter,
                )
            else:
                P = pandas.read_csv(
                    filename,
                    names=colnames,
                    skipinitialspace=True,
                    header=header,
                    delim_whitespace=True,
                )

            nPnts = len(P.X)
            x = P.X.to_numpy().reshape((nPnts, 1))
            y = P.Y.to_numpy().reshape((nPnts, 1))
            if ncol == 3:
                z = P.Val.to_numpy().reshape((nPnts, 1))
                LC = numpy.concatenate((x, y, z), axis=1)
            else:
                LC = numpy.concatenate((x, y), axis=1)
            L = shapely.geometry.LineString(LC)

        else:
            GEO = geopandas.read_file(filename)["geometry"]
            L = GEO[0]

        return L

    @staticmethod
    def write_xyc(xy: numpy.ndarray, val: numpy.ndarray, filename: str) -> None:
        """
        Write a text file with x, y, and values.

        Arguments
        ---------
        xy : numpy.ndarray
            N x 2 array containing x and y coordinates.
        val : numpy.ndarray
            N x k array containing values.
        filename : str
            Name of the file to be written.

        Returns
        -------
        None
        """
        with open(filename, "w") as xyc:
            if val.ndim == 1:
                for i in range(len(val)):
                    valstr = "{:.2f}".format(val[i])
                    xyc.write(
                        "{:.2f}\t{:.2f}\t".format(xy[i, 0], xy[i, 1]) + valstr + "\n"
                    )
            else:
                for i in range(len(val)):
                    valstr = "\t".join(["{:.2f}".format(x) for x in val[i, :]])
                    xyc.write(
                        "{:.2f}\t{:.2f}\t".format(xy[i, 0], xy[i, 1]) + valstr + "\n"
                    )
