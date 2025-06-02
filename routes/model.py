import os
import pandas as pd
import numpy as np
from flask import Blueprint, render_template, request, redirect, url_for, flash
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report
import joblib
from connectDB import connect_mysql

model_bp = Blueprint('model', __name__)
CSV_PATH = "csv/moocubex_label_train.csv"
MODEL_PATH = "model/random_forest_model.pkl"
FEATURE_PATH = "model/rf_feature_names.npy"
conn = connect_mysql()

def load_csv():
    if not os.path.exists(CSV_PATH):
        return None
    df = pd.read_csv(CSV_PATH)
    return df

def load_model_and_features():
    model = joblib.load(MODEL_PATH)
    feature_names = np.load(FEATURE_PATH, allow_pickle=True)
    return model, feature_names

@model_bp.route('/model', methods=['GET'])
def model_home():
    return render_template('model.html')

@model_bp.route('/model/predict', methods=['GET'])
def prediction():
    df = load_csv()
    if df is None or 'cluster' not in df.columns:
        flash("CSV chưa tồn tại hoặc không có cột 'cluster'.", 'danger')
        return redirect(url_for('model.model_home'))

    model, feature_names = load_model_and_features()
    X = df[feature_names]
    predictions = model.predict(X)
    df['prediction'] = predictions

    # Ghi ra file
    df[['user_ids', 'prediction']].to_csv("csv/predicted.csv", index=False)

    # Lưu vào database
    try:
        cursor = conn.cursor()

        # Xóa dữ liệu cũ
        cursor.execute("DELETE FROM user_predict")

        # Thêm dữ liệu mới
        insert_query = "INSERT INTO user_predict (uid, predict) VALUES (%s, %s)"
        data_to_insert = list(zip(df['user_ids'], df['prediction']))
        batch_size = 1000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i+batch_size]
            cursor.executemany(insert_query, batch)

        conn.commit()
        cursor.close()
        conn.close()

        flash("Đã thực hiện dự đoán và lưu kết quả vào predicted.csv và CSDL.", 'success')
    except Exception as e:
        flash(f"Lỗi khi ghi vào CSDL: {e}", 'danger')

    return redirect(url_for('model.model_home'))

@model_bp.route('/model/evaluate', methods=['GET'])
def evaluate():
    df = load_csv()
    if df is None or 'cluster' not in df.columns:
        flash("CSV chưa tồn tại hoặc không có cột 'cluster'.", 'danger')
        return redirect(url_for('model.model_home'))

    model, feature_names = load_model_and_features()
    X = df[feature_names]
    y_true = df['cluster']
    y_pred = model.predict(X)

    acc = accuracy_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred, average='macro')

    report_dict = classification_report(y_true, y_pred, output_dict=True)
    report_df = pd.DataFrame(report_dict).transpose()
    report_html = report_df.to_html(classes="table table-bordered table-sm", float_format="%.4f")

    return render_template(
        'model.html',
        acc=acc,
        f1=f1,
        report_html=report_html,
        features_used=feature_names
    )

@model_bp.route('/model/retrain', methods=['GET'])
def retrain():
    df = load_csv()
    if df is None or 'cluster' not in df.columns:
        flash("CSV chưa tồn tại hoặc không có cột 'cluster'.", 'danger')
        return redirect(url_for('model.model_home'))

    y = df['cluster']
    X = df.drop(columns=['user_ids', 'label'], errors='ignore')
    feature_names = X.columns

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    np.save(FEATURE_PATH, feature_names)

    # Evaluate again
    y_pred = model.predict(X)
    acc = accuracy_score(y, y_pred)
    f1 = f1_score(y, y_pred, average='macro')

    flash("Model retrained successfully.", 'success')
    flash(f"Accuracy after retraining: {acc:.4f}", 'info')
    flash(f"F1 Score after retraining: {f1:.4f}", 'info')
    return redirect(url_for('model.model_home'))
