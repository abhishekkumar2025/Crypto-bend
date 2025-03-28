import requests
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

def fetch_crypto_data(symbol, days=90):
    """Fetch historical price data for a given cryptocurrency symbol"""
    url = f"https://api.coingecko.com/api/v3/coins/{symbol}/market_chart?vs_currency=usd&days={days}"
    response = requests.get(url)
    data = response.json()

    # Convert to DataFrame
    df = pd.DataFrame(data["prices"], columns=["timestamp", "price"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")

    return df

def train_model(df):
    """Train XGBoost model on given crypto price data"""
    df["MA_3"] = df["price"].rolling(window=3).mean()
    df["MA_7"] = df["price"].rolling(window=7).mean()
    df["Price_Change_%"] = df["price"].pct_change() * 100
    df.dropna(inplace=True)

    X = df[["MA_3", "MA_7", "Price_Change_%"]]
    y = df["price"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = XGBRegressor(n_estimators=200, learning_rate=0.05, max_depth=3)
    model.fit(X_train, y_train)

    return model, X

def predict_next_price(model, X):
    """Predict the next hour's price"""
    latest_features = X.iloc[-1].values.reshape(1, -1)
    next_price = model.predict(latest_features)
    return float(next_price[0])

def get_prediction(coin_symbol: str):
    """Get prediction for a given coin symbol"""
    try:
        df = fetch_crypto_data(coin_symbol.lower())
        model, X = train_model(df)
        predicted_price = predict_next_price(model, X)
        current_price = df["price"].iloc[-1]
        
        return {
            "symbol": coin_symbol.upper(),
            "current_price": current_price,
            "predicted_price": predicted_price,
            "predicted_change_percent": ((predicted_price - current_price) / current_price) * 100
        }
    except Exception as e:
        raise Exception(f"Error predicting price for {coin_symbol}: {str(e)}")