import pandas as pd

for i in range(1, 6):
    df1 = pd.read_csv(f'clustering/overall_metrics_trial{i}.txt', header=None)
    df2 = pd.read_csv(f'new_metrics/overall_metrics_trial{i}.txt', header=None)
    
    combined = pd.concat([df1, df2], ignore_index=True)
    
    combined.to_csv(f'new_metrics/combined_metrics_trial{i}.txt', index=False, header=False)
