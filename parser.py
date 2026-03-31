import requests
import re
import base64

# Ультимативный список агрегаторов (здесь тысячи ключей)
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mixed",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_configs.txt",
    "https://raw.githubusercontent.com/WilliamStar007/Proxy-List/main/v2ray.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config",
    "https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList.txt",
    "https://raw.githubusercontent.com/sarve_v2ray/V2ray_Configs/main/All_Configs_Sub.txt"
]

def fetch_all():
    nodes = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                text = r.text
                # Если данные в base64, пробуем декодировать
                if "://" not in text[:50]:
                    try:
                        text = base64.b64decode(text.strip()).decode('utf-8')
                    except: pass
                
                # Собираем все типы протоколов
                found = re.findall(r'(vless|vmess|ss|trojan)://[^\s|<>"]+', text)
                nodes.extend(found)
                print(f"[+] Собрано с {url[:30]}... : {len(found)}")
        except: continue
    return list(set(nodes)) # Удаляем дубликаты

if __name__ == "__main__":
    configs = fetch_all()
    with open("sub.txt", "w", encoding="utf-8") as f:
        if configs:
            f.write("\n".join(configs))
            print(f"--- УСПЕХ: ЗАПИСАНО {len(configs)} КЛЮЧЕЙ ---")
        else:
            # Если пусто, оставляем старый рабочий ключ
            f.write("ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo0MzIxQDEyNy4wLjAuMTo4MDgw#Archangel_System_Ready")

    # Создаем красивую HTML заглушку
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(f"<html><body style='background:#000;color:#0f0;font-family:monospace;'>")
        f.write(f"<h1>Archangel VPN Status</h1><p>Active Nodes: {len(configs)}</p>")
        f.write(f"</body></html>")
