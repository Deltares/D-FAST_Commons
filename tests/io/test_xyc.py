from io import StringIO

import mock
import pytest

from dfastcommons.io.xyc import XYCModel


class Test_read_xyc:
    @pytest.fixture
    def setup_data(self):
        with mock.patch("os.path.splitext") as mock_splitext:
            mock_splitext.return_value = ("c:\\", ".XYC")
            yield self

    def test_read_xyc_with_header_with_chainages_custom_separator(self, setup_data):
        """
        read .xyc file with chainage
        With custom header and seperator.
        """
        data_string = """\
                        "A", "B", "C"
                        1, 2, 3
                        4, 5, 6
                        7, 8, 9
                        10, 11, 12
                        """
        string_io = StringIO(data_string)

        line = XYCModel.read_xyc(string_io, 3, ",", True)
        assert line.wkt == "LINESTRING Z (2 3 1, 5 6 4, 8 9 7, 11 12 10)"

    def test_read_xyc_with_header_without_chainages_custom_separator(self, setup_data):
        """
        read .xyc file without chainage (X,Y only)
        With custom header and seperator.
        """
        data_string = """\
                        "A", "B"
                        2, 3
                        5, 6
                        8, 9
                        11, 12
                        """
        string_io = StringIO(data_string)

        line = XYCModel.read_xyc(string_io, 2, ",", True)
        assert line.wkt == "LINESTRING (2 3, 5 6, 8 9, 11 12)"

    def test_read_xyc_with_header_with_chainages_no_custom_separator(self, setup_data):
        """
        read .xyc file with chainage
        With custom header and seperator.
        """
        data_string = """\
                        "A" "B" "C"
                        1 2 3
                        4 5 6
                        7 8 9
                        10 11 12
                        """
        string_io = StringIO(data_string)

        line = XYCModel.read_xyc(string_io, 3, has_header=True)
        assert line.wkt == "LINESTRING Z (2 3 1, 5 6 4, 8 9 7, 11 12 10)"

    def test_read_xyc_with_header_without_chainages_no_custom_separator(
        self, setup_data
    ):
        """
        read .xyc file without chainage (X,Y only)
        With custom header and seperator.
        """
        data_string = """\
                        "A" "B"
                        2 3
                        5 6
                        8 9
                        11 12
                        """
        string_io = StringIO(data_string)

        line = XYCModel.read_xyc(string_io, 2, has_header=True)
        assert line.wkt == "LINESTRING (2 3, 5 6, 8 9, 11 12)"

    def test_read_xyc_no_header_with_chainages_no_custom_separator(self, setup_data):
        """
        read .xyc file with chainage
        No header and no custom seperator.
        """
        data_string = """\
                        1 2 3
                        4 5 6
                        7 8 9
                        10 11 12
                        """
        string_io = StringIO(data_string)
        line = XYCModel.read_xyc(string_io, 3)

        assert line.wkt == "LINESTRING Z (2 3 1, 5 6 4, 8 9 7, 11 12 10)"

    def test_read_xyc_no_header_without_chainages_no_custom_separator(self, setup_data):
        """
        read .xyc file without chainage
        No header and no custom seperator.
        """
        data_string = """\
                        2 3
                        5 6
                        8 9
                        11 12
                        """
        string_io = StringIO(data_string)
        line = XYCModel.read_xyc(string_io, 2)

        assert line.wkt == "LINESTRING (2 3, 5 6, 8 9, 11 12)"

    def test_read_xyc_no_header_with_chainages_custom_separator(self, setup_data):
        """
        read .xyc file with chainage
        No header and custom seperator.
        """
        data_string = """\
                        1;2;3
                        4;5;6
                        7;8;9
                        10;11;12
                        """
        string_io = StringIO(data_string)
        line = XYCModel.read_xyc(string_io, 3, ";")

        assert line.wkt == "LINESTRING Z (2 3 1, 5 6 4, 8 9 7, 11 12 10)"

    def test_read_xyc_no_header_without_chainages_custom_separator(self, setup_data):
        """
        read .xyc file without chainage (X,Y only)
        No header and custom seperator.
        """
        data_string = """\
                        2;3
                        5;6
                        8;9
                        11;12
                        """
        string_io = StringIO(data_string)
        line = XYCModel.read_xyc(string_io, 2, ";")
        assert line.wkt == "LINESTRING (2 3, 5 6, 8 9, 11 12)"
