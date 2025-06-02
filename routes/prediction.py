from flask import Blueprint, render_template, request
from connectDB import connect_mysql

model_bp = Blueprint('model', __name__)
conn = connect_mysql()

@model_bp.route('/model', methods=['GET', 'POST'])
def model():
    return render_template('model.html')