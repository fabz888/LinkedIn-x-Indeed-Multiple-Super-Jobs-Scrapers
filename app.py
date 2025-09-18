import os
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
import json
import csv
import io
from datetime import datetime

app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

@app.route('/api/jobs/filters', methods=['GET'])
def get_filters():
    """Get available filter options"""
    filters = {
        'job_types': ['fulltime', 'parttime', 'contract', 'internship'],
        'sources': ['linkedin', 'indeed', 'glassdoor', 'ziprecruiter', 'google'],
        'hours_old_options': [24, 72, 168, 720],  # 1 day, 3 days, 1 week, 1 month
        'results_options': [10, 20, 50, 100]
    }
    
    return jsonify(filters)

@app.route('/api/jobs/search', methods=['POST'])
def search_jobs():
    """Demo search endpoint - returns sample data"""
    try:
        data = request.get_json()
        search_term = data.get('search_term', '')
        location = data.get('location', '')
        job_type = data.get('job_type', None)
        is_remote = data.get('is_remote', False)
        results_wanted = data.get('results_wanted', 10)
        hours_old = data.get('hours_old', None)
        sources = data.get('sources', ['indeed'])
        
        # Sample job data for demonstration
        sample_jobs = [
            {
                "id": "demo_1",
                "title": f"Senior {search_term.title() if search_term else 'Developer'}",
                "company": "Tech Corp",
                "location": location or "San Francisco, CA",
                "salary_min": 120000,
                "salary_max": 180000,
                "job_type": job_type or "fulltime",
                "is_remote": is_remote,
                "posted_date": "2025-09-10",
                "source": sources[0] if sources else "demo",
                "url": "https://example.com/job1",
                "description": f"We are looking for a skilled {search_term if search_term else 'professional'} to join our team. This is a great opportunity to work with cutting-edge technology and make a real impact."
            },
            {
                "id": "demo_2", 
                "title": f"{search_term.title() if search_term else 'Developer'} - Remote",
                "company": "StartupXYZ",
                "location": "Remote",
                "salary_min": 100000,
                "salary_max": 150000,
                "job_type": job_type or "fulltime",
                "is_remote": True,
                "posted_date": "2025-09-11",
                "source": sources[0] if sources else "demo",
                "url": "https://example.com/job2",
                "description": f"Remote {search_term if search_term else 'position'} with flexible hours and great benefits. Join our innovative team!"
            },
            {
                "id": "demo_3",
                "title": f"Junior {search_term.title() if search_term else 'Developer'}",
                "company": "BigTech Inc",
                "location": location or "New York, NY",
                "salary_min": 80000,
                "salary_max": 120000,
                "job_type": job_type or "fulltime",
                "is_remote": is_remote,
                "posted_date": "2025-09-12",
                "source": sources[0] if sources else "demo",
                "url": "https://example.com/job3",
                "description": f"Entry-level {search_term if search_term else 'position'} perfect for recent graduates. Excellent mentorship and growth opportunities."
            }
        ]
        
        # Limit results based on results_wanted parameter
        limited_jobs = sample_jobs[:min(results_wanted, len(sample_jobs))]
        
        response = {
            'jobs': limited_jobs,
            'total_results': len(limited_jobs),
            'search_time': 0.5,
            'search_parameters': {
                'search_term': search_term,
                'location': location,
                'job_type': job_type,
                'is_remote': is_remote,
                'results_wanted': results_wanted,
                'hours_old': hours_old,
                'sources': sources
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs/analytics', methods=['POST'])
def get_analytics():
    """Get analytics data from job results"""
    try:
        data = request.get_json()
        jobs = data.get('jobs', [])
        
        analytics = {
            'total_jobs': len(jobs),
            'sources': {'demo': len(jobs)},
            'job_types': {'fulltime': len(jobs)},
            'locations': {},
            'companies': {},
            'salary_stats': {
                'min_salary': 80000,
                'max_salary': 180000,
                'avg_min_salary': 100000,
                'avg_max_salary': 150000
            }
        }
        
        for job in jobs:
            location = job.get('location', 'unknown')
            analytics['locations'][location] = analytics['locations'].get(location, 0) + 1
            
            company = job.get('company', 'unknown')
            analytics['companies'][company] = analytics['companies'].get(company, 0) + 1
        
        return jsonify(analytics)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/jobs/export', methods=['POST'])
def export_jobs():
    """Export job data"""
    try:
        data = request.get_json()
        jobs = data.get('jobs', [])
        format_type = data.get('format', 'json').lower()
        
        if not jobs:
            return jsonify({'error': 'No jobs data provided'}), 400
            
        if format_type == 'csv':
            # Create CSV
            output = io.StringIO()
            if jobs:
                fieldnames = jobs[0].keys()
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(jobs)
            
            csv_data = output.getvalue()
            output.close()
            
            return jsonify({
                'data': csv_data,
                'filename': f'jobs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                'content_type': 'text/csv'
            })
            
        elif format_type == 'json':
            json_data = json.dumps(jobs, indent=2)
            return jsonify({
                'data': json_data,
                'filename': f'jobs_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json',
                'content_type': 'application/json'
            })
            
        else:
            return jsonify({'error': 'Unsupported format. Use csv or json'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    # Create static directory if it doesn't exist
    if not os.path.exists('static'):
        os.makedirs('static')
    
    # Create a simple index.html if it doesn't exist
    index_path = os.path.join('static', 'index.html')
    if not os.path.exists(index_path):
        with open(index_path, 'w') as f:
            f.write('''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <link rel="icon" type="image/x-icon" href="/favicon.ico" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>JobHunter Pro - AI-Powered Job Search</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.jsx"></script>
  </body>
</html>''')
    
    app.run(host='0.0.0.0', port=5000, debug=True)