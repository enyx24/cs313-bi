from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
import os
from connectDB import connect_mysql
from stats import get_stats_data
from dashboard import get_dashboard_data
from routes.search import search_bp
from routes.user import user_bp
from routes.course import course_bp
from routes.model import model_bp


# Flask app
app = Flask(__name__)
conn = connect_mysql()
app.register_blueprint(search_bp)
app.register_blueprint(user_bp)
app.register_blueprint(course_bp)
app.register_blueprint(model_bp)

app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'csv')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Flask routes
@app.route('/')
def home():
    return render_template("home.html")

@app.route('/stats')
def stats():
    # return render_template("unavailable.html")
    data = get_stats_data(conn)
    return render_template("stats.html", **data)

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    csv_path = session.get('current_csv', 'mooccubex_final.csv')
    data = get_dashboard_data(csv_path)

    selected_correlation = []
    filtered_corr = {}

    if request.method == 'POST':
        selected_correlation = request.form.getlist('selected_cols')
        if selected_correlation:
            filtered_corr = {
                row: {
                    col: data['correlation'][row][col]
                    for col in selected_correlation
                    if col in data['correlation'][row]
                }
                for row in selected_correlation
            }

    return render_template('dashboard.html',
                           data=data,
                           selected_correlation=selected_correlation,
                           selected_correlation_data=filtered_corr)

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    if 'csv_file' not in request.files:
        flash('No file part')
        return redirect(url_for('dashboard'))

    file = request.files['csv_file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('dashboard'))

    if file and file.filename.endswith('.csv'):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        session['current_csv'] = filepath  # set file dùng cho dashboard
        flash(f'Uploaded {filename} successfully!')
        return redirect(url_for('dashboard'))

    flash('Invalid file type. Please upload a CSV file.')
    return redirect(url_for('dashboard'))

# Route chi tiết tạm thời
# @app.route('/user/<uid>')
# def user_detail(uid):
#     return f"<h2>Thông tin người dùng: {uid}</h2>"

# @app.route('/course/<cid>')
# def course_detail(cid):
#     return f"<h2>Thông tin khóa học: {cid}</h2>"


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
