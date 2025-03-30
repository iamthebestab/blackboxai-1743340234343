from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from calculation import calculate_pieces, select_best_sheet, calculate_costs

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)

# Available sheet sizes
SHEETS = [(15, 20), (14, 22), (18, 23), (12, 23), (11.5, 18), 
          (18, 25), (12.5, 18), (19, 26), (13, 19), (13.5, 15)]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        data = request.get_json()
        
        # Extract and validate inputs
        L_p = float(data['piece_length'])
        B_p = float(data['piece_breadth'])
        quantity = int(data['quantity'])
        gsm = int(data['gsm'])
        paper_price = float(data['paper_price'])
        pasting_option = data['pasting_option']
        no_of_plates = int(data['no_of_plates'])
        cost_of_printing = float(data['cost_of_printing'])
        cost_of_lamination = float(data['cost_of_lamination'])
        cost_of_cutting = float(data['cost_of_cutting'])
        cost_of_uv = float(data['cost_of_uv'])
        cost_of_dye = float(data['cost_of_dye'])
        cost_of_leaf = float(data['cost_of_leaf'])

        # Calculate best sheet and pieces
        best_sheet, max_pieces, min_waste = select_best_sheet(SHEETS, L_p, B_p)
        
        if not best_sheet:
            return jsonify({'error': 'No suitable sheet size found'}), 400

        # Calculate costs
        cost_details = calculate_costs(
            quantity, max_pieces, best_sheet, gsm, paper_price,
            pasting_option, no_of_plates, cost_of_printing,
            cost_of_lamination, cost_of_cutting, cost_of_uv,
            cost_of_dye, cost_of_leaf
        )

        # Prepare response
        response = {
            'best_sheet': best_sheet,
            'pieces': max_pieces,
            'waste': min_waste,
            **cost_details
        }

        return jsonify(response)

    except KeyError as e:
        return jsonify({'error': f'Missing required field: {str(e)}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid input: {str(e)}'}), 400
    except Exception as e:
        return jsonify({'error': f'An error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)