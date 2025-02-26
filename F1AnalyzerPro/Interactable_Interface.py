from flask import Flask, request, render_template_string, jsonify
import pandas as pd
from Driver_Performance import *  # Import necessary functions
from Constructor_Performance import *

app = Flask(__name__)

# Load the drivers data
drivers = pd.read_csv('f1_data/drivers.csv')

# Combine first names and surnames for autocomplete functionality
ALL_DRIVER_NAMES = [
    {"full_name": f"{row['forename']} {row['surname']}", "surname": row["surname"]}
    for _, row in drivers.iterrows()
]
constructors = pd.read_csv('f1_data/constructors.csv')

# Combine first names and surnames for autocomplete functionality
ALL_CONSTRUCTOR_NAMES = [
    {"constructor_name": row['name']}
    for _, row in constructors.iterrows()
]

# HTML Templates
START_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>F1 Performance</title>
</head>
<body>
    <h1>Welcome to F1 Analyst Pro</h1>
    <p>Please choose a page to visit:</p>
    <button onclick="window.location.href='/driver-points-by-year'">Driver Points by Year</button>
    <button onclick="window.location.href='/constructor-points-by-year'">Constructor Points by Year</button>
</body>
</html>
"""

DRIVER_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driver Points</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        tr:nth-child(odd) { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #ffffff; }
        tr:hover { background-color: #ddd; }
        #suggestions-container {
            position: absolute; max-height: 200px; overflow-y: auto; border: 1px solid #ddd;
            border-top: none; background-color: white; z-index: 1000;
        }
        #suggestions-container div {
            padding: 8px; cursor: pointer;
        }
        #suggestions-container div:hover {
            background-color: #ddd;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $("#name").on("input", function() {
                let query = $(this).val().toLowerCase();
                if (query.length >= 1) {
                    $.ajax({
                        url: "/autocomplete_drivers",
                        data: { query: query },
                        success: function(data) {
                            let container = $("#suggestions-container");
                            container.empty();
                            if (data.length > 0) {
                                data.forEach(name => {
                                    container.append(`<div>${name}</div>`);
                                });
                            }
                        }
                    });
                }
            });

            $(document).on("click", "#suggestions-container div", function() {
                $("#name").val($(this).text());
                $("#suggestions-container").empty();
            });
        });
    </script>
</head>
<body>
    <h1>Driver Performance</h1>
    <button onclick="window.location.href='/'">Home</button>
    <button onclick="window.location.href='/compare-driver-year-points'">Compare Performance</button>
    <button onclick="window.location.href='/driver-points-per-race'">Driver Points Per Race</button>
    <form method="POST">
        <label for="name">Driver:</label>
        <input type="text" id="name" name="name" required autocomplete="off">
        <button type="submit">Submit</button>
        <div id="suggestions-container"></div>
    </form>
    {% if output %}
        <h2>Points by Year for {{ name }}</h2>
        <div>{{ output|safe }}</div>
    {% endif %}
</body>
</html>
"""

DRIVER_COMPARE_YEAR_POINTS_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compare Driver Points</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        tr:nth-child(odd) { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #ffffff; }
        tr:hover { background-color: #ddd; }
        .suggestions-container {
            position: absolute; max-height: 200px; overflow-y: auto; border: 1px solid #ddd;
            border-top: none; background-color: white; z-index: 1000;
        }
        .suggestions-container div {
            padding: 8px; cursor: pointer;
        }
        .suggestions-container div:hover {
            background-color: #ddd;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            function setupAutocomplete(inputFieldId, suggestionsContainerClass) {
                $(`#${inputFieldId}`).on("input", function() {
                    let inputField = $(this);
                    let query = inputField.val().toLowerCase();
                    let suggestionsContainer = $(`.${suggestionsContainerClass}`);
                    if (query.length >= 1) {
                        $.ajax({
                            url: "/autocomplete_drivers",
                            data: { query: query },
                            success: function(data) {
                                suggestionsContainer.empty();
                                if (data.length > 0) {
                                    data.forEach(name => {
                                        suggestionsContainer.append(`<div>${name}</div>`);
                                    });
                                }
                            }
                        });
                    } else {
                        suggestionsContainer.empty();
                    }
                });

                $(document).on("click", `.${suggestionsContainerClass} div`, function() {
                    let selectedName = $(this).text();
                    $(`#${inputFieldId}`).val(selectedName);
                    $(`.${suggestionsContainerClass}`).empty();
                });
            }

            setupAutocomplete("name1", "suggestions-container-name1");
            setupAutocomplete("name2", "suggestions-container-name2");
        });
    </script>
</head>
<body>
    <h1>Compare Driver Performance</h1>
    <button onclick="window.location.href='/'">Home</button>
    <button onclick="window.location.href='/compare-driver-year-points'">Compare Performance</button>
    <button onclick="window.location.href='/driver-points-per-race'">Driver Points Per Race</button>
    <form method="POST">
        <label for="name1">Driver 1:</label>
        <input type="text" id="name1" name="name1" required autocomplete="off">
        <div class="suggestions-container suggestions-container-name1"></div>

        <label for="name2">Driver 2:</label>
        <input type="text" id="name2" name="name2" required autocomplete="off">
        <div class="suggestions-container suggestions-container-name2"></div>

        <button type="submit">Compare</button>
    </form>

    {% if output1 %}
        <h2>Points by Year for {{ name1 }}</h2>
        <div>{{ output1|safe }}</div>
    {% endif %}

    {% if output2 %}
        <h2>Points by Year for {{ name2 }}</h2>
        <div>{{ output2|safe }}</div>
    {% endif %}

    {% if comparison_output %}
        <h2>Comparison</h2>
        <div>{{ comparison_output|safe }}</div>
    {% endif %}
</body>
</html>
"""

DRIVER_BY_RACE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driver Points</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        tr:nth-child(odd) { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #ffffff; }
        tr:hover { background-color: #ddd; }
        #suggestions-container {
            position: absolute; max-height: 200px; overflow-y: auto; border: 1px solid #ddd;
            border-top: none; background-color: white; z-index: 1000;
        }
        #suggestions-container div {
            padding: 8px; cursor: pointer;
        }
        #suggestions-container div:hover {
            background-color: #ddd;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $("#name").on("input", function() {
                let query = $(this).val().toLowerCase();
                if (query.length >= 1) {
                    $.ajax({
                        url: "/autocomplete_drivers",
                        data: { query: query },
                        success: function(data) {
                            let container = $("#suggestions-container");
                            container.empty();
                            if (data.length > 0) {
                                data.forEach(name => {
                                    container.append(`<div>${name}</div>`);
                                });
                            }
                        }
                    });
                }
            });

            $(document).on("click", "#suggestions-container div", function() {
                $("#name").val($(this).text());
                $("#suggestions-container").empty();
            });
        });
    </script>
</head>
<body>
    <h1>Driver Performance By Race</h1>
    <button onclick="window.location.href='/'">Home</button>
    <button onclick="window.location.href='/driver-points-by-year'">Back</button>
    <form method="POST">
        <label for="name">Driver:</label>
        <input type="text" id="name" name="name" required autocomplete="off">
        <button type="submit">Submit</button>
        <div id="suggestions-container"></div>
    </form>
    {% if output %}
        <h2>Points by Race for {{ name }}</h2>
        <div>{{ output|safe }}</div>
    {% endif %}
</body>
</html>
"""

CONSTRUCTOR_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Constructor Points</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        tr:nth-child(odd) { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #ffffff; }
        tr:hover { background-color: #ddd; }
        #suggestions-container {
            position: absolute; max-height: 200px; overflow-y: auto; border: 1px solid #ddd;
            border-top: none; background-color: white; z-index: 1000;
        }
        #suggestions-container div {
            padding: 8px; cursor: pointer;
        }
        #suggestions-container div:hover {
            background-color: #ddd;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $("#name").on("input", function() {
                let query = $(this).val().toLowerCase();
                if (query.length >= 1) {
                    $.ajax({
                        url: "/autocomplete_constructors",
                        data: { query: query },
                        success: function(data) {
                            let container = $("#suggestions-container");
                            container.empty();
                            if (data.length > 0) {
                                data.forEach(name => {
                                    container.append(`<div>${name}</div>`);
                                });
                            }
                        }
                    });
                }
            });

            $(document).on("click", "#suggestions-container div", function() {
                $("#name").val($(this).text());
                $("#suggestions-container").empty();
            });
        });
    </script>
</head>
<body>
    <h1>Constructor Performance</h1>
    <button onclick="window.location.href='/'">Home</button>
    <button onclick="window.location.href='/constructor-points-per-race'">Constructor Points Per Race</button>
    <form method="POST">
        <label for="name">Constructor:</label>
        <input type="text" id="name" name="name" required autocomplete="off">
        <button type="submit">Submit</button>
        <div id="suggestions-container"></div>
    </form>
    {% if output %}
        <h2>Points by Year for {{ name }}</h2>
        <div>{{ output|safe }}</div>
    {% endif %}
</body>
</html>
"""

CONSTRUCTOR_BY_RACE_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Driver Points</title>
    <style>
        table { width: 100%; border-collapse: collapse; }
        th, td { padding: 8px; text-align: left; border: 1px solid #ddd; }
        tr:nth-child(odd) { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #ffffff; }
        tr:hover { background-color: #ddd; }
        #suggestions-container {
            position: absolute; max-height: 200px; overflow-y: auto; border: 1px solid #ddd;
            border-top: none; background-color: white; z-index: 1000;
        }
        #suggestions-container div {
            padding: 8px; cursor: pointer;
        }
        #suggestions-container div:hover {
            background-color: #ddd;
        }
    </style>
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
    <script>
        $(document).ready(function() {
            $("#name").on("input", function() {
                let query = $(this).val().toLowerCase();
                if (query.length >= 1) {
                    $.ajax({
                        url: "/autocomplete_constructors",
                        data: { query: query },
                        success: function(data) {
                            let container = $("#suggestions-container");
                            container.empty();
                            if (data.length > 0) {
                                data.forEach(name => {
                                    container.append(`<div>${name}</div>`);
                                });
                            }
                        }
                    });
                }
            });

            $(document).on("click", "#suggestions-container div", function() {
                $("#name").val($(this).text());
                $("#suggestions-container").empty();
            });
        });
    </script>
</head>
<body>
    <h1>Constructor Performance By Race</h1>
    <button onclick="window.location.href='/'">Home</button>
    <button onclick="window.location.href='/constructor-points-by-year'">Back</button>
    <form method="POST">
        <label for="name">Constructor:</label>
        <input type="text" id="name" name="name" required autocomplete="off">
        <button type="submit">Submit</button>
        <div id="suggestions-container"></div>
    </form>
    {% if output %}
        <h2>Points by Race for {{ name }}</h2>
        <div>{{ output|safe }}</div>
    {% endif %}
</body>
</html>
"""

@app.route('/autocomplete_drivers')
def autocomplete_drivers():
    query = request.args.get('query', '').lower()
    # Filter drivers where the surname contains the query
    filtered_names = [
        driver["full_name"]
        for driver in ALL_DRIVER_NAMES
        if query in driver["surname"].lower()
    ]
    return jsonify(filtered_names)

@app.route('/autocomplete_constructors')
def autocomplete_constructors():
    query = request.args.get('query', '').lower()
    # Filter drivers where the surname contains the query
    filtered_names = [
        constructor["constructor_name"]
        for constructor in ALL_CONSTRUCTOR_NAMES
        if query in constructor["constructor_name"].lower()
    ]
    return jsonify(filtered_names)

@app.route('/')
def starting_page():
    """Landing page for selecting the analysis type."""
    return render_template_string(START_TEMPLATE)

@app.route('/driver-points-by-year', methods=['GET', 'POST'])
def run_function_driver_eoy_points():
    output = None
    name = None  # Initialize name variable to be passed to the template
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            return render_template_string(DRIVER_TEMPLATE, output="Error: Driver name is required.", name=name)

        # Validate that the name exists in the dataset
        matched_driver = next((driver for driver in ALL_DRIVER_NAMES if driver["full_name"] == name), None)
        if not matched_driver:
            return render_template_string(DRIVER_TEMPLATE, output="Error: Driver not found.", name=name)

        try:
            # Call the imported function with the last name
            function_output = viewFinalDriverPointsByYear(name)

            if isinstance(function_output, pd.DataFrame):
                output = function_output.to_html(classes='table table-striped', index=False)
            elif isinstance(function_output, (list, dict)):
                import json
                output = json.dumps(function_output, indent=4)
            else:
                output = str(function_output)
        except Exception as e:
            output = f"An error occurred: {str(e)}"
    return render_template_string(DRIVER_TEMPLATE, output=output, name=name)

@app.route('/compare-driver-year-points', methods=['GET', 'POST'])
def run_function_compare_driver_eoy_points():
    output1 = None
    output2 = None
    comparison_output = None
    name1 = None
    name2 = None

    if request.method == 'POST':
        name1 = request.form.get('name1', '').strip()
        name2 = request.form.get('name2', '').strip()

        if not name1:
            return render_template_string(DRIVER_COMPARE_YEAR_POINTS_TEMPLATE,
                                          output1="Error: Driver 1 name is required.",
                                          output2=None, comparison_output=None,
                                          name1=name1, name2=name2)

        if not name2:
            return render_template_string(DRIVER_COMPARE_YEAR_POINTS_TEMPLATE,
                                          output1=None,
                                          output2="Error: Driver 2 name is required.",
                                          comparison_output=None,
                                          name1=name1, name2=name2)

        # Validate that the names exist in the dataset
        matched_driver1 = next((driver for driver in ALL_DRIVER_NAMES if driver["full_name"] == name1), None)
        matched_driver2 = next((driver for driver in ALL_DRIVER_NAMES if driver["full_name"] == name2), None)

        if not matched_driver1:
            return render_template_string(DRIVER_COMPARE_YEAR_POINTS_TEMPLATE,
                                          output1="Error: Driver 1 not found.",
                                          output2=None, comparison_output=None,
                                          name1=name1, name2=name2)

        if not matched_driver2:
            return render_template_string(DRIVER_COMPARE_YEAR_POINTS_TEMPLATE,
                                          output1=None,
                                          output2="Error: Driver 2 not found.",
                                          comparison_output=None,
                                          name1=name1, name2=name2)

        try:
            # Fetch data for Driver 1
            function_output1 = viewFinalDriverPointsByYear(name1)

            # Convert to DataFrame if needed and set the HTML output
            if isinstance(function_output1, pd.DataFrame):
                output1 = function_output1.to_html(classes='table table-striped', index=False)
            else:
                output1 = str(function_output1)

        except Exception as e:
            output1 = f"An error occurred while fetching data for {name1}: {str(e)}"

        try:
            # Fetch data for Driver 2
            function_output2 = viewFinalDriverPointsByYear(name2)

            # Convert to DataFrame if needed and set the HTML output
            if isinstance(function_output2, pd.DataFrame):
                output2 = function_output2.to_html(classes='table table-striped', index=False)
            else:
                output2 = str(function_output2)

        except Exception as e:
            output2 = f"An error occurred while fetching data for {name2}: {str(e)}"

        # Compare the two DataFrames if both are valid
        if isinstance(function_output1, pd.DataFrame) and isinstance(function_output2, pd.DataFrame):
            try:
                # Merge the data on the "year" column
                comparison_df = pd.merge(
                    function_output1,
                    function_output2,
                    on='year',
                    how='outer',
                    suffixes=(f' ({name1})', f' ({name2})')
                ).fillna(0)  # Fill missing values with 0 for comparison

                # Add a column for point difference
                comparison_df['Point Difference'] = (
                    comparison_df[f'points ({name1})'] - comparison_df[f'points ({name2})']
                )

                # Calculate totals
                total_row = {
                    'year': 'Total',
                    f'points ({name1})': comparison_df[f'points ({name1})'].sum(),
                    f'points ({name2})': comparison_df[f'points ({name2})'].sum(),
                    'Point Difference': comparison_df['Point Difference'].sum()
                }

                # Append the total row
                comparison_df = pd.concat(
                    [comparison_df, pd.DataFrame([total_row])],
                    ignore_index=True
                )

                # Convert the comparison DataFrame to HTML
                comparison_output = comparison_df.to_html(classes='table table-striped', index=False)

            except Exception as e:
                comparison_output = f"An error occurred during comparison: {str(e)}"

    return render_template_string(
        DRIVER_COMPARE_YEAR_POINTS_TEMPLATE,
        output1=output1,
        output2=output2,
        comparison_output=comparison_output,
        name1=name1,
        name2=name2
    )

@app.route('/driver-points-per-race', methods=['GET', 'POST'])
def run_function_driver_points_per_race():
    output = None
    name = None  # Initialize name variable to be passed to the template
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            return render_template_string(DRIVER_BY_RACE_TEMPLATE, output="Error: Driver name is required.", name=name)

        # Validate that the name exists in the dataset
        matched_driver = next((driver for driver in ALL_DRIVER_NAMES if driver["full_name"] == name), None)
        if not matched_driver:
            return render_template_string(DRIVER_BY_RACE_TEMPLATE, output="Error: Driver not found.", name=name)

        try:
            # Call the imported function with the last name
            function_output =  driverTotalPointsPerRace(name)

            if isinstance(function_output, pd.DataFrame):
                output = function_output.to_html(classes='table table-striped', index=False)
            elif isinstance(function_output, (list, dict)):
                import json
                output = json.dumps(function_output, indent=4)
            else:
                output = str(function_output)
        except Exception as e:
            output = f"An error occurred: {str(e)}"
    return render_template_string(DRIVER_BY_RACE_TEMPLATE, output=output, name=name)

@app.route('/constructor-points-by-year', methods=['GET', 'POST'])
def run_function_constructor_eoy_points():
    output = None
    name = None  # Initialize name variable to be passed to the template
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            return render_template_string(CONSTRUCTOR_TEMPLATE, output="Error: Constructor name is required.", name=name)

        # Validate that the name exists in the dataset
        matched_constructor = next((constructor for constructor in ALL_CONSTRUCTOR_NAMES if constructor["constructor_name"] == name), None)
        if not matched_constructor:
            return render_template_string(CONSTRUCTOR_TEMPLATE, output="Error: Constructor not found.", name=name)

        try:
            # Call the imported function with the last name
            function_output = constructorFinalPointsByYear(name)

            if isinstance(function_output, pd.DataFrame):
                output = function_output.to_html(classes='table table-striped', index=False)
            elif isinstance(function_output, (list, dict)):
                import json
                output = json.dumps(function_output, indent=4)
            else:
                output = str(function_output)
        except Exception as e:
            output = f"An error occurred: {str(e)}"
    return render_template_string(CONSTRUCTOR_TEMPLATE, output=output, name=name)

@app.route('/constructor-points-per-race', methods=['GET', 'POST'])
def run_function_constructor_points_per_race():
    output = None
    name = None  # Initialize name variable to be passed to the template
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        if not name:
            return render_template_string(CONSTRUCTOR_BY_RACE_TEMPLATE, output="Error: Constructor name is required.", name=name)

        # Validate that the name exists in the dataset
        matched_constructor = next((constructor for constructor in ALL_CONSTRUCTOR_NAMES if constructor["constructor_name"] == name), None)
        if not matched_constructor:
            return render_template_string(CONSTRUCTOR_BY_RACE_TEMPLATE, output="Error: Constructor not found.", name=name)

        try:
            # Call the imported function with the last name
            function_output =  constructorTotalPointsPerRace(name)

            if isinstance(function_output, pd.DataFrame):
                output = function_output.to_html(classes='table table-striped', index=False)
            elif isinstance(function_output, (list, dict)):
                import json
                output = json.dumps(function_output, indent=4)
            else:
                output = str(function_output)
        except Exception as e:
            output = f"An error occurred: {str(e)}"
    return render_template_string(CONSTRUCTOR_BY_RACE_TEMPLATE, output=output, name=name)


if __name__ == '__main__':
    app.run(debug=True)
