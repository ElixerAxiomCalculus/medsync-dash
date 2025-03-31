#Training the Random Forest Model
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Load dataset
data = pd.read_csv('data/data.csv')

# Assuming 'usage' as the target variable
X = data[['Current_Stock', 'Days_Until_Expiry']]
y = data['Average_Daily_Usage']

# Train model
model = RandomForestRegressor()
model.fit(X, y)

# Save the trained model
joblib.dump(model, 'models/model.pkl')
