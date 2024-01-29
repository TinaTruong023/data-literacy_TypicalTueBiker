import pandas as pd
import os


def get_parent_directory(target_directory):
    """
    Find the parent directory containing the specified target directory.
    Parameters:
    - filepath: Starting filepath.
    - target_directory: Target directory to search for.
    Returns:
    - The filepath containing the target directory, or None if not found.
    """
    current_directory = os.getcwd()
    while True:
        # Check if the target directory exists in the current directory
        target_directory_path = os.path.join(current_directory, target_directory)
        if os.path.exists(target_directory_path) and os.path.isdir(target_directory_path):
            return current_directory
        # Move up one level in the directory hierarchy
        parent_directory = os.path.dirname(current_directory)
        # Check if we have reached the root directory
        if parent_directory == current_directory:
            return
        current_directory = parent_directory
def get_files_in_directory(directory_path):
    try:
        # List all files and directories in the given path
        files_and_directories = os.listdir(directory_path)
        # Filter only the files from the list
        files = [
            file for file in files_and_directories
            if os.path.isfile(os.path.join(directory_path, file))
        ]
        return files
    except OSError as e:
        print(f"Error reading directory: {e}")
def get_data_filepath(keywords: list, files, root_filepath):
    if not isinstance(keywords, list):
        raise TypeError(f"list of strings expected, got '{type(keywords).__name__}'")
    def get_one_dataset_filepath(keyword):
        for f in files:
            if keyword.lower() in f.lower():
                dataset_filepath = os.path.join(root_filepath, f)
                if not os.path.isfile(dataset_filepath):
                    raise FileNotFoundError(f"File not found: {dataset_filepath}")
                return dataset_filepath
    return {
        keyword:get_one_dataset_filepath(keyword)
        for keyword in keywords
    }

def to_datetime(df, affected_cols):
    for col in affected_cols:
        df[col] = pd.to_datetime(df[col], utc=True)
    return df

def is_subset(A, B):
    A_is_subset = True
    for a in A:
        if a not in B:
            A_is_subset = False
            break
    return A_is_subset


class EventsData:
    """
    Loads event data. Data categories are:
        "covid_date",
        "covid_info",
        "holiday",
        "lecture",
        "semester",
        "unibreak"
        "oepv",
        "schoolbreak"
    Use get_data(), then the individual datasets are accessed via their dict keys (categories).
    """
    def __init__(self):
        self.relative_filepath = "dat/evd"
        self.data_categories = [
            "covid_date",
            "covid_info",
            "holiday",
            "lecture",
            "semester",
            "unibreak",
            "oepv",
            "schoolbreak"
        ]
        self.data_filepaths = self.create_events_data_filepaths()
        self.data = self.get_data()

    def create_events_data_filepaths(self):
        root_dir = get_parent_directory(self.relative_filepath)
        path_to_data = os.path.join(root_dir,self.relative_filepath)
        csv_files = get_files_in_directory(path_to_data)
        fp = get_data_filepath(self.data_categories, csv_files, path_to_data)
        return fp
    def get_data(self):
        """Gets a list of dataframes from given filepaths.

        Args:
            filepaths (list): list of filepaths to the csv files

        Returns:
            list: list of csv data as dataframes
        """
        date_cols = ["start", "end"]
        data = {}
        for category, filepath in self.data_filepaths.items():
            df = pd.read_csv(filepath)
            if is_subset(date_cols, list(df.columns.values)):
                df = to_datetime(df, date_cols)
            data[category] = df
        return data

if __name__ == "__main__":
    events_data = EventsData()
    print(events_data.data["schoolbreak"][events_data.data["schoolbreak"]["name"]=="Fasnetferien"])
