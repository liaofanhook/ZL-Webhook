import os
import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev-secret-key")
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

# In-memory storage for quotations
quotations_storage = []

def validate_quotation_data(data):
    """Validate quotation data structure and required fields."""
    if not isinstance(data, dict):
        return False, "Invalid data format: expected JSON object"
    
    required_fields = ['id', 'customer_name', 'items', 'total_amount']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate data types
    if not isinstance(data['id'], (str, int)):
        return False, "Field 'id' must be a string or integer"
    
    if not isinstance(data['customer_name'], str):
        return False, "Field 'customer_name' must be a string"
    
    if not isinstance(data['items'], list) or len(data['items']) == 0:
        return False, "Field 'items' must be a non-empty array"
    
    if not isinstance(data['total_amount'], (int, float)):
        return False, "Field 'total_amount' must be a number"
    
    # Validate items structure
    for i, item in enumerate(data['items']):
        if not isinstance(item, dict):
            return False, f"Item {i} must be an object"
        
        item_required_fields = ['name', 'quantity', 'unit_price']
        item_missing_fields = [field for field in item_required_fields if field not in item]
        
        if item_missing_fields:
            return False, f"Item {i} missing required fields: {', '.join(item_missing_fields)}"
    
    return True, "Valid"

@app.route('/')
def index():
    """Main page displaying quotations."""
    search_query = request.args.get('search', '').strip()
    customer_filter = request.args.get('customer', '').strip()
    
    filtered_quotations = quotations_storage.copy()
    
    # Apply search filter
    if search_query:
        filtered_quotations = [
            q for q in filtered_quotations 
            if search_query.lower() in str(q.get('id', '')).lower() 
            or search_query.lower() in q.get('customer_name', '').lower()
        ]
    
    # Apply customer filter
    if customer_filter:
        filtered_quotations = [
            q for q in filtered_quotations 
            if customer_filter.lower() in q.get('customer_name', '').lower()
        ]
    
    # Sort by received_at timestamp (newest first)
    filtered_quotations.sort(key=lambda x: x.get('received_at', ''), reverse=True)
    
    return render_template('index.html', 
                         quotations=filtered_quotations,
                         search_query=search_query,
                         customer_filter=customer_filter,
                         total_count=len(quotations_storage))

@app.route('/webhook/quotations', methods=['POST'])
def webhook_quotations():
    """Webhook endpoint for receiving quotation data."""
    try:
        # Check content type
        if not request.is_json:
            logger.warning(f"Invalid content type: {request.content_type}")
            return jsonify({
                'error': 'Invalid content type',
                'message': 'Content-Type must be application/json'
            }), 400
        
        # Parse JSON data
        try:
            data = request.get_json()
        except Exception as e:
            logger.error(f"JSON parsing error: {str(e)}")
            return jsonify({
                'error': 'Invalid JSON',
                'message': 'Request body must contain valid JSON'
            }), 400
        
        # Validate quotation data
        is_valid, error_message = validate_quotation_data(data)
        if not is_valid:
            logger.warning(f"Data validation failed: {error_message}")
            return jsonify({
                'error': 'Validation failed',
                'message': error_message
            }), 400
        
        # Add metadata
        quotation = data.copy()
        quotation['received_at'] = datetime.utcnow().isoformat()
        quotation['received_from_ip'] = request.remote_addr
        
        # Check for duplicate IDs
        existing_ids = [q.get('id') for q in quotations_storage]
        if quotation['id'] in existing_ids:
            logger.info(f"Updating existing quotation with ID: {quotation['id']}")
            # Update existing quotation
            for i, q in enumerate(quotations_storage):
                if q.get('id') == quotation['id']:
                    quotations_storage[i] = quotation
                    break
        else:
            # Add new quotation
            quotations_storage.append(quotation)
            logger.info(f"Added new quotation with ID: {quotation['id']}")
        
        return jsonify({
            'success': True,
            'message': 'Quotation received successfully',
            'id': quotation['id']
        }), 200
        
    except Exception as e:
        logger.error(f"Webhook processing error: {str(e)}")
        return jsonify({
            'error': 'Internal server error',
            'message': 'An unexpected error occurred while processing the request'
        }), 500

@app.route('/api/documentation')
def api_documentation():
    """API documentation page."""
    return render_template('documentation.html')

@app.route('/api/quotations')
def api_quotations():
    """API endpoint to retrieve all quotations."""
    return jsonify({
        'quotations': quotations_storage,
        'total_count': len(quotations_storage)
    })

@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'quotations_count': len(quotations_storage),
        'timestamp': datetime.utcnow().isoformat()
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
