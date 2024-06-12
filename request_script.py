import requests
import time

# Конфигурация
SOURCE_URL = '###'
LOGIN_URL = '###'
LOGIN_DATA = {
    'username': '###',
    'password': '###'
}
FORWARDING_URL = '###'
CHECK_INTERVAL = 1  # Интервал проверки в секундах

# Функция для получения номеров с исходного сайта
def get_numbers(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        numbers = response.text.strip().split('\n')
        return numbers
    except requests.RequestException as e:
        print(f"Error fetching numbers: {e}")
        return []

# Функция для обновления переадресации
def update_call_forwarding(login_url, login_data, forwarding_url, phone_number):
    session = requests.Session()
    try:
        # Авторизация
        login_response = session.post(login_url, data=login_data)
        login_response.raise_for_status()
        
        # Перенос номера
        forwarding_data = {
            'phone_number': phone_number,
            'action': 'save'
        }
        forward_response = session.post(forwarding_url, data=forwarding_data)
        forward_response.raise_for_status()
        
        print(f"Successfully updated call forwarding to {phone_number}")
    except requests.RequestException as e:
        print(f"Error updating call forwarding: {e}")

# Основной цикл для периодической проверки и обновления
def main():
    last_number = None
    
    while True:
        numbers = get_numbers(SOURCE_URL)
        
        if numbers:
            current_number = numbers[-1]
            if current_number != last_number:
                update_call_forwarding(LOGIN_URL, LOGIN_DATA, FORWARDING_URL, current_number)
                last_number = current_number
        
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
