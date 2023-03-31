import pandas as pd
import os
import yaml


def get_evaluated_month_filenames(folder: str) -> list[str]:
    """Returns list containing the file names from the evaluated months.

    Args:
        folder (str): Folder name that contains month csv files.

    Returns:
        List containing the file names from the evaluated months.
    """
    file_names = []
    for file in os.listdir(f"./{folder}"):
        if file.endswith(".csv") and "overview" in file:
            file_names.append(file)
    return file_names


def load_config(path: str) -> dict:
    """Load config yaml files.

    Args:
        path: Path to config file.

    Returns:
        The config file as a dict.
    """
    with open(path, "r") as ymlfile:
        cfg = yaml.safe_load(ymlfile)
    return cfg


def extract_expenditures_for_position(account_history_df: pd.DataFrame,
                                      position_identifiers: list[str],
                                      column_key: str
                                      ) -> pd.DataFrame:
    """Creates a dataframe containing only the expenditures to the 
    corresponding position (identified via the position identifiers).

    Args:
        account_history_df: The bank account dataframe.
        position_identifiers: list of strings identifying expenditures 
            for the corresponding position.
        column_key: The column name to look at.

    Returns:
        The dataframe containing the expenditures.
    """
    position_df = account_history_df[
        account_history_df[column_key].str.contains(
            '|'.join(position_identifiers),
            na=False
            )
        ]
    return position_df


def convert_column_to_float(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Converts a column in a dataframe to float

    Args:
        df: Dataframe containing the column to be converted.
        column: Column that will be converted.

    Returns:
        The converted dataframe
    """
    df[column].replace(',', '.', regex=True, inplace=True)
    df[column] = df[column].astype(float)
    return df


def remove_expenditures_from_account_history(account_history_df: pd.DataFrame,
                                             expenditures: str
                                             ) -> pd.DataFrame:
    """Removes the rows of the dataframe containing a certain string

    Args:
        account_history_df: dataframe to be processed
        expenditures: Expenditures string that will be checked

    Returns:
        Dataframe without rows containing the "position" string
    """
    df_new = account_history_df[
        account_history_df["Auftraggeber"].str.contains(
            '|'.join(expenditures)) == False
        ]
    return df_new


def add_expenditure_infos_to_overview_df(overview_df: pd.DataFrame,
                                         position: str,
                                         total_amount: int,
                                         number_of_expenditures: int
                                         ) -> pd.DataFrame:
    """Adds total amount and number of expenditures to the overview dataframe.

    Args:
        overview_df (pd.DataFrame): Overview dataframe.
        position (str): Position/class of the expenditures.
        total_amount (int): Total amount of the summed expenditures.
        number_of_expenditures (int): number of expenditures.

    Returns:
        The updated Overview dataframe.
    """
    index = overview_df.index[overview_df["Position"] == position].tolist()[0]
    overview_df.loc[index, 'Sum'] = total_amount
    overview_df.loc[index, 'counts'] = number_of_expenditures
    return overview_df
