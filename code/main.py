import pandas as pd
from manipulator import DataManipulator
from viz import Visualizer
import arg_parse
import html 
import webbrowser as wb

DF_PATH = 'netflix_titles_after_eda.csv'
DATE_COLUMN = 'date_added'
HTML_PATH = 'plot_of_netflix.html'


def load_data(file_path, date_column):

    #Load data from a CSV file and convert the specified column to datetime.
    
    try:
        df = pd.read_csv(file_path)
        df[date_column] = pd.to_datetime(df[date_column])
        return df
    except FileNotFoundError:
        print(f"File not found at path: {file_path}")
        return None
    except pd.errors.ParserError:
        print(f"Error parsing CSV file: {file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while loading data: {e}")
        return None


def visualize_data(df, args):
    
    #Visualize data based on the provided arguments using Plotly.
    
    if df is None:
        raise ValueError("DataFrame is None. Ensure the data is loaded correctly.")
    
    manipulator = DataManipulator(df)
    plotly_chart = None

    if args.column:
        grouped_df = manipulator.split_and_count(args.column, args.topN)
        plotly_chart = Visualizer.plot_topN(grouped_df, args.column, args.topN)
    elif args.interval:
        grouped_df = manipulator.group_by_time(args.interval)
        plotly_chart = Visualizer.plot_line_chart(grouped_df, args.interval)
    elif args.type:
        if not args.rating:
            grouped_df = manipulator.group_by_country(args.type)
            plotly_chart = Visualizer.plot_world_map(grouped_df, args.type)
        else:
            grouped_df = manipulator.group_by_country_and_rating_age(args.type, args.total_counts)
            plotly_chart = Visualizer.scatter_plot_of_age_group(grouped_df, args.type, args.total_counts)
    
    return plotly_chart


def save_and_open_html(plotly_chart, html_path):
    
    #Save the Plotly chart to an HTML file and open it in the default web browser.
    
    html_content = html.embedded_html_content(plotly_chart)
    
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    wb.open(html_path)


if __name__ == "__main__":
    df = load_data(DF_PATH, DATE_COLUMN)
    args = arg_parse.args

    try:
        plotly_chart = visualize_data(df, args)
        if plotly_chart:
            save_and_open_html(plotly_chart, HTML_PATH)
    except ValueError as e:
        print(f"Error: {e}")
