import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.performance_analyzer import PerformanceAnalyzer

# 1. Mock Data for Testing 
data = {
    'requests': [100, 150, 200, 50, 300, 120, 180],
    'success': [98, 145, 190, 10, 295, 115, 175],
    'latency_ms': [20, 25, 22, 850, 21, 24, 23]
}
df = pd.DataFrame(data)

# 2. Initialize and Run Analysis
analyzer = PerformanceAnalyzer(df)
analyzer.clean_data()
analyzer.calculate_efficiency_kpis(input_col='requests', output_col='success')
analyzer.detect_performance_outliers(column='latency_ms', threshold=2.0)

# 3. Print Results
report = analyzer.generate_summary_report()
print("--- Performance Analysis Summary ---")
print(f"Total Records: {report['total_records']}")
print(f"Avg Efficiency: {report['avg_efficiency']:.2f}%")
print(f"Outliers: {report['outlier_count']}")

# 4. Visualization
sns.set_theme(style="whitegrid")
plt.figure(figsize=(12, 6))
sns.scatterplot(data=analyzer.df, x='requests', y='success', hue='is_outlier', palette={True: 'red', False: 'blue'})
plt.title('System Efficiency & Outlier Detection Analysis')
plt.show()
