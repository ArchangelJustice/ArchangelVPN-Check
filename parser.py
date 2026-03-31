import requests
import base64
import re
from datetime import datetime

# Источники бесплатных конфигураций
SOURCES = [
    "https://raw.githubusercontent.com/freev2ray/v2ray-free/master/v2ray",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_configs.txt",
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/vless",
    "https://raw.githubusercontent.com/soroushmirzaei/telegram-configs-collector/main/protocols/vless"
]

def fetch_configs():
    all_nodes = []
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Сбор узлов запущен...")
    
    for url in SOURCES:
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                raw_data = resp.text
                # Попытка декодирования, если данные в Base64
                if not raw_data.startswith(("vless://", "vmess://", "ss://", "trojan://")):
                    try:
                        raw_data = base64.b64decode(raw_data).decode('utf-8')
                    except: pass
                
                # Регулярка для поиска ссылок протоколов
                found = re.findall(r'(vless|vmess|ss|trojan)://[^\s]+', raw_data)
                all_nodes.extend(found)
        except Exception as e:
            print(f"[-] Ошибка при чтении {url}: {e}")

    return list(set(all_nodes)) # Удаляем дубликаты

if __name__ == "__main__":
    nodes = fetch_configs()
    
    # Сохраняем файл подписки (raw текст)
    with open("sub.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(nodes))
    
    # Создаем интерактивную HTML страницу
    update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    html_template = f"""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>ArchangelVPN Status</title>
        <style>
            body {{ background: #0a0a0a; color: #00ff41; font-family: 'Courier New', monospace; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
            .container {{ border: 2px solid #00ff41; padding: 20px; box-shadow: 0 0 15px #00ff41; text-align: center; }}
            h1 {{ text-transform: uppercase; letter-spacing: 5px; }}
            .status {{ color: white; background: #00ff4122; padding: 10px; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Archangel Justice VPN</h1>
            <div class="status">СТАТУС: ACTIVE</div>
            <p>Найдено узлов: <b>{len(nodes)}</b></p>
            <p>Последнее обновление: {update_time} UTC</p>
            <p style="font-size: 0.8em; color: #666;">Powered by GitHub Actions</p>
        </div>
    </body>
    </html>
    """
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)
        
    print(f"[+] Готово! Собрано {len(nodes)} уникальных ключей.")
