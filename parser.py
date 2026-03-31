import requests
import re
import base64

# Увеличили список источников и добавили больше протоколов
SOURCES = [
    "https://raw.githubusercontent.com/freev2ray/v2ray-free/master/v2ray",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_configs.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config",
    "https://raw.githubusercontent.com/WilliamStar007/Proxy-List/main/v2ray.txt"
]

def fetch():
    nodes = []
    for url in SOURCES:
        try:
            r = requests.get(url, timeout=15)
            if r.status_code == 200:
                text = r.text
                # Пробуем декодировать из Base64, если это каша
                if "://" not in text:
                    try:
                        text = base64.b64decode(text).decode('utf-8')
                    except: pass
                
                # Ищем ключи регуляркой
                found = re.findall(r'(vless|vmess|ss|trojan|ssr)://[^\s|<>"]+', text)
                nodes.extend(found)
                print(f"[+] С {url} собрано: {len(found)}")
        except: continue
    return list(set(nodes))

if __name__ == "__main__":
    configs = fetch()
    if configs:
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(configs))
        print(f"[SUCCESS] Записано {len(configs)} ключей в sub.txt")
    else:
        # Если ничего не нашли, запишем хотя бы один тестовый, чтобы файл не был 0 байт
        with open("sub.txt", "w") as f:
            f.write("ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo0MzIxQDEyNy4wLjAuMTo4MDgw#EmptyNodesTryAgainLater")
        print("[!] Ключи не найдены, записан заглушка")
