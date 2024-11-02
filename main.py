import pandas as pd
import requests
import os
import dotenv

dotenv.load_dotenv(override=True)

access_token = os.getenv("ACCESS_TOKEN")
# Define the first function to fetch option chain data
def get_option_chain_data(instrument_name: str, expiry_date: str, side: str) -> pd.DataFrame:

    url = 'https://api.upstox.com/v2/option/chain'
    params = {
        'instrument_key': instrument_name,
        'expiry_date': expiry_date
    }
    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

    response = requests.get(url, params=params, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch option chain data")
        return pd.DataFrame()
    
    option_chain = response.json().get("data", [])
    
    # Process and filter data based on side
    data = []
    for option in option_chain:
        if side == "PE" and 'put_options' in option:
            instrument_key = option['put_options']['instrument_key']
            price = option['put_options']['market_data']['bid_price']
            data.append([instrument_name, option['strike_price'], "PE", price, instrument_key])
        elif side == "CE" and 'call_options' in option:
            instrument_key = option['call_options']['instrument_key']
            price = option['call_options']['market_data']['ask_price']
            data.append([instrument_name, option['strike_price'], "CE", price, instrument_key])

    # Create DataFrame
    df = pd.DataFrame(data, columns=["instrument_name", "strike_price", "side", "bid/ask", "instrument_key"])
    return df

# Define the second function to calculate margin and premium earned
def calculate_margin_and_premium(data: pd.DataFrame) -> pd.DataFrame:

    url = "https://api.upstox.com/v2/charges/margin"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    lot_size = 50  # Example lot size
    
    # Initialize columns for margin_required and premium_earned
    margin_required_list = []
    premium_earned_list = []

    # Prepare payload for margin calculation
    instruments_payload = []
    
    # Gather payload for all instruments
    for index, row in data.iterrows():
        instruments_payload.append({
            "instrument_key": row["instrument_key"],
            "quantity": lot_size,  # Set the quantity based on lot size
            "transaction_type": "SELL",  # Assuming we're selling
            "product": "D",  # Delivery or product type
            "price": row["bid/ask"]
        })

    # Prepare the final payload for the API request
    final_payload = {
        "instruments": instruments_payload
    }
    
    for index, row in data.iterrows():
        transaction_type = "SELL"  # Assuming we are calculating margin for sell positions

        # Prepare payload for margin calculation
        payload = {
            "instruments": [
                {
                    "instrument_key": row["instrument_key"],
                    "quantity": 1 * lot_size, # Adjust accordingly
                    "transaction_type": transaction_type,
                    "product": "D",  # Delivery or product type
                    "price": row["bid/ask"]
                }
            ]
        }
        
        # Fetch margin data
        response = requests.post(url, headers=headers, json=payload)
        margin_data = response.json().get("data", {}).get("required_margin", 0)
        
        # Append margin and premium data
        margin_required_list.append(margin_data)
        premium_earned_list.append(row["bid/ask"] * lot_size)

    # Add new columns to DataFrame
    data["margin_required"] = margin_required_list
    data["premium_earned"] = premium_earned_list
    
    return data


# Example usage
if __name__ == "__main__":
    # Specify the instrument, expiry date, and option type (CE or PE)
    instrument_name = 'NSE_INDEX|Nifty 50'
    expiry_date = '2024-11-28'
    side = 'PE'  # Can be 'CE' for Call options as well

    # Fetch option chain data
    option_data = get_option_chain_data(instrument_name, expiry_date, side)
    print("Option Chain Data:")
    print(option_data)

    # Calculate margin and premium
    final_data = calculate_margin_and_premium(option_data)
    print("Final Data:")
    print(final_data)