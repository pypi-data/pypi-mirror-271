import requests
from web3 import Web3
from web3.auto import w3
from eth_account.messages import encode_defunct
import json

class FailSafeAttestationServiceAuth:
    def __init__(self, fs_attestation_service_base_url: str, chain_id: int, safe_address: str, safe_cli_owner: str, safe_cli_owner_private_key: str):
        self.fs_attestation_service_base_url = fs_attestation_service_base_url
        self.chain_id = chain_id
        self.safe_address = safe_address
        self.safe_cli_owner = safe_cli_owner
        self.safe_cli_owner_private_key = safe_cli_owner_private_key
        self.fs_api_key = "1Rm0ER9VPn8tNsQRQf7Iia9Koq7I33b728Ml7dvO"
        # TO DO - Remove below line
        self.fs_attestation_service_base_url = "https://1fw43grxlf.execute-api.us-east-1.amazonaws.com/v1"

    def initiate_auth(self):
        endpoint_url = "{}/auth/login".format(self.fs_attestation_service_base_url)
        headers = {
            'x-api-key': self.fs_api_key,
        }
        data = {
            'wallet_address': self.safe_address.lower(),
            'wallet_owner': self.safe_cli_owner.lower(),
            'chain_id': self.chain_id,
            'wallet_type': "gnosis",
        }
        response = requests.post(endpoint_url, json=data, headers=headers)
        return response.json()

    def sign_challenge(self, challenge):
        web3_instance = Web3()
        try:
            message_hash = encode_defunct(text=challenge)
            message_signed = w3.eth.account.sign_message(message_hash, private_key=self.safe_cli_owner_private_key)
            signature_hash = message_signed.signature.hex()
            return signature_hash
        except Exception as error:
            raise

    def verify_challenge(self, signature, session_token):
        endpoint_url = "{}/auth/login".format(self.fs_attestation_service_base_url)
        payload = {
            'wallet_address': self.safe_address.lower(),
            'wallet_owner': self.safe_cli_owner.lower(),
            'challengeResponse': { 'signature': signature, 'network_id': self.chain_id },
            'sessionToken': session_token,
            'chain_id': self.chain_id,
            'wallet_type': "gnosis"
        }

        # Configuration object with headers including the x-api-key
        headers = {
            'x-api-key': self.fs_api_key
        }

        try:
            response = requests.post(endpoint_url, json=payload, headers=headers)
            response_data = response.json()
            if 'AuthenticationResult' in response_data:
                return response_data
            else:
                raise Exception('Verification failed')
        except Exception as error:
            raise

    # Perform the authentication flow and returns the access token
    def fs_attestation_user_login(self) -> str:
        try:
            initiate_auth_response = self.initiate_auth()
            session_token = initiate_auth_response['Session']
            challenge = initiate_auth_response['ChallengeParameters']['message']

            signature = self.sign_challenge(challenge)
            verification_response = self.verify_challenge(signature, session_token)

            access_token = verification_response['AuthenticationResult']['AccessToken']
            return access_token
        except Exception as error:
            raise