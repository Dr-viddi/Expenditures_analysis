# Class for plotting datasets
import matplotlib.pyplot as plt
from utils import get_evaluated_month_filenames
import pandas as pd

class Plotter:
    
    def __init__(self, overview_df: pd.DataFrame) -> None:
        """Init the plotter class.

        Args:
            overview_df: Overview dataframe that contains the amount spent for each class.
        """
        self.overview_df = overview_df
    
    def print_line_chart(self, path: str, title: str) -> None:
        """Plots a line chart.

        Args:
            path: Outputh path of the line chart.
            title: Title of the line chart.
        """
        ax = self.overview_df.plot.line(figsize=(20, 10), title=title, grid=True,  marker='o').legend(loc='center left',bbox_to_anchor=(1.0, 0.5))
        plt.xlabel('Month')
        plt.ylabel('Euro')
        fig = ax.get_figure()
        fig.savefig(path)
        
    def print_bar_chart(self, path: str, title: str) -> None:
        """Plots a bar chart.

        Args:
            path: Outputh path of the bar chart.
            title: Title of the bar chart.
        """
        ax = self.overview_df.plot.bar(y='Sum', figsize=(20, 10), rot=0, title=title)
        for p in ax.patches:
            ax.annotate(str(p.get_height()), (p.get_x() * 1.005, p.get_height() * 1.005))
        fig = ax.get_figure()
        fig.savefig(path)
        
    def print_pie_chart(self, path: str, title: str) -> None:
        """Plots a pie chart.

        Args:
            path: Outputh path of the pie chart.
            title: Title of the pie chart.
        """
        ax = self.overview_df.plot.pie(y='Sum', figsize=(10, 10), autopct='%1.1f%%', title=title)
        fig = ax.get_figure()
        fig.savefig(path)

    def print_stacked_bar_chart(self, path: str, title: str) -> None:
        """Plots a stacked bar chart.

        Args:
            path: Outputh path of the bar chart.
            title: Title of the bar chart.
        """
        print(self.overview_df)
        total_spend = self.overview_df["Total"].to_list()
        self.overview_df.drop(["Total"], axis=1, inplace=True)
        ax = self.overview_df.plot.bar(stacked=True, figsize=(15, 10), title=title, grid=True)
        patches = ax.patches        

        # add total amount spent on the top of the stacked bars
        available_months_count = len(get_evaluated_month_filenames(folder=path))
        for index in range(available_months_count):
            ax.annotate(total_spend[index], (patches[index].get_x(), total_spend[index] + 40))      

        # add amount spent for each class in each stacked bar
        list_values = []
        for column in self.overview_df:
            list_values = list_values + self.overview_df[column].tolist()
        for rect, value in zip(patches, list_values):
            h = rect.get_height()/2.
            w = rect.get_width()/2.
            x, y = rect.get_xy()
            ax.text(x+w, y+h,value,horizontalalignment='center',verticalalignment='center')     

        # plot
        plt.xlabel('Month')
        plt.ylabel('Euro')
        plt.legend(bbox_to_anchor=(1.0, 1.0))
        fig = ax.get_figure()
        fig.savefig(path)