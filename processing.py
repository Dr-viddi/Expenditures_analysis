import pandas as pd
import calendar
from const import (MONTHS, MONTHS_STR_NR)
pd.options.mode.chained_assignment = None  # default='warn'


class Dataframe_processor:

    def __init__(self) -> None:
        """Init function
        """
        pass

    @staticmethod
    def remove_decimal_points(dataframe: pd.DataFrame,
                              column: str
                              ) -> pd.DataFrame:
        """Removes the decimal point in all entries of the provided column.

        Args:
            dataframe: Dataframe that contains the column.
            column: Column for which the decimal points are removed.

        Returns:
            The processed dataframe.
        """
        dataframe[column] = dataframe[column].str.replace('.', '')
        return dataframe

    @staticmethod
    def convert_column_to_float(dataframe: pd.DataFrame,
                                column: str
                                ) -> pd.DataFrame:
        """Converts a column in a dataframe to float.

        Args:
            dataframe: Dataframe containing the column to be converted.
            column: Column that will be converted.

        Returns:
            The processed dataframe.
        """
        dataframe[column].replace(',', '.', regex=True, inplace=True)
        dataframe[column] = dataframe[column].astype(float)
        return dataframe

    @staticmethod
    def remove_positive_entries(dataframe: pd.DataFrame,
                                column: str
                                ) -> pd.DataFrame:
        """Removes all positive entries in a dataframe column.

        Args:
            dataframe: Provided dataframe.
            column: Column that will be converted.

        Returns:
            The processed dataframe.
        """
        dataframe = dataframe[dataframe[column].str.contains("-")]
        return dataframe

    @staticmethod
    def remove_entries(dataframe: pd.DataFrame,
                       exclude_data: dict
                       ) -> pd.DataFrame:
        """Removes all entries in the dataframe specified in the
        exclude_data dict.

        Args:
            dataframe: Dataframe to be processed.
            exclude_data: Json file that specifies the excluded data.

        Returns:
            The processed dataframe.
        """
        for column in exclude_data:
            for excluded_position in exclude_data[column]:
                dataframe = \
                    dataframe[dataframe[column] != excluded_position]
        return dataframe

    @staticmethod
    def convert_column_to_datetime(dataframe: pd.DataFrame,
                                   column: str
                                   ) -> pd.DataFrame:
        """Converts the column to dataframe format.

        Args:
            dataframe: Dataframe to be processed.
            column: Column to be prcoessed.

        Returns:
            The processed dataframe.
        """
        dataframe[column] = pd.to_datetime(dataframe[column], dayfirst=True)
        return dataframe

    @staticmethod
    def split_dataframes_according_to_months(dataframe: pd.DataFrame,
                                             cfg: dict,
                                             date_column: str
                                             ) -> None:
        """Splits the dataframe in 12 dataframes, one for each month.

        Args:
            dataframe: Dataframe to be splitted.
            cfg: Config file.
            date_column: Column that contains the dates of the expenses.
        """
        for index, month in enumerate(MONTHS_STR_NR):
            last_day_of_month = str(
                calendar.monthrange(cfg["year"], index+1)[1]
                )
            start_date = f'{cfg["year"]}-{month}-01'
            end_date = f'{cfg["year"]}-{month}-{last_day_of_month}'
            mask = (dataframe[date_column] >= start_date) & \
                (dataframe[date_column] <= end_date)
            month_df = dataframe.loc[mask]
            output_path = cfg["base_dir"] + "/" + MONTHS[index] + \
                "/" + "month_all.csv"
            month_df.to_csv(output_path, sep=';')

    @staticmethod
    def extract_rows_to_new_df(dataframe: pd.DataFrame,
                               identifiers: list[str],
                               column: str
                               ) -> pd.DataFrame:
        """Extracts rows (identified via the identifiers) and copies them to
        a newly created dataframe.

        Args:
            dataframe: The bank account dataframe.
            identifiers: list of strings identifying the rows.
            column: The column name to look at.

        Returns:
            The dataframe containing the expenditures.
        """
        position_df = dataframe[dataframe[column].str.contains('|'.join(
            identifiers),
            na=False
            )]
        return position_df

    @staticmethod
    def remove_rows(dataframe: pd.DataFrame,
                    column: str,
                    strings_in_row: list[str]
                    ) -> pd.DataFrame:
        """Removes the rows of the dataframe containing a certain string

        Args:
            dataframe: Dataframe to be processed
            column: Column that possibiliy contains the values to be removed.
            strings_in_row: String that will be checked if it is in the column

        Returns:
            Dataframe without rows containing the strings
        """
        df_new = dataframe[dataframe[column].str.contains(
            '|'.join(strings_in_row)
            ) == False]
        return df_new

    @staticmethod
    def add_value_to_df(dataframe: pd.DataFrame,
                        position: str,
                        column: str,
                        value: int
                        ) -> pd.DataFrame:
        """Adds the value to the column at index specified by position
        Args:
            dataframe: Overview dataframe.
            position: Position/class of the expenditures.
            column: Column to be changed.
            value: Value of the entry.
        Returns:
            The updated Overview dataframe.
        """
        index = dataframe.index[dataframe["Position"] == position].tolist()[0]
        dataframe.loc[index, column] = value
        return dataframe

    @staticmethod
    def make_values_absolut(dataframe: pd.DataFrame,
                            column: list
                            ) -> pd.DataFrame:
        """Applies abs() to all values in the column.

        Args:
            dataframe: Dataframe to be processed.
            column (list): Column to be processed.

        Returns:
            The processed dataframe.
        """
        dataframe[column] = dataframe[column].astype('int')
        dataframe[column] = dataframe[column].abs()
        return dataframe

    @staticmethod
    def sum_columns(dataframe: pd.DataFrame) -> pd.DataFrame:
        """Sums up the values of all columns.

        Args:
            dataframe: Dataframe to be processed.

        Returns:
            The processed dataframe.
        """
        dataframe.loc[len(dataframe)] = dataframe.sum()
        dataframe.rename(index={len(dataframe)-1: 'Total'}, inplace=True)
        return dataframe
