import pandas as pd

def get_dashboard_data(csv_path='mooccubex_label_train.csv'):
    print(f"Reading CSV file: {csv_path}")
    df = pd.read_csv(csv_path)

    num_rows = len(df)
    completeness = df.notnull().mean().to_dict()
    consistency = {col: df[col].nunique() / num_rows for col in df.columns}
    min_max = {col: {'min': df[col].min(), 'max': df[col].max()} for col in df.select_dtypes(include='number').columns}
    correlation = df.corr(numeric_only=True).to_dict()
    print("correlation:", correlation)

    return {
        'num_rows': num_rows,
        'completeness': completeness,
        'consistency': consistency,
        'min_max': min_max,
        'correlation': correlation,
        'columns': list(df.select_dtypes(include='number').columns)
    }
