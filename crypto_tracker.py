import requests
import csv

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    "vs_currency": "usd",
    "order": "market_cap_desc",
    "per_page": 10,
    "page": 1
}

try:
    response = requests.get(url, params=params, timeout=15)
    response.raise_for_status()

    coins = response.json()

    if not isinstance(coins, list):
        raise ValueError("Unexpected API response format.")

    if not coins:
        print("No cryptocurrency data was returned.")
    else:
        print("Top 10 Cryptocurrencies\n")

        for coin in coins:
            print("Name:", coin.get("name", "N/A"))
            print("Current Price: $", coin.get("current_price", "N/A"))
            print("24h Change:", coin.get("price_change_percentage_24h", "N/A"), "%")
            print("24h High: $", coin.get("high_24h", "N/A"))
            print("24h Low: $", coin.get("low_24h", "N/A"))
            print("-" * 30)

        with open("crypto_prices.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Name", "Current Price (USD)", "24h Change (%)",
                "24h High (USD)", "24h Low (USD)"
            ])

            for coin in coins:
                writer.writerow([
                    coin.get("name"),
                    coin.get("current_price"),
                    coin.get("price_change_percentage_24h"),
                    coin.get("high_24h"),
                    coin.get("low_24h")
                ])

        print("Data saved to crypto_prices.csv")

except requests.exceptions.Timeout:
    print("Error: The API request timed out. Please try again.")

except requests.exceptions.HTTPError as e:
    print("API error:", e.response.status_code)
    print("The API may have rate-limited the request.")

except requests.exceptions.RequestException as e:
    print("Network error:", e)

except ValueError as e:
    print("Data error:", e)