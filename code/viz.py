import plotly.express as px
import plotly.io as pio  #for html file

# Get the Plotly chart as HTML content
def _chart_in_html(fig):
        chart = pio.to_html(fig, full_html=False)
        return chart

class Visualizer:
    # 1 ===============================================================
    # Function that plot bar chart of top N values in specific column
    @staticmethod
    def plot_topN(agg_df,column, topN):
        
        fig = px.bar(agg_df, x = column, y = 'Count',  
                    color = column, color_discrete_sequence = ['red'],
                    text = agg_df['Count']
        )
        
        if column=='cast':
            title_val = 'Actor'
        else:
            title_val = f'{column.title()}'
        
        fig.update_layout(xaxis_title = title_val, yaxis_title = 'Count', 
                        plot_bgcolor = 'black', paper_bgcolor = 'black',
                        font = dict(color='white'),
                        bargap = 0.5,  # Adjust space between bars
                        height = 500, width=1000,
                        title=dict(text=f'Top {topN} {title_val}s', x=0.5)  # Set the title and center it horizontally
        )

        return _chart_in_html(fig)

    # 2 =======================================================================
    # Create a line chart
    @staticmethod
    def plot_line_chart(grouped_df, interval):
        
        # for average line
        average_count = grouped_df.groupby('type')['count'].mean().reset_index(name='average_count')

        fig = px.line(grouped_df, x = interval, y = 'count', color = 'type',
                title = f'Count of Movies and TV Shows Added Each {interval.capitalize()}',
                labels = {'year': 'Year', 'month':'Month', 'count': 'Count', 'type': 'Type'},
                markers=True,
                color_discrete_sequence = ['#FF0000', '#ff8080']
        )

        # Add average lines for movies and TV shows
        for _, row in average_count.iterrows():
            fig.add_shape(type = 'line',
                        x0 = grouped_df[interval].min(),
                        y0 = row['average_count'],
                        x1 = grouped_df[interval].max(),
                        y1 = row['average_count'],
                        line = dict(color='yellow', dash='dash')
                        )
            # Add annotation for the average count value
            fig.add_annotation(x = grouped_df[interval].max() + 0.5, y = row['average_count'],
                            text = f'AVG: {row["average_count"]:.2f}',
                            showarrow = False,
                            font = dict(color='yellow', size=10)
                            )

        
        # Customizing appearance
        fig.update_traces(line=dict(width=2.5), marker=dict(size=10))
        
        fig.update_layout(
            plot_bgcolor = 'black', paper_bgcolor = 'black',  
            font = dict(color='white'),  
            title = dict(font=dict(color='white'), x=0.3),
            height = 500, width=1000,
            xaxis=dict(showgrid=False),  
            yaxis=dict(gridcolor='lightgrey', gridwidth=0.05)
        )
        
        return _chart_in_html(fig)

    # 3 ==========================================================================
    # Load the world map colored according count of rows in each country
    @staticmethod
    def plot_world_map(grouped_df, type_of_netflix):
        
        custom_color_scale = ['#ffb3b3','#ff9999', '#ff8080','#ff6666', '#ff4d4d','#ff3333', '#ff0000', '#cc0000', '#990000']

        fig = px.choropleth(
            grouped_df,
            locations ='country', 
            color ='Count',       
            locationmode = 'country names',
            color_continuous_scale = custom_color_scale,
            range_color = (grouped_df['Count'].min(), grouped_df['Count'].max()),
            hover_data = ["country", "Count"],
            title = f'{type_of_netflix} Count by Country'
        )

        fig.update_geos(
            bgcolor='black',  
            projection_type='natural earth' ,
            visible=True,
            showcountries=True,
            countrywidth=1,  
            countrycolor='grey'  # Set the color of country borders
        )

        fig.update_layout(
            plot_bgcolor = 'black', paper_bgcolor = 'black',  
            font = dict(color='white'),  
            title = dict(font=dict(color='white'), x=0.5),
            height = 500, width=1000
        )

        return _chart_in_html(fig)

    # 4 ===============================================================
    # Scatter plot of age group by country
    @staticmethod
    def scatter_plot_of_age_group(grouped_df, type_of_netflix, total_count):
        
        scatter_fig = px.scatter(grouped_df, x='country', y='age_group',  color='age_group', size='percentage',
                                title = f"Percentage of Age Group by Country for {type_of_netflix} (Total Count: {total_count} and above)", 
                                category_orders = {'age_group': ['Kids', 'Older Kids', 'Teens', 'Young Adults', 'Adults']},
                                size_max = 35,
                                color_discrete_map = {
                                    'Kids': '#ffb3b3',         
                                    'Older Kids': '#ff8080', 
                                    'Teens': '#ff6666',     
                                    'Young Adults': '#ff4d4d', 
                                    'Adults': '#ff0000'       
                                },
                                hover_data = {'age_group': False, 'count': True, 'percentage': ':.2f%'} 
                                )  

        # Update layout to change background color and other elements
        scatter_fig.update_layout(
            plot_bgcolor = 'black',  paper_bgcolor = 'black',  
            font = dict(color='white'),  
            title = dict(font=dict(color='white'), x=0.5),
            xaxis_title = 'Country', yaxis_title = 'Age Group',
            xaxis = dict(linecolor='white', showgrid=False),  
            yaxis = dict(linecolor='white', showgrid=False),  
            legend = dict(bgcolor='black', bordercolor='white', borderwidth=1, font=dict(color='white')),  
            height = 500, width=1000
        )

        return _chart_in_html(scatter_fig)

    # =======================================================================
