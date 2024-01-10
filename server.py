from flask import Flask, request, jsonify, render_template
from flasgger import Swagger
from service import write_csv, read_csv, read_csv_as_dataframe
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
import json
import plotly

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/api/health",methods=["GET"])
def home():
    """
    See if the application is active.
    ---
    responses:
      200:
        description: A string stating that the application is up
    """
    return "The application is up"

@app.route('/api/data', methods=['GET'])
def get_all_data():
    """
    Get all data from the CSV file
    ---
    responses:
      200:
        description: A list of data records
    """
    data = read_csv()
    return jsonify(data)


@app.route('/api/data/<int:record_id>', methods=['GET'])
def get_record(record_id):
    """
    Get a specific record from the CSV file by ID
    ---
    parameters:
      - name: record_id
        in: path
        type: integer
        required: true
        description: ID of the record to retrieve
    responses:
      200:
        description: A single data record
      404:
        description: Record not found
    """
    data = read_csv()
    record = next((row for row in data if row['id'] == record_id), None)
    if record:
        return jsonify(record)
    else:
        return jsonify({'error': 'Record not found'}), 404

@app.route('/api/data', methods=['POST'])
def add_record():
    """
    Add a new record to the CSV file
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          id: NewRecord
          properties:
            name:
              type: string
              description: Student's name
            marks:
              type: number
              format: float
              minimum: 0
              maximum: 100
              description: Marks obtained by the student (float between 0 and 100)
            grade:
              type: string
              description: Letter grade obtained by the student
            course:
              type: string
              description: Name of the course
    responses:
      201:
        description: The newly created data record
    """
    new_record = request.get_json()
    data = read_csv()
    
    if not data:
        new_record['id'] = 1
    else:
        new_record['id'] = max(row['id'] for row in data) + 1
    
    data.append(new_record)
    write_csv(data)
    return jsonify(new_record), 201


@app.route('/api/data/<int:record_id>', methods=['PUT'])
def update_record(record_id):
    """
    Update a record in the CSV file by ID
    ---
    parameters:
      - name: record_id
        in: path
        type: integer
        required: true
        description: ID of the record to update
      - name: body
        in: body
        required: true
        schema:
          id: UpdatedRecord
          properties:
            name:
              type: string
              description: Updated student's name
            marks:
              type: number
              format: float
              minimum: 0
              maximum: 100
              description: Updated marks obtained by the student (float between 0 and 100)
            grade:
              type: string
              description: Updated letter grade obtained by the student
            course:
              type: string
              description: Updated name of the course
    responses:
      200:
        description: The updated data record
      404:
        description: Record not found
    """
    updated_record = request.get_json()
    data = read_csv()

    record_index = next((index for index, row in enumerate(data) if row['id'] == record_id), None)
    
    if record_index is not None:
        data[record_index] = updated_record
        write_csv(data)
        return jsonify(updated_record)
    else:
        return jsonify({'error': 'Record not found'}), 404


@app.route('/api/data/<int:record_id>', methods=['DELETE'])
def delete_record(record_id):
    """
    Delete a record from the CSV file by ID
    ---
    parameters:
      - name: record_id
        in: path
        type: integer
        required: true
        description: ID of the record to delete
    responses:
      200:
        description: Record deleted successfully
      404:
        description: Record not found
    """
    data = read_csv()
    updated_data = [row for row in data if row['id'] != record_id]
    
    if len(updated_data) < len(data):
        write_csv(updated_data)
        return jsonify({'message': 'Record deleted successfully'})
    else:
        return jsonify({'error': 'Record not found'}), 404

# Route to render the view for existing records
@app.route('/view_records_plotly', methods=['GET'])
def render_view_records_plotly():
    df = read_csv_as_dataframe()
    # Create a Plotly table
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(df.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df.course, df.grade, df.marks, df.name, df.id],
               fill_color='lavender',
               align='left'))
    ])

    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('view_records_plotly.html', graphJSON=graphJSON)

# Route to render the view for existing records
@app.route('/render_stats_plotly', methods=['GET'])
def render_stats_plotly():
    df = read_csv_as_dataframe()
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        specs=[[{"type": "bar"}],
            [{"type": "pie"}]],
        subplot_titles=("Compare average marks across courses", "Grade Distribution")
    )

    # Bar chart for average marks by course
    avg_marks_by_course = df.groupby('course')['marks'].mean().reset_index()
    bar_fig = px.bar(avg_marks_by_course, x='course', y='marks', title='Average Marks by Course', labels={'Marks': 'Average Marks'})

    fig.add_trace(
        bar_fig['data'][0],
        row=1, col=1
    )

    # Pie chart for grade distribution
    grade_distribution = df['grade'].value_counts().reset_index()
    grade_distribution.columns = ['grade', 'count']
    pie_fig = px.pie(grade_distribution, names='grade', values='count', title='Grade Distribution')

    fig.add_trace(
        pie_fig['data'][0],
        row=2, col=1
    )

    fig.update_layout(height=800, width=700, showlegend=False)

    # Create graphJSON
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return render_template('view_stats_plotly.html', graphJSON=graphJSON)

# Route to render the "View Records" page
@app.route('/view_records')
def render_view_records():
    data = read_csv()
    return render_template('view_records.html', records=data)

# Route to render the form for adding a new record
@app.route('/add_record', methods=['GET'])
def render_add_records_form():
    return render_template('add_records.html')
