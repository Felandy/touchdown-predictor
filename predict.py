import requests
import pandas as pd

# === CONFIG ===
API_KEY = "YOUR_ODDS_API_KEY"  # replace with your Odds API key
SPORT = "americanfootball_nfl"
REGIONS = "us"  # odds from US sportsbooks
MARKETS = "player_props"
ODDS_URL = f"https://api.the-odds-api.com/v4/sports/{SPORT}/odds/"

# === GET ODDS ===
def fetch_odds():
    params = {
        "apiKey": API_KEY,
        "regions": REGIONS,
        "markets": MARKETS,
    }
    response = requests.get(ODDS_URL, params=params)
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}, {response.text}")
    return response.json()

# === PREDICTION LOGIC (DUMMY FOR NOW) ===
def predict_touchdowns(data):
    preds = []
    for game in data:
        for bookmaker in game.get("bookmakers", []):
            for market in bookmaker.get("markets", []):
                if market["key"] == "player_props":
                    for outcome in market.get("outcomes", []):
                        # Example prediction: higher chance if line <= 1.5
                        prob = 0.65 if outcome.get("point", 0) <= 1.5 else 0.35
                        preds.append({
                            "player": outcome["name"],
                            "line": outcome.get("point"),
                            "odds": outcome["price"],
                            "predicted_probability": prob
                        })
    return preds

# === MAIN ===
if __name__ == "__main__":
    odds_data = fetch_odds()
    predictions = predict_touchdowns(odds_data)

    # Save to Excel
    df = pd.DataFrame(predictions)
    df.to_excel("touchdown_predictions.xlsx", index=False)
    print("✅ Predictions saved to touchdown_predictions.xlsx")
