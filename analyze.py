import pandas as pd
from utils import (load_config, accumulate_expenditure, remove_expenditures_from_account_history, add_expenditure_infos_to_overview_df)
from plotter import Plotter

# load config
cfg = load_config("config.yml")

for month in cfg["paths"]["months"]:
    # load data
    month_dir = cfg["paths"]["months"][month]["dir"]
    cvs_filepath = month_dir + cfg["paths"]["months"][month]["cvs"]
    account_history = pd.read_csv(cvs_filepath,
                                  encoding= 'unicode_escape',
                                  sep=";",
                                  usecols=cfg["imported_bank_data"]
                                  )

    # delete positions not to be consierered, eg. income
    for column in cfg["exclude_data"]:
        excluded_positions= cfg["exclude_data"][column]
        for excluded_position in excluded_positions:
            account_history = account_history[account_history[column] != excluded_position]

    # create overiew dataset containg the positions as rows
    overview_df = pd.DataFrame(list(cfg["positions"].keys()), columns =['Position'])
    overview_df['Sum'] = 0
    overview_df['counts'] = 0

    # adding expenditures for each position class
    for position in cfg["positions"]:
        output_path = month_dir + position + ".csv"
        position_identifiers = cfg["positions"][position]
        column_containing_expenditure_identifiers = cfg["column_name_key"]
        column_containing_expenditure_values = cfg["column_name_value"]
        total_expenditure, number_of_expenditures, df_position = accumulate_expenditure(account_history, 
                                                                                        position_identifiers,
                                                                                        column_containing_expenditure_identifiers,
                                                                                        column_containing_expenditure_values
                                                                                        )
        account_history = remove_expenditures_from_account_history(account_history, position_identifiers)
        overview_df = add_expenditure_infos_to_overview_df(overview_df, position, total_expenditure, number_of_expenditures)
        df_position.to_csv(output_path, sep=';')
    overview_df['Sum'] = overview_df['Sum'].astype('int') # prevent numerical issues when saving to CSV

    # all expenditures which are not assigned to a class defined in the config will be added to "misc" class
    output_path = month_dir + "misc.csv"
    account_history.to_csv(output_path, sep=';')

    # change signs and index for a more convenient view
    overview_df['Sum'] = overview_df['Sum'].abs()
    overview_df.set_index('Position', inplace=True)

    # plot
    pltr = Plotter(overview_df)
    output_path = month_dir + "bar.pdf"
    pltr.print_bar_chart(output_path, "blubb")

    output_path = month_dir + "pie.pdf"
    pltr.print_pie_chart(output_path, "blubb")

    # sum everything up and save overview_df to disk
    overview_df.loc[len(overview_df)] = overview_df.sum()
    overview_df.rename(index={len(cfg["positions"]):'Total'},inplace=True)
    output_path = month_dir + "overview.csv"
    overview_df.to_csv(output_path, sep=';')




# todo: 
# Auftraggeber / Begünstiger -> Umaut Ü mit einbeziehen
# add year evaluation
# refactor position and expedniture word