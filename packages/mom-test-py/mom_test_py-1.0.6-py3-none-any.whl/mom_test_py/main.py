# test function
import requests  # Import the requests module
class Client:
    """A client for accessing the plasgate API."""

    def __init__(self, private_key, secret_key):
        self.private_key = private_key
        self.secret_key = secret_key
        self.baseUrl = "https://cloudapi.plasgate.com/rest"

    @property                   # to be without parentheses
    def messages(self) -> "MessageCreate":
        return MessageCreate(self.private_key, self.secret_key, self.baseUrl)

class MessageCreate:
    def __init__(self, private_key, secret_key, baseUrl):
        self.private_key = private_key
        self.secret_key = secret_key
        self.baseUrl = baseUrl

    def create(self, to, sender, content):
        if (self.validatePhoneNumber(to)):# on this------------------------
            url = f"{self.baseUrl}/batch-send" if isinstance(to, list) else f"{self.baseUrl}/send"
            url += f"?private_key={self.private_key}"

            self.validate_payload(to, content, sender)
            payload = self.normalizePayload(to, sender, content)
            headers = {'X-Secret': self.secret_key }

            response = requests.post(url, json=payload, headers=headers)
            print("Response:", response.text)
        else:
            print("Phone number must be start with +855 only")  

    def normalizePayload(self, to, sender, content):
        if isinstance(to, list):
            to = [number.lstrip('+') for number in to]
            payload = {
                "globals": {
                    "sender": sender
                },
                "messages": [
                    {
                        "to": to,
                        "content": content
                    }
                ]
            }
        else:
            to = to.lstrip('+')
            payload = {
                "to": to,
                "sender": sender,
                "content": content
            }

        return payload
    
    def validatePhoneNumber(self, to):
        if isinstance(to, list):
            return all(number.startswith("+855") for number in to)
        elif isinstance(to, str):
            return to.startswith("+855")
        else:
            print("Invalid phone number")

    def validate_length(self, value, max_length, error_message):
        if not isinstance(value, str):
            return False
        
        try:
            if len(value) > max_length:
                raise ValueError(error_message)
            return True
        except ValueError as e:
            print(e)
            return False

    def validate_type(self, value, expected_type, error_message):
        try:
            if not isinstance(value, expected_type):
                raise TypeError(error_message)
            return True
        except TypeError as e:
            print(e)
            return False
    
    def validate_payload(self, to, content, sender):
        self.validate_type(sender, str, "BAD REQUEST sender must be a string.")
        self.validate_type(content, str, "BAD REQUEST content must be a string.")
        self.validate_length(sender, 11, "BAD REQUEST sender must be only 11 characters.")
        self.validate_length(content, 160, "BAD REQUEST content available only 153 to 160 characters.")
        self.validatePhoneNumber(to)


# Example usage:
# private_key = "OJ1IEQ0c0AkuDjIXhsqsrf-7fKVY80L9S7o5xn_x8-sr5hLxCpy0LXbGwNbPPCN58xGzRjiKR5EYdhfgcdkVFw"
# secret_key = "$5$rounds=535000$ybjSgyF6bWxslwYY$C2k7qye80gZ8yEOD5y858Q1YTbuhtOqAwGvYyLueBJ3"

# client = Client(private_key, secret_key)
# message = client.messages.create(
#     to="+855977804485",
#     # to=["+855977804485","+8558962862015"],
#     content= "Welcome to sms plasgate",
#     sender= "SMS Info"
# )
