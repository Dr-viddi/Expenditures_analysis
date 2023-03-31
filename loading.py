from pathlib import Path
import pandas as pd
from const import MONTHS


class Loader:

    def __init__(self, cfg: dict) -> None:
        """Inits the class

        Args:
            cfg: Config file containing the configurations
        """
        self.cfg = cfg

    def make_dirs(self):
        """Creates for each month a subdirectory specified in the cfg file.
        """
        [Path(f"{self.cfg['base_dir']}/{month}").mkdir(
            parents=True,
            exist_ok=True
            ) for month in MONTHS]

    def load_dataframe(self, path):
        """Loads a dataframe from csv file.

        Args:
            path: Path to the csv file.

        Returns:
            The laoded dataframe.
        """
        dataframe = pd.read_csv(
            path,
            encoding='unicode_escape',
            sep=";",
            usecols=self.cfg["imported_bank_data"]
            )
        return dataframe

    def create_income_df_from_config(self):
        """Creates a dataframe containing the income.

        Returns:
            The dataframe
        """
        income = []
        months = []
        for month in MONTHS:
            income.append(sum(self.cfg[month]["income"]))
            months.append(month)
        return pd.DataFrame({'Income': income}, index=months)

    def create_month_overview_dataset(self):
        """Creates the a dataframe containing the expenses over a month.

        Returns:
            The dataframe.
        """
        overview_df = pd.DataFrame(
            list(self.cfg["positions"].keys()),
            columns=['Position']
            )
        overview_df['Sum'] = 0
        overview_df['counts'] = 0
        return overview_df

    def create_expenses_year_dataframe(self) -> pd.DataFrame:
        """Creates a dataframe containing the expenses over a year.

        Returns:
            The dataframe.
        """
        position_list = list(self.cfg["positions"].keys())
        position_list.append("Sonstiges")

        for ext_position in self.cfg["Jan"]["external positions"]:
            position_list.append(ext_position)
        position_list.append("Total")
        return pd.DataFrame(position_list, columns=['Position'])
