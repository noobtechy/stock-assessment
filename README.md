# **Option Chain Data Fetching and Margin Calculation using Upstox API**
This document provides an overview of a Python script designed to fetch option chain data for specified instruments and calculate margin and premium earned for each contract. It utilizes the Upstox API, requiring authentication and the use of multiple endpoints for data processing.

---

## **Table of Contents**
1. [Introduction](#introduction)
2. [Dependencies](#dependencies)
3. [Authentication](#authentication)
4. [Fetching Option Chain Data](#fetching-option-chain-data)
5. [Calculating Margin and Premium](#calculating-margin-and-premium)

---

## **1. Introduction**

This script fetches option chain data for selected stock indices or securities, filters the data based on user-defined parameters, and calculates the required margin and premium earned. The script interacts with the Upstox API, a trading and investing platform for Indian financial markets.

---

## **2. Dependencies**

The script requires the following libraries:
- `pandas`: For data manipulation and DataFrame handling.
- `requests`: For making HTTP requests to the Upstox API.

Install dependencies via pip if necessary:

```bash
pip install pandas requests
```

---

## **3. Authentication**

Upstox’s API requires OAuth 2.0 authentication. The process involves generating an authorization code and then exchanging it for an access token.

### **3.1 Authorization Code Request**

1. **Set Parameters**:  
   - `client_id`: Your Upstox API client ID.
   - `redirect_uri`: URL that Upstox redirects to with the authorization code.
   - `response_type`: Set to `"code"` for the authorization request.

2. **Construct URL**:  
   - Navigate to the generated URL in your browser, log in, and obtain the authorization code.

### **3.2 Access Token Exchange**

Use the authorization code to obtain an access token by sending a POST request to Upstox's token endpoint.

---

## **4. Fetching Option Chain Data**

The `get_option_chain_data()` function retrieves option chain data based on the specified instrument, expiry date, and option type (put or call).

- **Endpoint**: `https://api.upstox.com/v2/option/chain`
- **Parameters**:
  - `instrument_name`: Instrument name (e.g., `"NSE_INDEX|Nifty 50"`).
  - `expiry_date`: Expiry date of options (e.g., `"2024-11-28"`).
  - `side`: Option type, `"PE"` (put) or `"CE"` (call).

- **Response Processing**: Filters data to extract instrument key, strike price, bid or ask price, and other relevant fields.


---

## **5. Calculating Margin and Premium**

The `calculate_margin_and_premium()` function computes the margin required and premium earned for each option contract, submitting data in batches of up to 20 instruments (per API constraints).

- **Endpoint**: `https://api.upstox.com/v2/charges/margin`
- **Payload**:
  - `instrument_key`: Key of the instrument (formatted as `NSE_EQ|symbol`).
  - `quantity`: Quantity in multiples of lot size.
  - `transaction_type`: Set to `"SELL"` for margin calculation.
  - `price`: Bid or ask price.
  - `product`: Set to `"D"` for delivery.

- **Response Handling**: Extracts margin requirement data and calculates premium based on bid/ask price and lot size.
