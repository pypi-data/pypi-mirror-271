from typing import List, Dict, Any
import numpy as np
from pytom3d.util import list_files

class Scan:

    def __init__(self, **kwargs: Dict['str', Any]) -> None:
        """
        Initialize a Scan object.

        Parameters
        ----------
        name : str, optional
            Name of the scan. If not provided, defaults to "Untitled".
        """
        try:
            self.name = kwargs.pop("name")
        except KeyError:
            self.name = "Untitled"

        try:
            self.color = kwargs.pop("color")
        except KeyError:
            self.color = "k"

        try:
            self.line = kwargs.pop("line")
        except KeyError:
            self.line = "-"

        try:
            self.alpha = kwargs.pop("alpha")
        except KeyError:
            self.alpha = 0.3

    def config_aspect(self, color, line, alpha):
        self.color = color
        self.line = line
        self.alpha = alpha

    def load_file(self, reader: callable, path: str, **kwargs: Dict['str', Any]) -> None:
        """
        Load data from a file.

        Parameters
        ----------
        reader : callable
            A function to read the data from the file.
        path : str
            The path to the file.
        **kwargs : dict
            Additional keyword arguments to pass to the reader function.
        """
        data = reader(path, **kwargs)
        self.x = data.iloc[:, 0].to_numpy()
        self.y = data.iloc[:, 1].to_numpy()
        self.y_err = data.iloc[:, 2].to_numpy()

    def load_data(self, x: np.ndarray, y: np.ndarray, y_err: np.ndarray = None) -> None:
        """
        Load data directly.

        Parameters
        ----------
        x : numpy.ndarray
            X-axis data.
        y : numpy.ndarray
            Y-axis data.
        y_err : numpy.ndarray
            Error associated with the y-axis data.
        """
        self.x = x
        self.y = y
        self.y_err = y_err


def export_line_scan(reader: callable, path: str, *scans: List, **kwargs:  Dict['str', Any]) -> None:
    """
    Export line scan data to an Excel file.

    Parameters
    ----------
    reader : callable
        A function to read line scan data.
    path : str
        The path to save the Excel file.
    *scans : tuple
        Variable length argument list of line scans.
    **kwargs : dict
        Additional keyword arguments to pass to the reader function.

    Returns
    -------
    None
    """
    for s in scans:
        data = reader(s, **kwargs)
        data.to_excel(path, index=False)