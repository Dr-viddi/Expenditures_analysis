from utils import load_config
from plotting import Month_Plotter, Year_Plotter
from loading import Loader
from processing import Dataframe_processor
from const import MONTHS

# load config
cfg = load_config("example_config.yml")

# init classes
loader = Loader(cfg)
processor = Dataframe_processor()

# create project folders
loader.make_dirs()

# create income df
income_df = loader.create_income_df_from_config()

# Create expenses of the year dataframe
overview_year_df = loader.create_expenses_year_dataframe()

# load account history
path = cfg["account_year_history"]
account_history_df = loader.load_dataframe(path)

# preprocess account history
column_to_be_processed = cfg["column_name_value"]
excluded_data = cfg["exclude_data"]
date_column = cfg["column_date"]
account_history_df = processor.remove_decimal_points(
    account_history_df,
    column_to_be_processed
    )
# remove income
account_history_df = processor.remove_positive_entries(
    account_history_df,
    column_to_be_processed
    )
account_history_df = processor.remove_entries(
    account_history_df,
    excluded_data
    )
account_history_df = processor.convert_column_to_datetime(
    account_history_df,
    date_column
    )

# split dataframe into monthly dataframes
processor.split_dataframes_according_to_months(
    account_history_df,
    cfg,
    date_column
    )

# Expenditures for each month
for month in MONTHS:

    # Create an empty overview dataset for a month containing only
    # the summed up expednitures
    month_overview_df = loader.create_month_overview_dataset()

    # load bank account history for a month
    path = cfg["base_dir"] + cfg[month]["subdir"] + "month_all.csv"
    account_month_df = loader.load_dataframe(path)

    column_containing_expenditure_identifiers = cfg["column_name_key"]
    column_containing_expenditure_values = cfg["column_name_value"]
    for position in cfg["positions"]:

        # load the identifiers for the position
        position_identifiers = cfg["positions"][position]

        # copy the entries of of the month bankacount df to a newly created
        # position df containing only the individual epcenditures
        position_df = processor.extract_rows_to_new_df(
            account_month_df,
            position_identifiers,
            column_containing_expenditure_identifiers
            )

        # convert entries
        position_df = processor.convert_column_to_float(
            position_df,
            column_containing_expenditure_values
            )

        # save dataset to disk
        path = cfg["base_dir"] + cfg[month]["subdir"] + position + ".csv"
        position_df.to_csv(path, sep=';')

        # compute number of positions and summed up expenditures
        number_of_expenditures = len(position_df)
        total_expenditure = position_df[
            column_containing_expenditure_values
            ].sum()

        # Add the positions and summed up expenditures to the month overview df
        month_overview_df = processor.add_value_to_df(
            month_overview_df,
            position,
            "Sum",
            total_expenditure
            )
        month_overview_df = processor.add_value_to_df(
            month_overview_df,
            position,
            "counts",
            number_of_expenditures
            )

        # Delete the rows that have be transfered to a position dataframe
        account_month_df = processor.remove_rows(
                account_month_df,
                cfg["column_name_key"],
                position_identifiers
            )

    # all expenditures which are not assigned to a class defined in the
    # config will be added to "Sonstiges" class
    month_overview_df.loc[len(month_overview_df)] = ["Sonstiges", 0, 0]

    account_month_df = processor.convert_column_to_float(
            account_month_df,
            column_containing_expenditure_values
            )

    number_of_expenditures = len(account_month_df)
    total_expenditure = account_month_df[
        column_containing_expenditure_values
        ].sum()

    month_overview_df = processor.add_value_to_df(
            month_overview_df,
            "Sonstiges",
            "Sum",
            total_expenditure
            )
    month_overview_df = processor.add_value_to_df(
            month_overview_df,
            "Sonstiges",
            "counts",
            number_of_expenditures
            )

    path = cfg["base_dir"] + cfg[month]["subdir"] + "Sonstiges.csv"
    account_month_df.to_csv(path, sep=';')

    # add external expenses, e.g. from other bank accounts
    for ext_position in cfg[month]["external positions"]:
        month_overview_df.loc[len(month_overview_df)] = [ext_position, 0, 0]
        month_overview_df = processor.add_value_to_df(
            month_overview_df,
            ext_position,
            "Sum",
            cfg[month]["external positions"][ext_position]
            )
        month_overview_df = processor.add_value_to_df(
            month_overview_df,
            ext_position,
            "counts",
            1
            )

    # change signs and index for a more convenient view
    month_overview_df = processor.make_values_absolut(
        month_overview_df,
        column='Sum'
        )
    month_overview_df.set_index('Position', inplace=True)

    # plot
    plotter = Month_Plotter(month_overview_df)
    path = cfg["base_dir"] + cfg[month]["subdir"] + "bar.pdf"
    plotter.print_bar_chart(path, f"Expenses {month}")

    path = cfg["base_dir"] + cfg[month]["subdir"] + "pie.pdf"
    plotter.print_pie_chart(path, f"Expenses {month}")

    # sum everything up
    month_overview_df = processor.sum_columns(month_overview_df)

    # save to disk
    path = cfg["base_dir"] + cfg[month]["subdir"] + "overview.csv"
    month_overview_df.to_csv(path, sep=';')

    # Append monthly overview to year dataframe
    overview_year_df[month] = month_overview_df["Sum"].to_list()

# year dataframe
overview_year_df.set_index('Position', inplace=True)
overview_year_df = overview_year_df.transpose()

# print
path = cfg["base_dir"] + "overview.csv"
overview_year_df.to_csv(path, sep=';')

# plot lines
plotter = Year_Plotter(overview_year_df, income_df)
path = cfg["base_dir"] + "summary_line.pdf"
plotter.print_line_chart(path, cfg["year"])

path = cfg["base_dir"] + "summary_bar.pdf"
plotter.print_stacked_bar_chart(path, cfg["year"])
