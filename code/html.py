import webbrowser as wb

def embedded_html_content(chart):
    
    # Create HTML content with background image and Plotly chart

    html_content = f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Plotly Chart - Netflix</title>
        <style>
            body {{
                background-image: url('https://www.cityheadshots.com/uploads/5/1/2/1/5121840/how-to-audition-for-netflix_orig.jpg'); 
                background-size: cover;
                margin: 0; 
                padding: 15px; 
                font-family: Arial, sans-serif; 
            }}
            h1 {{
                text-align: center;
                color: red; 
            }}
            .plot-container {{
                margin: 0 auto;
                width: 100%;
                max-width: 950px; 
            }}
        </style>
    </head>
    <body>
        <h1>Plotly Chart - Netflix</h1>
        <div class="plot-container">
            {chart} 
        </div>
    </body>
    </html>
    '''
    return html_content


def save_and_open_html(plotly_chart, html_path):
    
    #Save the Plotly chart to an HTML file and open it in the default web browser.
    
    html_content = embedded_html_content(plotly_chart)
    
    with open(html_path, 'w', encoding='utf-8') as file:
        file.write(html_content)
    
    wb.open(html_path)
