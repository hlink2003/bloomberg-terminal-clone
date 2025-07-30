# src/ai/price_predictor.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class PricePredictor:
    def __init__(self):
        self.model = None
        self.scaler = StandardScaler()
        self.feature_columns = []
        self.is_trained = False
    
    def prepare_features(self, stock_data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for machine learning"""
        if stock_data.empty:
            return pd.DataFrame()
        
        df = stock_data.copy()
        
        # Technical indicators
        df['Returns'] = df['Close'].pct_change()
        df['Volume_MA'] = df['Volume'].rolling(window=10).mean()
        df['Price_MA_5'] = df['Close'].rolling(window=5).mean()
        df['Price_MA_10'] = df['Close'].rolling(window=10).mean()
        df['Price_MA_20'] = df['Close'].rolling(window=20).mean()
        
        # Volatility
        df['Volatility'] = df['Returns'].rolling(window=10).std()
        
        # Price position indicators
        df['High_Low_Ratio'] = df['High'] / df['Low']
        df['Close_Open_Ratio'] = df['Close'] / df['Open']
        
        # Momentum indicators
        df['Momentum_3'] = df['Close'] / df['Close'].shift(3)
        df['Momentum_5'] = df['Close'] / df['Close'].shift(5)
        
        # RSI (if available)
        if 'RSI' in df.columns:
            df['RSI_normalized'] = df['RSI'] / 100
        
        # Bollinger Bands
        df['BB_upper'] = df['Price_MA_20'] + (df['Close'].rolling(window=20).std() * 2)
        df['BB_lower'] = df['Price_MA_20'] - (df['Close'].rolling(window=20).std() * 2)
        df['BB_position'] = (df['Close'] - df['BB_lower']) / (df['BB_upper'] - df['BB_lower'])
        
        # Feature columns (exclude target and non-predictive columns)
        feature_cols = [
            'Volume_MA', 'Price_MA_5', 'Price_MA_10', 'Price_MA_20',
            'Volatility', 'High_Low_Ratio', 'Close_Open_Ratio',
            'Momentum_3', 'Momentum_5', 'BB_position'
        ]
        
        if 'RSI_normalized' in df.columns:
            feature_cols.append('RSI_normalized')
        
        # Remove rows with NaN values
        df = df.dropna()
        
        return df[feature_cols]
    
    def train_model(self, stock_data: pd.DataFrame, target_days: int = 1) -> Dict:
        """Train the prediction model"""
        if stock_data.empty:
            return {'success': False, 'error': 'No data provided'}
        
        # Prepare features
        features_df = self.prepare_features(stock_data)
        
        if features_df.empty:
            return {'success': False, 'error': 'Could not prepare features'}
        
        # Prepare target (future price)
        target = stock_data['Close'].shift(-target_days).dropna()
        
        # Align features and target
        min_len = min(len(features_df), len(target))
        X = features_df.iloc[:min_len]
        y = target.iloc[:min_len]
        
        if len(X) < 20:  # Need minimum data points
            return {'success': False, 'error': 'Insufficient data for training'}
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, shuffle=False
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        self.model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            max_depth=10
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        self.feature_columns = list(X.columns)
        self.is_trained = True
        
        return {
            'success': True,
            'mse': mse,
            'r2_score': r2,
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict_price(self, stock_data: pd.DataFrame, days_ahead: int = 1) -> Dict:
        """Predict future price"""
        if not self.is_trained:
            train_result = self.train_model(stock_data)
            if not train_result['success']:
                return {'success': False, 'error': 'Could not train model'}
        
        # Prepare features for the latest data point
        features_df = self.prepare_features(stock_data)
        
        if features_df.empty:
            return {'success': False, 'error': 'Could not prepare features for prediction'}
        
        # Get the most recent features
        latest_features = features_df.iloc[-1:][self.feature_columns]
        
        # Scale features
        latest_features_scaled = self.scaler.transform(latest_features)
        
        # Make prediction
        prediction = self.model.predict(latest_features_scaled)[0]
        current_price = stock_data['Close'].iloc[-1]
        
        # Calculate confidence (simplified)
        confidence = max(0.1, min(0.9, self.model.score(
            self.scaler.transform(features_df[self.feature_columns]), 
            stock_data['Close'].iloc[:len(features_df)]
        )))
        
        return {
            'success': True,
            'predicted_price': prediction,
            'current_price': current_price,
            'predicted_change': prediction - current_price,
            'predicted_change_pct': ((prediction - current_price) / current_price) * 100,
            'confidence': confidence,
            'days_ahead': days_ahead
        }
    
    def get_feature_importance(self) -> Dict:
        """Get feature importance from the trained model"""
        if not self.is_trained or not hasattr(self.model, 'feature_importances_'):
            return {}
        
        importance_dict = {}
        for feature, importance in zip(self.feature_columns, self.model.feature_importances_):
            importance_dict[feature] = importance
        
        # Sort by importance
        sorted_importance = dict(sorted(importance_dict.items(), key=lambda x: x[1], reverse=True))
        
        return sorted_importance