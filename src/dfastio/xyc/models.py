"""XYC file reader and writer."""

from pathlib import Path

import geopandas as gpd
import numpy as np
import pandas as pd
import shapely.geometry.linestring as linestring
from shapely.geometry import LineString


class XYCModel:
    """Class for reading and writing XYC files."""

    @staticmethod
    def read(
        file_name: str,
        num_columns: int = 2,
        delimiter: str = None,
        has_header: bool = False,
    ) -> linestring.LineString:
        """
        Read lines from a file.

        Args:
            file_name (str):
                Name of the file to be read.
            num_columns (int):
                Number of columns to be read (2 or 3)
            delimiter (str):
                delimiter used in the file.
            has_header (bool):
                whether the file has a header.

        Returns:
            L : shapely.geometry.linestring.LineString
                Line strings.

        Examples:
            ```python
            >>> from dfastio.xyc.models import XYCModel
            >>> path = "examples/data/simple-xyc-file.xyc"
            >>> line = XYCModel.read(path, num_columns=3, delimiter=" ", has_header=True)
            >>> print(line)
            LINESTRING Z (5 6 4, 8 9 7, 11 12 10)

            ```
        """
        ext = Path(file_name).suffix
        if ext.lower() == ".xyc":
            if num_columns == 3:
                column_names = ["Val", "X", "Y"]
            else:
                column_names = ["X", "Y"]
            header = 0 if has_header else None
            if delimiter is not None:
                data = pd.read_csv(
                    file_name,
                    names=column_names,
                    skipinitialspace=True,
                    header=header,
                    delimiter=delimiter,
                )
            else:
                data = pd.read_csv(
                    file_name,
                    names=column_names,
                    skipinitialspace=True,
                    header=header,
                    sep=r"\s+",
                )

            num_points = len(data.X)
            x = data.X.to_numpy().reshape((num_points, 1))
            y = data.Y.to_numpy().reshape((num_points, 1))
            if num_columns == 3:
                z = data.Val.to_numpy().reshape((num_points, 1))
                coords = np.concatenate((x, y, z), axis=1)
            else:
                coords = np.concatenate((x, y), axis=1)
            coords_line_strig = LineString(coords)

        else:
            data_geometry = gpd.read_file(file_name)["geometry"]
            coords_line_strig = data_geometry[0]

        return coords_line_strig

    @staticmethod
    def write_xyc(xy: np.ndarray, val: np.ndarray, file_name: str) -> None:
        """
        Write a text file with x, y, and values.

        Arguments
        ---------
        xy : np.ndarray
            N x 2 array containing x and y coordinates.
        val : np.ndarray
            N x k array containing values.
        file_name : str
            Name of the file to be written.

        Returns
        -------
        None
        """
        with open(file_name, "w") as xyc:
            if val.ndim == 1:
                for i in range(len(val)):
                    val_str = "{:.2f}".format(val[i])
                    xyc.write(
                        "{:.2f}\t{:.2f}\t".format(xy[i, 0], xy[i, 1]) + val_str + "\n"
                    )
            else:
                for i in range(len(val)):
                    val_str = "\t".join(["{:.2f}".format(x) for x in val[i, :]])
                    xyc.write(
                        "{:.2f}\t{:.2f}\t".format(xy[i, 0], xy[i, 1]) + val_str + "\n"
                    )
