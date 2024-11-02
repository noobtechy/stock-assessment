# **Option Chain Data Fetching and Margin Calculation using Upstox API**
This document provides an overview of a Python script designed to fetch option chain data for specified instruments and calculate margin and premium earned for each contract. It utilizes the Upstox API, requiring authentication and the use of multiple endpoints for data processing.

---

## **Table of Contents**
1. [Introduction](#1-introduction)
2. [Dependencies](#2-dependencies)
3. [File Structure](#3-file-structure)
4. [Setup Instructions](#4-setup-instructions)
5. [Authentication](#5-authentication)
   - [5.1 Authorization Code Request](#51-authorization-code-request)
   - [5.2 Access Token Exchange](#52-access-token-exchange)
6. [Fetching Option Chain Data](#6-fetching-option-chain-data)
7. [Calculating Margin and Premium](#7-calculating-margin-and-premium)

---

## **1. Introduction**

This script fetches option chain data for selected stock indices or securities, filters the data based on user-defined parameters, and calculates the required margin and premium earned. The script interacts with the Upstox API, a trading and investing platform for Indian financial markets.

---

## **2. Dependencies**

The script requires the following libraries:
- `pandas`: For data manipulation and DataFrame handling.
- `requests`: For making HTTP requests to the Upstox API.
- `dotenv`: For loading environment variables from `.env` files.

---

## **3. File Structure**

```
project/
├── login.py              # Script to initiate login and retrieve code.
├── get_token.py          # Script to get access token.
├── main.py               # Main script that calls option chain and margin calculation functions.
├── option_chain.py       # Script to fetch option chain data based on instrument and expiry date.
├── margin_calculation.py # Script to calculate margin required and premium earned.
├── .env                  # File containing sensitive credentials.
├── README.md             # Project documentation.
└── requirements.txt      # List of required Python packages.
```

---

## **4. Setup Instructions**

1. **Install Dependencies**:

   Run the following command to install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

2. **Create a `.env` File**:

   Store your sensitive credentials in a `.env` file in the project directory. The `.env` file should look like this:

   ```plaintext
   # .env
   ACCESS_TOKEN=your_access_token
   REDIRECT_URI=your_redirect_uri
   CLIENT_ID=your_client_id/api_key
   CLIENT_SECRET=your_client_secret/api_secret
   CODE=code_obtained_after_login
   ```

3. **Workflow for Running the Scripts**:

   - **Step 1: Run `login.py`**:
     - This script initiates the login process and provides a URL for authorization.
     - Open the URL, log in, and you’ll receive an **access code**.
     - **Note:** Copy this access code and paste it in `.env`, as it will be needed in the next step.

   - **Step 2: Run `get_token.py`**:
     - Running this script exchanges the access code for an **access token**.
     - The access token will be printed in the console. Paste this token in `.env`, as it is required for authentication in `main.py`.

   - **Step 3: Run `main.py`**:
     - After obtaining the access token, run `main.py` to fetch option chain data, calculate the required margin, and compute the premium earned.
     - If the access token is still valid, you can directly run `main.py` without repeating Steps 1 and 2.
     - **Note:** When the access token expires, repeat Steps 1 and 2 to obtain a new access token before running `main.py`.

### **Handling Sensitive Information with `.env`**

All sensitive information, such as `CLIENT_ID`, `CLIENT_SECRET`, `CODE`, `ACCESS_TOKEN`, and `REDIRECT_URI`, is stored in a `.env` file. This setup improves security by keeping credentials separate from the codebase.

---

## **5. Authentication**

Upstox’s API requires OAuth 2.0 authentication. The process involves generating an authorization code and then exchanging it for an access token.

### **5.1 Authorization Code Request**

1. **Set Parameters**:  
   - `client_id`: Your Upstox API client ID.
   - `redirect_uri`: URL that Upstox redirects to with the authorization code.
   - `response_type`: Set to `"code"` for the authorization request.

2. **Construct URL**:  
   - Navigate to the generated URL in your browser, log in, and obtain the authorization code.

### **5.2 Access Token Exchange**

Use the authorization code to obtain an access token by sending a POST request to Upstox's token endpoint.

---

## **6. Fetching Option Chain Data**

The `get_option_chain_data()` function retrieves option chain data based on the specified instrument, expiry date, and option type (put or call).

- **Endpoint**: `https://api.upstox.com/v2/option/chain`
- **Parameters**:
  - `instrument_name`: Instrument name (e.g., `"NSE_INDEX|Nifty 50"`).
  - `expiry_date`: Expiry date of options (e.g., `"2024-11-28"`).
  - `side`: Option type, `"PE"` (put) or `"CE"` (call).

- **Response Processing**: Filters data to extract instrument key, strike price, bid or ask price, and other relevant fields.

---

## **7. Calculating Margin and Premium**

The `calculate_margin_and_premium()` function computes the margin required and premium earned for each option contract, submitting data in batches of up to 20 instruments (per API constraints).

- **Endpoint**: `https://api.upstox.com/v2/charges/margin`
- **Payload**:
  - `instrument_key`: Key of the instrument (formatted as `NSE_EQ|symbol`).
  - `quantity`: Quantity in multiples of lot size.
  - `transaction_type`: Set to `"SELL"` for margin calculation.
  - `price`: Bid or ask price.
  - `product`: Set to `"D"` for delivery.

- **Response Handling**: Extracts margin requirement data and calculates premium based on bid/ask price and lot size.