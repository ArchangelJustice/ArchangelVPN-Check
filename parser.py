import requests
import re

# Прямые ссылки на зеркала с готовыми ключами (самые стабильные)
SOURCES = [
    "https://raw.githubusercontent.com/mansooridavood/v2ray-freeer/main/proxy.txt",
    "https://raw.githubusercontent.com/freev2ray/v2ray-free/master/v2ray",
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_configs.txt",
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt"
]

def start_harvest():
    all_nodes = []
    print("--- START MINING ---")
    
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

    for url in SOURCES:
        try:
            r = requests.get(url, headers=headers, timeout=15)
            if r.status_code == 200:
                # Ищем всё, что похоже на ключи
                found = re.findall(r'(vless|vmess|ss|trojan)://[^\s|<>"]+', r.text)
                all_nodes.extend(found)
                print(f"[+] {url[:30]}... found: {len(found)}")
        except Exception as e:
            print(f"[!] Error {url[:30]}: {e}")

    # Убираем дубли и мусор
    clean_nodes = list(set([n for n in all_nodes if len(n) > 20]))

    if clean_nodes:
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(clean_nodes))
        print(f"--- SUCCESS: {len(clean_nodes)} NODES SAVED ---")
    else:
        # Резервный рабочий ключ, если всё упало
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write("ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo0MzIxQDEyNy4wLjAuMTo4MDgw#Archangel_Emergency_Key")
        print("--- NO NODES FOUND, SAVED EMERGENCY KEY ---")

if __name__ == "__main__":
    start_harvest()
