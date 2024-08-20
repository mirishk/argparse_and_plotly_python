from data_loader import load_data
from manipulator import DataManipulator
from viz import Visualizer
import arg_parse
import html 

DF_PATH = 'netflix_titles_after_eda.csv'
DATE_COLUMN = 'date_added'
HTML_PATH = 'plot_of_netflix.html'

if __name__ == "__main__":
    df = load_data(DF_PATH, DATE_COLUMN)
    args = arg_parse.args
    manipulator = DataManipulator(df)

    try:
        plotly_chart = Visualizer.visualize_data(df, args, manipulator)
        if plotly_chart:
            html.save_and_open_html(plotly_chart, HTML_PATH)
    except ValueError as e:
        print(f"Error: {e}")

