from flask import Flask, request, render_template_string
from Driver_Performance import *  # Import all functions
import pandas as pd  # Ensure pandas is imported

app = Flask(__name__)

# HTML template for the web page
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<style>
        /* Zebra stripe styling for the table */
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 8px;
            text-align: left;
            border: 1px solid #ddd;
        }
        tr:nth-child(odd) {
            background-color: #f2f2f2;  /* Light gray for odd rows */
        }
        tr:nth-child(even) {
            background-color: #ffffff;  /* White for even rows */
        }
        /* Add a hover effect on rows */
        tr:hover {
            background-color: #ddd;
        }
    </style>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Script</title>
</head>
<body>
    <h1>Enter a Name</h1>
    <form method="POST">
        <label for="name">Name:</label>
        <input type="text" id="name" name="name" required>
        <button type="submit">Submit</button>
    </form>
    {% if output %}
        <h2>Points by Year for {{ name }}</h2>  <!-- Dynamic Title -->
        <div>{{ output|safe }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def run_function():
    output = None
    name = None  # Initialize name variable to be passed to the template
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        name = name.capitalize()
        if not name:
            return render_template_string(HTML_TEMPLATE, output="Error: Name is required.", name=name)
        try:
            # Call the imported function and pass the name as an argument
            function_output = viewLifetimeDriverPointsByYear(name)

            if isinstance(function_output, pd.DataFrame):
                # Convert the DataFrame to an HTML table
                output = function_output.to_html(classes='table table-striped', index=False)
            elif isinstance(function_output, (list, dict)):
                # Format the output for display if it is complex data
                import json
                output = json.dumps(function_output, indent=4)
            else:
                output = str(function_output)
        except Exception as e:
            output = f"An error occurred: {str(e)}"
    return render_template_string(HTML_TEMPLATE, output=output, name=name)


if __name__ == '__main__':
    app.run(debug=True)
