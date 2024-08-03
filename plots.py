import matplotlib.pyplot as plt
import pandas as pd
import definemetrics

metrics = {
    "Completeness": definemetrics.calculate_completeness(df),
    "Uniqueness": definemetrics.calculate_uniqueness(df),
    "Consistency": definemetrics.calculate_consistency(df, schema),
    "Conformity": definemetrics.calculate_conformity(df, formats),
    "Readability": definemetrics.calculate_readability(df),
    "Ease of Manipulation": definemetrics.calculate_ease_of_manipulation(df),
    "Accessibility": definemetrics.calculate_accessibility(df),
    "Integrity": definemetrics.calculate_integrity(df),
}

# Create the bar chart
metrics_df = pd.DataFrame(list(metrics.items()), columns=['Metric', 'Percentage'])

plt.figure(figsize=(12, 6))
plt.bar(metrics_df['Metric'], metrics_df['Percentage'], color='skyblue')
plt.xlabel('Metrics')
plt.ylabel('Percentage')
plt.title('Metrics Scores')
plt.xticks(rotation=45)
plt.ylim(0, 100)
plt.tight_layout()

# Show the bar chart
plt.show()