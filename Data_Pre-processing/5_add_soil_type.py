"""Add `soil_type` column to dataset based on soil moisture.

This script will:
- Read an input CSV (default: `data/crop_data.csv`).
- Determine which column to use for soil moisture. If `soil_moisture` exists it will be used.
  Otherwise a proxy column can be specified (default: `humidity`).
- Impute missing moisture values using `sklearn.impute.KNNImputer` across numeric features.
- Map moisture to `soil_type` categories using configurable thresholds.
- Write the result to a new CSV (default: `data/crop_data_with_soiltype.csv`).

Usage:
    python 5_add_soil_type.py --input ../data/crop_data.csv --output ../data/crop_data_with_soiltype.csv

Defaults are conservative; adjust `--proxy-column` or `--thresholds` as needed.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.cluster import KMeans


def parse_thresholds(s: str):
    """Parse thresholds argument like '30,60' to [30.0,60.0]."""
    parts = [p.strip() for p in s.split(',') if p.strip()]
    if len(parts) != 2:
        raise ValueError("--thresholds must be two comma-separated numbers, e.g. 30,60")
    return [float(parts[0]), float(parts[1])]


def assign_soil_type_from_moisture(moisture, thresholds, labels):
    """Map numeric moisture to a soil type label.

    thresholds: [t1, t2] means:
      moisture < t1 => labels[0]
      t1 <= moisture <= t2 => labels[1]
      moisture > t2 => labels[2]
    """
    t1, t2 = thresholds
    if pd.isna(moisture):
        return np.nan
    try:
        m = float(moisture)
    except Exception:
        return np.nan
    if m < t1:
        return labels[0]
    if m <= t2:
        return labels[1]
    return labels[2]


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-i', default='../data/crop_data.csv', help='Input CSV path')
    parser.add_argument('--output', '-o', default='../data/crop_data_with_soiltype.csv', help='Output CSV path')
    parser.add_argument('--moisture-column', '-m', default=None,
                        help=('Column name that contains soil moisture. If not provided, '
                              'the script will look for `soil_moisture`. If missing, it will use the proxy column.'))
    parser.add_argument('--proxy-column', '-p', default='humidity', help='Proxy column to use when soil_moisture is absent (default: humidity)')
    parser.add_argument('--k', type=int, default=5, help='`k` for KNNImputer (default: 5)')
    parser.add_argument('--method', choices=['threshold','kmeans'], default='kmeans',
                        help="Method to assign soil_type: 'threshold' uses numeric thresholds; 'kmeans' uses clustering on moisture-related features (default: kmeans)")
    parser.add_argument('--thresholds', '-t', default='30,60', help='Two comma-separated moisture thresholds, e.g. "30,60"')
    parser.add_argument('--labels', '-l', default='sandy,petmos,clay', help='Comma-separated labels for the three soil types in order (low, mid, high)')
    args = parser.parse_args(argv)

    input_path = Path(args.input).expanduser()
    output_path = Path(args.output).expanduser()

    if not input_path.exists():
        print(f"ERROR: input file not found: {input_path}")
        return 2

    df = pd.read_csv(input_path)
    print(f"Loaded {input_path} with shape {df.shape}")

    # Determine moisture column
    moisture_col = args.moisture_column
    if moisture_col is None:
        if 'soil_moisture' in df.columns:
            moisture_col = 'soil_moisture'
            print("Using existing 'soil_moisture' column from dataset.")
        else:
            moisture_col = args.proxy_column
            print(f"No 'soil_moisture' column found. Using proxy column '{moisture_col}' (change with --proxy-column).")

    if moisture_col not in df.columns:
        print(f"ERROR: chosen moisture/proxy column '{moisture_col}' not found in dataset columns: {list(df.columns)}")
        return 3

    # Prepare numeric columns for imputation
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if moisture_col not in numeric_cols:
        # try to coerce the moisture column to numeric
        df[moisture_col] = pd.to_numeric(df[moisture_col], errors='coerce')
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    print(f"Numeric columns used for KNN imputation: {numeric_cols}")

    # Use KNNImputer to impute missing values in numeric columns (including moisture_col if it has NaNs)
    imputer = KNNImputer(n_neighbors=max(1, args.k))
    numeric_df = df[numeric_cols]
    numeric_imputed = imputer.fit_transform(numeric_df)
    numeric_df_imputed = pd.DataFrame(numeric_imputed, columns=numeric_cols, index=df.index)

    # Put imputed moisture back into df
    df[numeric_cols] = numeric_df_imputed

    # Parse thresholds and labels
    thresholds = parse_thresholds(args.thresholds)
    labels = [s.strip() for s in args.labels.split(',')]
    if len(labels) != 3:
        raise ValueError("--labels must provide exactly three comma-separated labels")

    # Assign soil_type according to chosen method
    if args.method == 'threshold':
        df['soil_type'] = df[moisture_col].apply(lambda v: assign_soil_type_from_moisture(v, thresholds, labels))
    else:
        # KMeans clustering on moisture-related numeric features. Choose features that correlate with soil moisture.
        candidate_features = ['humidity', 'rainfall', 'temperature']
        features = [f for f in candidate_features if f in df.columns and f in numeric_cols]
        if not features:
            # fallback to moisture_col only
            features = [moisture_col]
        print(f"Clustering using features: {features}")

        X_cluster = df[features].fillna(df[features].mean()).values
        # normalize features to zero mean, unit variance for clustering
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        Xs = scaler.fit_transform(X_cluster)

        kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
        labels_cluster = kmeans.fit_predict(Xs)

        # Determine ordering of clusters by mean of the moisture proxy (use moisture_col if present else humidity)
        cluster_order = []
        cluster_stats = {}
        for c in range(3):
            mask = labels_cluster == c
            # use moisture_col as moisture proxy if numeric
            proxy_col = moisture_col if moisture_col in numeric_cols else (features[0] if features else None)
            proxy_mean = float(np.nan)
            if proxy_col is not None:
                proxy_mean = float(df.loc[mask, proxy_col].mean())
            cluster_stats[c] = proxy_mean
        # order clusters by proxy_mean ascending -> sandy (low), petmos (mid), clay (high)
        ordered = sorted(cluster_stats.items(), key=lambda x: (np.nan_to_num(x[1], nan=-np.inf)))
        mapping = {cluster_id: labels[idx] for idx, (cluster_id, _) in enumerate(ordered)}
        # Assign mapped soil_type
        df['soil_type'] = [mapping[int(c)] for c in labels_cluster]

    # Report counts
    counts = df['soil_type'].value_counts(dropna=False)
    print("Soil type distribution (after imputation):")
    print(counts.to_string())

    # Save output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"Wrote output to {output_path}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))
