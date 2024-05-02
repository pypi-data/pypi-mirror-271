import json
import requests

class WhatsAppClient:
    """
    A class that encapsulates WhatsApp messaging functionalities.
    """

    def __init__(self, base_url="https://graph.facebook.com/v18.0/"):
        self.base_url = base_url
        self._auth_token = None
        self._from_number_id = None
        
    def set_credentials(self, auth_token, from_number_id):
        """
        Set the WhatsApp authentication token and from number ID.

        Args:
            auth_token: The WhatsApp authentication token.
            from_number_id: The WhatsApp from number ID.
        """
        self.auth_token = auth_token
        self.from_number_id = from_number_id

    @property
    def auth_token(self):
        if not self._auth_token:
            raise ValueError("WhatsApp authentication token not set")
        return self._auth_token

    @auth_token.setter
    def auth_token(self, token):
        self._auth_token = token

    @property
    def from_number_id(self):
        if not self._from_number_id:
            raise ValueError("WhatsApp from number ID not set")
        return self._from_number_id

    @from_number_id.setter
    def from_number_id(self, number_id):
        self._from_number_id = number_id

    def build_custom_message(self, to_number, message, username):
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "to": to_number,
                "recipient_type": "individual",
                "type": "text",
                "text": {"preview_url": "false", "body": message.format(username)},
            }
        )

    def build_message_using_template(self, template_name, to_number, lang_code, header, body, button_link):
        components = self.generate_components(header, body, button_link)
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": to_number,
                "type": "template",
                "template": {
                    "name": template_name,
                    "language": {"code": lang_code},
                    "components": components["components"],
                },
            }
        )
    
    def generate_components(self,header, body, button_link):
        """
        This function generates a components object with header, body and button sections,
        adding only sections with at least one element.

        Args:
            header: List containing text elements for the header section.
            body: List containing text elements for the body section.
            button_link: List containing text element for the button text.

        Returns:
            A dictionary containing the generated components object.
        """

        components = []

        # Add header section if it has elements
        if header:
            header_section = {
                "type": "header",
                "parameters": [{"type": "text", "text": text} for text in header],
            }
            components.append(header_section)

        # Add body section if it has elements
        if body:
            body_section = {
                "type": "body",
                "parameters": [{"type": "text", "text": text} for text in body],
            }
            components.append(body_section)

        # Add button section if it has elements
        if button_link:
            button_section = {
                "type": "button",
                "sub_type": "Url",
                "index": "0",
                "parameters": [{"type": "text", "text": button_link[0]}],
            }
            components.append(button_section)

        return {"components": components}

    def send_message(self,payload, max_retries=3, base_timeout=2):
        """
        Makes a request with exponential backoff for retries on timeout.

        Args:
            payload: the data to be posted to whatapp
            url: The URL to send the request to.
            headers: Carries mainly the authorization header, the content-type and any other necessary headers
            max_retries: The maximum number of retries to attempt (default: 3).
            base_timeout: The base timeout value in seconds (default: 2).

        Returns:
            The response object from a successful request.

        Raises:
            requests.exceptions.RequestException: If the request fails after all retries or if the is a another RequestException type error
        """
        url = f"{self.base_url}{self.from_number_id}/messages"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}",
        }
        for attempt in range(1, max_retries + 1):
            timeout_value = base_timeout * 2 ** (attempt - 1)  # exponential backoff
            try:
                response = requests.request(
                    "POST", url, headers=headers, data=payload, timeout=timeout_value
                )
                return response
            except requests.exceptions.Timeout as e:
                print(f"Request timed out on attempt {attempt} ({timeout_value}s): {e}")
            except requests.exceptions.RequestException as e:
                raise e

        # Raise an exception after all retries are exhausted
        raise requests.exceptions.RequestException("Request failed after all retries")

          
