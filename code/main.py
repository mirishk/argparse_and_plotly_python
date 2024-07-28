import pandas as pd
from manipulator import DataManipulator
from viz import Visualizer
import arg_parse
import html 
import webbrowser as wb

df_path= 'netflix_titles_after_eda.csv'

def load_data(file_path, date_column):
    try:
        df = pd.read_csv(file_path)
        df[date_column] = pd.to_datetime(df[date_column])  # Convert type to datetime
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
#-------------------  
def visualize_data(df, args):
    if df is None:
        raise ValueError("DataFrame is None. Ensure the data is loaded correctly.")
    
    manipulator = DataManipulator(df) 
    plotly_chart = None

    funcs_dict= {
        manipulator.split_and_count: ("column","topN"),
        manipulator.group_by_time: "interval" ,
        manipulator.group_by_country:"type" ,
        manipulator.group_by_country_and_rating_age:("type", "rating", "total_counts")
    }

    for _func, args_tuple in funcs_dict.items():
        if isinstance(args_tuple, tuple):
            # Unpack the tuple if it contains multiple arguments
            args_values = tuple(getattr(args, arg) for arg in args_tuple)
   
    if args.column:
        agg_df = manipulator.split_and_count(args.column, args.topN)
        plotly_chart = Visualizer.plot_topN(agg_df, args.column, args.topN)

    if args.interval:
        grouped_df = manipulator.group_by_time(args.interval)
        plotly_chart = Visualizer.plot_line_chart(grouped_df, args.interval)

    if args.type:
        if not args.rating:
            grouped_df = manipulator.group_by_country(args.type)
            plotly_chart = Visualizer.plot_world_map(grouped_df, args.type)
        else:
            grouped_df = manipulator.group_by_country_and_rating_age(args.type, args.total_counts)
            plotly_chart = Visualizer.scatter_plot_of_age_group(grouped_df, args.type, args.total_counts)
    return plotly_chart
#------------------------------------------------
if __name__ == "__main__":
    df = load_data(df_path, 'date_added')
    args = arg_parse.args

    plotly_chart= visualize_data(df, args)

    if plotly_chart:

        html_content= html.embedded_html_content(plotly_chart)

        html_path = 'plot_of_netflix.html'
        with open(html_path, 'w', encoding='utf-8') as file: # Save the HTML content to a file with 'utf-8' encoding
            file.write(html_content)

        wb.open(html_path) # Open the HTML file in the default web browser
