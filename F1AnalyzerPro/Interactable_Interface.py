from flask import Flask, request, render_template_string, jsonify
import pandas as pd  # Ensure pandas is imported
from Driver_Performance import *  # Import all functions

app = Flask(__name__)

# Load the drivers data
drivers = pd.read_csv('f1_data/drivers.csv')

# Fill the ALL_DRIVER_NAMES with surnames from the drivers data
ALL_DRIVER_NAMES = [row['surname'] for _, row in drivers.iterrows()]

# HTML template for the web page
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Run Script</title>
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

        /* Custom styling for the suggestions dropdown */
        #suggestions-container {
            position: relative;
            max-height: 200px;
            overflow-y: auto;
            border: 1px solid #ddd;
            border-top: none;
            background-color: white;
            z-index: 1000;
        }
        #suggestions-container div {
            padding: 8px;
            cursor: pointer;
        }
        #suggestions-container div:hover {
            background-color: #ddd;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function(){
            // Trigger the autocomplete process when the user starts typing
            $("#name").on("input", function() {
                var query = $(this).val().toLowerCase();  // Capture the user's input
                if(query.length >= 1) {  // Only make the request if the input is at least 1 character
                    $.ajax({
                        url: "/autocomplete",  // Server endpoint to fetch matching surnames
                        data: { query: query },
                        success: function(data) {
                            var dropdownContainer = $("#suggestions-container");
                            dropdownContainer.empty();  // Clear previous suggestions

                            // If there are suggestions, populate the dropdown
                            if (data.length > 0) {
                                data.forEach(function(name) {
                                    dropdownContainer.append("<div>" + name + "</div>");
                                });
                            }
                        }
                    });
                }
            });

            // Handle selection from the dropdown
            $(document).on("click", "#suggestions-container div", function() {
                $("#name").val($(this).text());  // Set input value to selected suggestion
                $("#suggestions-container").empty();  // Clear suggestions
            });
        });
    </script>
</head>
<body>
    <h1>Enter a Surname</h1>
    <form method="POST">
        <label for="name">Surname:</label>
        <input type="text" id="name" name="name" required>
        <button type="submit">Submit</button>
        <!-- Suggestions dropdown container -->
        <div id="suggestions-container"></div>
    </form>
    {% if output %}
        <h2>Points by Year for {{ name }}</h2>  <!-- Dynamic Title -->
        <div>{{ output|safe }}</div>
    {% endif %}
</body>
</html>

"""

@app.route('/autocomplete')
def autocomplete():
    query = request.args.get('query', '').lower()
    # Filter the surnames based on the query
    filtered_surnames = [surname for surname in ALL_DRIVER_NAMES if query in surname.lower()]
    print(f"Filtered surnames for query '{query}': {filtered_surnames}")  # Debugging
    return jsonify(filtered_surnames)

@app.route('/', methods=['GET', 'POST'])
def run_function():
    output = None
    name = None  # Initialize name variable to be passed to the template
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        name = name.capitalize()  # Capitalize the surname
        if not name:
            return render_template_string(HTML_TEMPLATE, output="Error: Surname is required.", name=name)
        try:
            # Call the imported function and pass the surname as an argument
            function_output = viewFinalDriverPointsByYear(name)

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