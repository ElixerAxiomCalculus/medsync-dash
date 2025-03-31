import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

data = pd.read_csv('data/data.csv')

# Assuming 'usage' as the target variable
X = data[['Current_Stock', 'Days_Until_Expiry']]
y = data['Average_Daily_Usage']
model = RandomForestRegressor()
model.fit(X, y)
joblib.dump(model, 'models/model.pkl')
