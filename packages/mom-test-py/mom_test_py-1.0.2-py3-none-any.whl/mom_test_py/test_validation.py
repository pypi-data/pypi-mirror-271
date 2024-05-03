# import pytest
from .main import MessageCreate
from unittest.mock import MagicMock
import responses


class TestValidation:

    def test_validate_type_success(self):
        obj = MessageCreate(private_key="your_private_key", secret_key="your_secret_key", baseUrl="your_base_url")  
        # Test if the validation passes for the correct type
        assert obj.validate_type(5, int, "Error message") is True

    def test_validate_length_success(self):
        obj = MessageCreate(private_key="your_private_key", secret_key="your_secret_key", baseUrl="your_base_url")  
        
        # Test if the validation passes for the correct type and length
        assert obj.validate_length("string length", 15, "Error message") is True
        print("Validation success: Type is string and length is within limit")



class TestValidation:

    @responses.activate
    def test_create_sms(self):
        # Define the base URL
        base_url = "http://your_base_url"

        # Call the create method with valid arguments
        msg = MessageCreate(private_key="your_private_key", secret_key="your_secret_key", baseUrl=base_url)
        msg.create("+855977804485", "content", "sender")

        # Construct the expected URL
        expected_url = f"{base_url}/send?private_key=your_private_key"

        # Construct the expected JSON payload
        expected_json = {'to': '+855977804485', 'content': 'content', 'sender': 'sender'}

        # If secret key is provided, construct the expected headers
        expected_headers = {'X-Secret': 'your_secret_key'} if msg.secret_key else {}

        # Register the response
        responses.add(responses.POST, expected_url, json={}, status=200)

        # Perform assertions
        response = msg.create("+855977804485", "content", "sender")
        assert response.status_code == 200

        # Check that the correct URL, JSON payload, and headers were used in the request
        assert len(responses.calls) == 1
        request = responses.calls[0].request
        assert request.url == expected_url
        assert request.method == 'POST'
        assert request.headers == expected_headers
        assert request.json() == expected_json


# class TestValidation:

#     def test_create_sms(self, monkeypatch):
#         # Define a mock post function
#         mock_post = MagicMock()

#         # Patch requests.post to use the mock_post function
#         monkeypatch.setattr("requests.post", mock_post)

#         # Call the create method with valid arguments
#         msg = MessageCreate(private_key="your_private_key", secret_key="your_secret_key", baseUrl="http://your_base_url")
#         msg.create("+855977804485", "content", "sender")

#         # Construct the expected URL
#         expected_url = "http://your_base_url/send?private_key=your_private_key"

#         # Construct the expected JSON payload
#         expected_json = {'to': '+855977804485', 'content': 'content', 'sender': 'sender'}

#         # Construct the expected headers
#         expected_headers = {'X-Secret': 'your_secret_key'}

#         # Assert that requests.post was called with the expected arguments
#         if "your_secret_key" in msg.secret_key:
#             mock_post.assert_called_once_with(expected_url, json=expected_json, headers=expected_headers)
#         else:
#             mock_post.assert_called_once_with(expected_url, json=expected_json)










# def test_create_sms(self, monkeypatch):  # Ensure the test method accepts 'self' as the first argument
#     # Define a mock post function
#     mock_post = MagicMock()

#     # Patch requests.post to use the mock_post function
#     monkeypatch.setattr("requests.post", mock_post)

#     # Call the create method with valid arguments
#     msg = MessageCreate(private_key="your_private_key", secret_key="your_secret_key", baseUrl="http://your_base_url")
#     msg.create("+855977804485", "content", "sender")

#     # Construct the expected URL
#     expected_url = "http://your_base_url/send?private_key=your_private_key"

#     # Construct the expected JSON payload
#     expected_json = {'to': '+855977804485', 'content': 'content', 'sender': 'sender'}

#     # Assert that requests.post was called with the expected arguments
#     mock_post.assert_called_once_with(expected_url, json=expected_json)


# def test_create_sms(monkeypatch):
#     # Define a mock post function
#     mock_post = MagicMock()

#     # Patch requests.post to use the mock_post function
#     monkeypatch.setattr("requests.post", mock_post)

#     # Call the create method with valid arguments
#     msg = MessageCreate(private_key="your_private_key", secret_key="your_secret_key", baseUrl="http://your_base_url")
#     msg.create("+855977804485", "content", "sender")

#     # Construct the expected URL
#     expected_url = "http://your_base_url/send"

#     # Construct the expected JSON payload
#     expected_json = {'to': '+855977804485', 'content': 'content', 'sender': 'sender', 'private_key': 'your_private_key'}

#     # Assert that requests.post was called with the expected arguments
#     mock_post.assert_called_once_with(expected_url, json=expected_json)



# class TestPhoneNumberValidator:
#     @pytest.mark.parametrize("phone_numbers, expected_result", [
#         ("+85512345678", True),
#         (["+85512345678", "+85587654321"], True),
#     ])
#     def test_numbers(self, phone_numbers, expected_result):
#         validator = validatePhoneNumber()
#         assert validator.validatePhoneNumber(phone_numbers) == expected_result












    # def test_create_sms(monkeypatch):
    #     # Define a mock post function
    #     mock_post = MagicMock()

    #     # Patch requests.post to use the mock_post function
    #     monkeypatch.setattr("requests.post", mock_post)

    #     # Call the create method with valid arguments
    #     msg = MessageCreate(private_key="your_private_key", secret_key="your_secret_key", baseUrl="http://your_base_url")
    #     msg.create("+855977804485", "content", "sender")

    #     # Construct the expected URL
    #     expected_url = "http://your_base_url/send?private_key=your_private_key"

    #     # Construct the expected JSON payload
    #     expected_json = {'to': '+855977804485', 'content': 'content', 'sender': 'sender'}

    #     # Assert that requests.post was called with the expected arguments
    #     mock_post.assert_called_once_with(expected_url, json=expected_json)
