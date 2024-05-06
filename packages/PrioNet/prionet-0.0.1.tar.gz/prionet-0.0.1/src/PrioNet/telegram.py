'''
Author: Giuseppe Priolo
Date: 2024-05-03
Description: Useful functions to interact with Telegram api.
'''
import os
import requests

class Telegram:
    def __init__(self, api_key=None, chat_id=None):
        # Set the chatID and the apiToken
        self.api_key = api_key
        self.chat_id = chat_id

    def send_to_telegram(self, message):
        # Set the URL
        apiURL = f'https://api.telegram.org/bot{self.api_key}/sendMessage'
        # Send a message to the chat
        requests.post(apiURL, json={'chat_id': self.chat_id, 'text': message})