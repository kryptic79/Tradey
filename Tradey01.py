import requests

def Login():
    active = True
    refresh_token = input("Enter Refersh token: ")
    authLink = "https://login.questrade.com/oauth2/token?grant_type=refresh_token&refresh_token="
    token_url = authLink + refresh_token
    params = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token
    }
    response = requests.get(token_url, params=params)
   
    if response.status_code == 200:
        token_data = response.json()
        new_access_token = token_data.get('access_token')  # Use .get() to avoid KeyErrors
        token_type = token_data.get('token_type')
        new_refresh_token = token_data.get('refresh_token')
        api_server = token_data.get('api_server')

        print("New Access Token:", new_access_token)
        print("New Refresh Token:", new_refresh_token)
        print("API Server:", api_server)
    else:
        try:
            error_data = response.json()  # Extract detailed error if available
            print("Failed to refresh token:", error_data)
        except ValueError:
            print("Failed to refresh token: Unable to parse error response.")
 
    while active:  # Simplified condition check
        print("\nSelect one of the following options:")
        print("1. Get account balances")
        print("2. Exit")

        # Get user input
        choice = input("Enter your choice (1 or 2): ")

        # Handle user choices
        if choice == "1":
            print("Fetching account balances...")
            # Call the function to get account balances here
            Getbalances(api_server,new_access_token)
        elif choice == "2":
            print("Exiting the program. Goodbye!")
            active = False  # Break the loop
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

def getAccountsInfo(api_server,new_access_token):
    endpoint = "/v1/accounts"
    headers = {
        "Authorization": f"Bearer {new_access_token}"
    }
    url = f"{api_server}{endpoint}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        accounts_data = response.json()
        accounts_list = accounts_data.get('accounts', [])
        
        if accounts_list:
            # Assuming you want the first account's number
            account_number = accounts_list[0].get('number')
        else:
            print("No accounts found.")
            return None

        print("Accounts Data:", accounts_data)
        return account_number
 

    else:
        print(f"Error: {response.status_code}")
        print(response.json())
   

def Getbalances(api_server,new_access_token):
    balance = getAccountsInfo(api_server,new_access_token)
    endpoint = f"/v1/accounts/{balance}/balances"
    print(endpoint)
    headers = {
        "Authorization": f"Bearer {new_access_token}"
        }
    url = f"{api_server}{endpoint}"
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        accounts_data = response.json()
        print("Accounts Data:", accounts_data, "\n")
    else:
        print(f"Error: {response.status_code}")
        print(response.json())

Login()
