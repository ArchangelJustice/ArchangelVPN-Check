import requests
import re
import base64

# Топовые источники, которые отдают тысячи ключей
SOURCES = [
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mixed",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_configs.txt",
    "https://raw.githubusercontent.com/WilliamStar007/Proxy-List/main/v2ray.txt",
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config",
    "https://raw.githubusercontent.com/aiboboxx/v2rayfree/main/v2ray",
    "https://raw.githubusercontent.com/LonUp/NodeList/main/NodeList.txt"
]

def fetch():
    final_nodes = []
    # Обманываем защиту сайтов, притворяясь браузером
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
    
    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=20)
            if r.status_code == 200:
                text = r.text
                # Если это Base64 каша - чистим
                if "://" not in text[:50]:
                    try:
                        text = base64.b64decode(text.strip()).decode('utf-8')
                    except: pass
                
                # Собираем всё: VLESS, VMess, SS, Trojan
                found = re.findall(r'(vless|vmess|ss|trojan)://[^\s|<>"]+', text)
                final_nodes.extend(found)
                print(f"[+] {url[:30]}... вытянуто: {len(found)}")
        except: continue
    return list(set(final_nodes))

if __name__ == "__main__":
    nodes = fetch()
    with open("sub.txt", "w", encoding="utf-8") as f:
        if nodes:
            f.write("\n".join(nodes))
            print(f"--- УСПЕХ: СОБРАНО {len(nodes)} УЗЛОВ ---")
        else:
            # Если совсем голяк, пишем рабочий резервный узел
            f.write("ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo0MzIxQDEyNy4wLjAuMTo4MDgw#Archangel_Reloader")
            print("--- Ключи не найдены, записан резерв ---")
