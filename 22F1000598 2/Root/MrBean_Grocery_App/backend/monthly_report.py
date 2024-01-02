import pandas as pd
import plotly.express as px
import plotly.io as pio
# pio.orca.config.use_xvfb = True
from jinja2 import Template
from database import get_monthly_purchased_items
import os

# Function to fetch purchased items for a specific user in a given month
def generate_monthly_report(user_id):
    # Fetch purchased items for the user in the given month
    purchased_items = get_monthly_purchased_items(user_id)
    print(purchased_items)
    # Process the fetched data for the table
    table_data = [{
        'name': item.Product.name,
        'quantity': item.Profile.quantity,
        'purchase_date': item.Profile.date_purchased
    } for item in purchased_items]
    print(table_data)
    for item in purchased_items:
        print(item.Product.name)
    # Create a Pandas DataFrame for Plotly chart
    df = pd.DataFrame({
        'Product Name': [item.Product.name for item in purchased_items],
        'Quantity': [item.Profile.quantity for item in purchased_items]
    })

    # Create a bar chart using Plotly Express
    fig = px.bar(df, x='Product Name', y='Quantity', title='Products Purchased')

    # Update layout for better appearance (optional)
    fig.update_layout(
        xaxis_title='Product Name',
        yaxis_title='Quantity',
        xaxis_tickangle=-45,  # Rotate x-axis labels for better readability
        bargap=0.2  # Set gap between bars
    )

    # Save the chart as an image
    image_path = f'chart.png'
    # fig.to_image(image_path)
    fig.write_image(image_path)

    # Read the HTML template
    with open('monthly_report_template.html', 'r') as file:
        template = Template(file.read())

    # Render HTML with table data and image path
    rendered_html = template.render(products=table_data, image_path=image_path)

    # Save the rendered HTML to a file
    report_file = f'report.html'
    if os.path.exists(report_file):
        os.remove(report_file)

    with open(report_file, 'w') as output:
        output.write(rendered_html)

    return report_file


