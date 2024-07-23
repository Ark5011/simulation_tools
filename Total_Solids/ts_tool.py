from flask import Flask, request, jsonify, render_template, session, make_response
from io import BytesIO
import os
from openpyxl import Workbook

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('ts_fe.html', input_data={})

def format_value(value, fmt):
    return fmt.format(value) if isinstance(value, (float, int)) else value

@app.route('/totalsolids', methods=['POST'])
def totalsolids():
    try:
        data = request.json
        fat_content = int(data['fat_content'])
        start_density = int(data['density'])

        results = []

        for i in range(61):
            current_density = start_density + i
            total_solids = (138.2 - (136.206 / current_density * 1000)) / (0.505 - (0.00651101 * fat_content))
            results.append(total_solids)

        session['calculated_data_ts'] = {
            'fat_content': int(data['fat_content']),
            'density': int(data['density']),
            'total_solids': results,
        }

        return jsonify({
            'total_solids': results,
            'error': None
        })

    except (ValueError, KeyError) as e:
        return jsonify({'error': f"An error occurred: {e}"})

@app.route('/generate_excel', methods=['GET'])
def generate_excel():
    try:
        data_from_ts_tool = session.get('calculated_data_ts')

        if not data_from_ts_tool:
            return jsonify({'error': 'No data found to generate Excel'}), 400

        # Prepare Excel data
        excel_data = [
            ['Density, kg/m3', 'Total Solids %']
        ]

        for i, ts_value in enumerate(data_from_ts_tool['total_solids']):
            density = data_from_ts_tool['density'] + i
            excel_data.append([density, ts_value])

        # Create Excel workbook
        wb = Workbook()
        ws = wb.active
        ws.title = "Total Solids Tool"

        # Write data to Excel sheet
        for row in excel_data:
            ws.append(row)

        # Save workbook to a bytes buffer
        output = BytesIO()
        wb.save(output)
        output.seek(0)

        # Create a response to return the Excel file
        response = make_response(output.getvalue())
        response.headers["Content-Disposition"] = "attachment; filename=ts.xlsx"
        response.headers["Content-type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        return response

    except Exception as e:
        return jsonify({'error': f"An error occurred: {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5005)
