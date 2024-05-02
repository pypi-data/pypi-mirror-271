import os
import functools
import glob
import pickle
import numpy as np
import pandas as pd
import re
from typing import Tuple, List, Any

from pytom3d.stats import running_mean, running_std


def export_regressor(regressor, folder: str = "./", filename: str = "my_regressor", extension: str = ".rg",
                     excluded_keys: List[str] = [], forced_values: List[Any] = []) -> None:
    """
    Export the attributes of a regressor to a dictionary for storage or inspection.

    Parameters
    ----------
    regressor : object
        The regressor object to export.

    path_to_file : str, optional
        The path to the file for exporting the regressor attributes. Default is "./".

    excluded_keys : list of str, optional
        A list of attribute keys to be excluded from the exported dictionary.

    forced_values : list of any, optional
        A list of values to be used for attributes specified in `excluded_keys`.

    Returns
    -------
        The dictionary containing the attributes of the regressor.

    Raises
    ------
    AssertionError
        If the length of `excluded_keys` is not equal to the length of `forced_values`.

    Notes
    -----
        This function is provided for convenience to handle backward compatibility
        of scikit-learn.

    """
    regressor_dict = {}

    assert len(excluded_keys) == len(forced_values)

    for k in vars(regressor).keys():
        if k in excluded_keys:
            regressor_dict[k] = forced_values[excluded_keys.index(k)]
        else:
            regressor_dict[k] = vars(regressor)[k]

    save(regressor_dict, folder, filename, extension)
    return regressor_dict


def import_regressor(folder: str = "./", filename: str = "my_regressor.rg", init_regressor = None) -> dict:
    """
    Import a regressor's attributes from a saved file and update an initialized regressor object.

    Parameters
    ----------
    folder : str, optional
        The path to the folder containing the saved regressor attributes file. Default is "./".

    filename : str, optional
        The name of the file containing the saved regressor attributes. Default is "my_regressor.rg".

    init_regressor : object
        The initialized regressor object to be updated with the imported attributes.

    Returns
    -------
    dict
        A dictionary containing the imported regressor attributes.

    Notes
    -----
        This function is provided for convenience to handle backward compatibility
        of scikit-learn.

    """
    regressor_dict = load(folder, filename)

    for k in regressor_dict.keys():
        setattr(init_regressor, k, regressor_dict[k])

    return regressor_dict


def trials(regressor, mesh, n: int = 1, folder: str = "./") -> None:
    """
    Generate and save trial data using a Gaussian Process Regression model.

    Parameters
    ----------
    regressor :
        The regressor of the topography.
    mesh : Topography
        The topogrphy object containing mesh data points for prediction.
    n : int, optional
        Number of trials to generate (default is 1).
    folder : str, optional
        The folder path to save the trial data files (default is "./").

    Returns
    -------
    None

    """
    for h in range(1, n+1):
        pred, sigma = regressor.predict(mesh.P[:, 0:2], return_std=True)
        noise = np.random.normal(loc=0, scale=sigma)
        output = np.vstack([mesh.P[:, 0], mesh.P[:, 1], mesh.P[:, 2],
                           pred, np.clip(max(0, h-1), 0, 1)*noise]).T
        np.savetxt(folder+mesh.name+"_" + str(h) + ".txt", output)


def predict_at_node(xx, yy, regressor):
    """
    Predict the value at a specific node in a regression model.

    Parameters
    ----------
    xx : float
        The x-coordinate of the node.
    yy : float
        The y-coordinate of the node.
    regressor : numpy.ndarray
        The regression model containing node information.

    Returns
    -------
    float
        The predicted value at the specified node.

    Raises
    ------
    Exception
        If there is not exactly one node matching the specified coordinates.

    """
    node_id = np.where(np.isclose(regressor[:, 0], xx, atol=1e-8) & np.isclose(regressor[:, 1], yy, atol=1e-8))[0]
    xm = regressor[node_id][0]
    ym = regressor[node_id][0]

    print(node_id)
    print("x:", xm, xx)
    print("y:", ym, yy)

    if len(node_id) == 1:
        return regressor[node_id][0][3] + regressor[node_id][0][4]
    else:
        raise Exception("There must be only one node.")


def prediction_wrapper(regressor, x, y) -> Tuple[np.ndarray]:
    """
    Predict the target variable and its uncertainty for given x and y coordinates using a regressor.

    Parameters
    ----------
    regressor : Regressor
        The trained regressor model.
    x : float
        The x-coordinate for prediction.
    y : float
        The y-coordinate for prediction.

    Returns
    -------
    tuple
        A tuple containing the predicted value and its associated standard deviation (uncertainty).

    """
    p = np.array([x, y]).reshape(1, -1)
    pred, sigma = regressor.predict(p, return_std=True)
    return pred[0], sigma[0]


def save(obj, folder: str = "./", filename: str = "my_file", extension: str = ".bin") -> None:
    """
    Save the given object to a binary file using pickle.

    Parameters
    ----------
    - obj: Any
        The object to be saved.
    - folder: str, optional
        The directory path where the file will be saved. Default is "./".
    - filename: str, optional
        The name of the file to be saved. Default is "my_file".
    - extension: str, optional
        The file extension. Default is ".bin".

    Returns
    -------
    None

    """
    with open(folder + filename + extension, 'wb') as file:
        pickle.dump(obj, file)


def load(path: str = "./"):
    """
     Load an object from a binary file using pickle.

    Parameters
    ----------
    - path: str, optional
        The path of the file. Default is "./".

    Returns
    -------
    Any
        The loaded object.

    """
    with open(path, 'rb') as file:
        return pickle.load(file)


def list_files(folder: str = "./", extension: str = ".gpr") -> List[str]:
    """
    List files in a folder.

    Parameters
    ----------
    folder : str, optional
        Path to the folder to search for files. Default is "./".
    extension : str, optional
        File extension to filter files. Default is ".gpr".

    Returns
    -------
    List[str]
        A list of file paths with the specified extension in the folder.

    """
    folder_path = folder
    files = glob.glob(folder_path + '/*' + extension)
    return [file for file in files]


def recursive_search(path: str, extension: str = ".dat", match: str = None,
                     pop_first: bool = False, take_first: bool = False) -> List[str]:
    """
    Recursively search for files with a specified extension in a directory and its subdirectories,
    optionally filtering by a match string and returning a modified list based on flags.

    Parameters
    ----------
    path : str
        The path to the directory to search in.

    extension : str, optional
        The file extension to search for. Default is ".dat".

    match : str, optional
        A substring to match in the file names. Default is None.

    pop_first : bool, optional
        If True, remove and discard the first element of the resulting list. Default is False.

    take_first : bool, optional
        If True, return only the first matching file. Overrides pop_first. Default is False.

    Returns
    -------
    List[str]
        A list of file paths matching the specified criteria.

    """
    file_list = []
    for root, dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path.endswith(extension):
                if match is not None:
                    if match in file_path:
                        file_list.append(file_path)

    if pop_first == True:
        return sorted(file_list)[1:None]
    elif take_first == True:
        return sorted(file_list)[0]
    else:
        return sorted(file_list[0:None])


def gather_data(match: str, inp: List[int], out: int, path: str, *list_path: List[str]) -> None:
    """
    Load data from multiple files, extract specified columns, and save to an Excel file.

    Parameters
    ----------
    match : str
        A regular expression pattern to match against the file paths.

    inp : List[int]
        List of column indices to extract as input features.

    out : int
        Index of the column to extract as the output feature.

    path : str
        Path to the output Excel file.

    *list_path : List[str]
        Variable number of file paths containing the data.

    Returns
    -------
    None

    """
    n2c = {"0": "x", "1": "y"}
    df = pd.DataFrame()

    for p in list_path:
        list_idx = list_path.index(p)
        regex_idx = re.search(match, p).group(0)
        input_cols = np.load(p)[:, inp]
        output_col = np.load(p)[:, out]

        if list_idx == 0:
            for r in range(0,len(inp)):
                df.insert(r, n2c[str(r)], input_cols[:,r])
            df.insert(len(df.columns), regex_idx, output_col)
        else:
            df.insert(len(df.columns), regex_idx, output_col)

    df.to_excel(path, index=False)


def get_coordinates(inp: List[int], *list_path: List[str]) -> np.ndarray:
    """
    Load and return the specified columns as coordinates from the first file path provided.

    Parameters
    ----------
    inp : List[int]
        List of column indices to extract as coordinates.

    list_path : List[str]
        Variable number of file paths containing the data. Only the first file path is used.

    Returns
    -------
    np.ndarray
        An array containing the coordinates extracted from the specified columns of the first file.

    """
    return np.load(list_path[0])[:, inp]


def lite_dict(gpr_obj: Any):
    """
    Load lite version of the regressor.

    Parameters
    ----------
    gpr_obj : Any
        Object of the Gaussian Process Regressor.

    Returns
    -------
    Dict[str, Any]
        Dictionary containing selected parameters and training data.

    Notes
    -----
    This function loads a lite version of the Gaussian Process Regressor
    by extracting specific parameters and training data for testing purposes.

    """
    gpr_ = load(gpr_obj)
    keys = ["k1__k1__constant_value", "k1__k1__constant_value_bounds",
            "k1__k2__length_scale", "k1__k2__length_scale_bounds",
            "k2__noise_level", "k2__noise_level_bounds"]
    values = [gpr_.kernel_.get_params()[k] for k in keys]
    params_dict = dict(zip(keys, values))
    data_dict = {"X_train_": gpr_.X_train_,
                 "y_train_": gpr_.y_train_}
    params_dict.update(data_dict)
    return params_dict


def update(method: callable):
    """
    Decorator to update edges, centroid, cardinality, and record history after executing a method.

    Parameters
    ----------
    method : callable
        The method to be decorated.

    Returns
    -------
    callable
        Decorated method.

    Notes
    -----
    This decorator assumes that the decorated method returns a list of tuples,
    where each tuple contains key-value pairs to be recorded in the event history.

    """
    @functools.wraps(method)
    def wrapper(self, *args, **kwargs) -> None:
        """
        Wrapper function to update edges, centroid, cardinality, and record history.

        Parameters
        ----------
        self : object
            Instance of the class.
        *args : tuple
            Positional arguments passed to the decorated method.
        **kwargs : dict
            Keyword arguments passed to the decorated method.

        Returns
        -------
        None

        Raises
        ------
        Any exceptions raised by the decorated method.

        Notes
        -----
        This wrapper assumes that the decorated method returns a list of tuples,
        where each tuple contains key-value pairs to be recorded in the event history.
        """
        # retrive values the method returns
        data = method(self, *args, **kwargs)

        # update edges, centroid, and cardinality
        self.edges()
        self.centroid()
        self.cardinality()

        # structure data for history
        event = {}
        for d in data:
            event[d[0]] = d[1]

        self.history_.append(event)
    return wrapper


def contour_data_wrapper(path: str, match: str) -> Tuple[np.ndarray]:
    """
    Wrapper function for generating contour data.

    Parameters
    ----------
    path : str
        Path to the directory containing data files.
    match : str
        A string used to match the desired data files.

    Returns
    -------
    Tuple[np.ndarray]
        A tuple containing the x-coordinates, y-coordinates, mean value, and standard deviation.

    """
    data = recursive_search(path, match=match, pop_first=True, take_first=False)

    mean = running_mean(3, None, *data)
    std = running_std(3, None, 1, *data)
    x, y = get_coordinates([0], *data), get_coordinates([1], *data)

    return x.reshape(-1), y.reshape(-1), mean, std


def scan_data_wrapper(path: str, match: str) -> Tuple[np.ndarray]:
    """
    Wrapper function for generating scan data.

    Parameters
    ----------
    path : str
        Path to the directory containing data files.
    match : str
        A string used to match the desired data files.

    Returns
    -------
    Tuple[np.ndarray]
        A tuple containing the x-coordinates, mean value, and standard deviation.

    """
    data = recursive_search(path, match=match, pop_first=True, take_first=False)

    mean = running_mean(3, None, *data)
    std = running_std(3, None, 1, *data)
    x = get_coordinates([0], *data)

    return x.reshape(-1), mean, std
