import requests

def register_miners(wallet_address: str):
    """Register a new user using the central API endpoint."""
    endpoint = "http://54.74.133.71/register_user"
    payload = {"wallet_address": wallet_address}

    with requests.Session() as session:
        response = session.post(endpoint, json=payload)
        if response.status_code == 200:
            # Extract miner information from the response
            miner_info = response.json()
            print("Response from server:", miner_info)  # Print server response for debugging or logging

            if 'wallet_address' in miner_info:
                # Notify the user of successful registration
                miner_address = miner_info['wallet_address']
                success_message = f"Miner registered successfully with wallet address: {miner_address}"
                return success_message
            elif miner_info == "User already exists":
                # Handle case where user has already registered
                already_registered_message = "User already exists. No need to register again."
                print(already_registered_message)  # Print relevant information to console or log
                return already_registered_message
            elif miner_info == "Invalid wallet address format":
                # Handle case where user has already registered
                already_registered_message = "Invalid wallet address format. Check Wallet address."
                print(already_registered_message)  # Print relevant information to console or log
                return already_registered_message

        else:
            # General error handling for unsuccessful attempts
            error_message = f"Failed to register user. Status code: {response.status_code}, Response: {response.json()}"
            print(error_message)  # Print error message to console or log
            return {"error": "Failed to register user.", "status_code": response.status_code}

        # Handle unexpected conditions or server messages
        unexpected_response_message = "Unexpected server response: {}".format(response.json())
        print(unexpected_response_message)
        return {"error": unexpected_response_message}



