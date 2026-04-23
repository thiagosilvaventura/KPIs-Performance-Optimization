import pandas as pd
import numpy as np
from typing import Dict, List, Optional

class PerformanceAnalyzer:
    """
    A comprehensive tool for KPI analysis and performance optimization datasets.
    Designed to handle data cleaning, metric calculation, and summary reporting.
    """

    def __init__(self, dataframe: pd.DataFrame):
        self.df = dataframe
        self.results: Dict = {}

    def clean_data(self) -> pd.DataFrame:
        """
        Performs data sanitization by handling missing values and ensuring 
        correct data types for performance metrics.
        """
        # Dropping duplicates to ensure data integrity
        self.df = self.df.drop_duplicates()
        
        # Filling missing numeric values with the median to avoid skewing KPIs
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns
        self.df[numeric_cols] = self.df[numeric_cols].fillna(self.df[numeric_cols].median())
        
        return self.df

    def calculate_efficiency_kpis(self, input_col: str, output_col: str) -> pd.Series:
        """
        Calculates the efficiency ratio between a given input and output.
        Formula: (Output / Input) * 100
        """
        self.df['efficiency_ratio'] = (self.df[output_col] / self.df[input_col]) * 100
        # Handling potential division by zero
        self.df['efficiency_ratio'] = self.df['efficiency_ratio'].replace([np.inf, -np.inf], 0)
        return self.df['efficiency_ratio']

    def detect_performance_outliers(self, column: str, threshold: float = 3.0) -> pd.DataFrame:
        """
        Identifies performance bottlenecks using the Z-Score method.
        Values exceeding the threshold are flagged as anomalies/outliers.
        """
        z_scores = np.abs((self.df[column] - self.df[column].mean()) / self.df[column].std())
        self.df['is_outlier'] = z_scores > threshold
        return self.df[self.df['is_outlier']]

    def generate_summary_report(self) -> Dict:
        """
        Aggregates data to provide a high-level overview of performance health.
        Useful for risk assessment and management reporting.
        """
        self.results = {
            "total_records": len(self.df),
            "avg_efficiency": self.df['efficiency_ratio'].mean() if 'efficiency_ratio' in self.df else None,
            "outlier_count": self.df['is_outlier'].sum() if 'is_outlier' in self.df else None,
            "max_latency_risk": self.df.select_dtypes(include=[np.number]).max().to_dict()
        }
        return self.results

#Usage
if __name__ == "__main__":
    # Mock data for demonstration purposes
    data = {
        'request_count': [100, 150, 200, 50, 300],
        'success_count': [98, 145, 190, 10, 295], # Note the anomaly at index 3
        'latency_ms': [20, 25, 22, 500, 21]
    }
    
    sample_df = pd.DataFrame(data)
    
    # Initialize the Anal.
    analyzer = PerformanceAnalyzer(sample_df)
    
    # Execute Pipeline
    analyzer.clean_data()
    analyzer.calculate_efficiency_kpis(input_col='request_count', output_col='success_count')
    analyzer.detect_performance_outliers(column='latency_ms')
    
    report = analyzer.generate_summary_report()
    print("--- Performance Analysis Report ---")
    print(report)
