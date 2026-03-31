import requests
import re
import base64

# Топовые агрегаторы, каждый из которых содержит СОТНИ свежих ключей
SOURCES = [
    # Агрегатор 1: Сборная солянка (Mixed)
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/mixed",
    # Агрегатор 2: Огромная база VLESS
    "https://raw.githubusercontent.com/yebekhe/TelegramV2rayCollector/main/sub/base64/vless",
    # Агрегатор 3: База малых прокси-листов
    "https://raw.githubusercontent.com/WilliamStar007/Proxy-List/main/v2ray.txt",
    # Агрегатор 4: Постоянно обновляемый репозиторий
    "https://raw.githubusercontent.com/vfarid/v2ray-share/main/all_configs.txt",
    # Агрегатор 5: Дополнительный резерв
    "https://raw.githubusercontent.com/tbbatbb/Proxy/master/dist/v2ray.config"
]

def fetch_and_extract():
    final_nodes = []
    print("[*] Начинаю тотальную зачистку источников...")

    for url in SOURCES:
        try:
            r = requests.get(url, timeout=20)
            if r.status_code == 200:
                content = r.text
                
                # Если контент в Base64 (агрегаторы это любят), декодируем
                if not content.startswith(("vless://", "vmess://", "ss://", "trojan://")):
                    try:
                        # Убираем лишние пробелы и перекодируем
                        content = base64.b64decode(content.strip()).decode('utf-8')
                    except:
                        pass # Значит, там просто текст или частичный base64
                
                # Регулярка для вытягивания ВСЕХ типов ключей
                found = re.findall(r'(vless|vmess|ss|trojan|ssr)://[^\s|<>"]+', content)
                final_nodes.extend(found)
                print(f"[+] С {url[:40]}... вытянуто {len(found)} ключей")
        except Exception as e:
            print(f"[!] Пропуск {url[:40]}: {e}")

    # Чистим дубликаты (сет)
    unique_nodes = list(set(final_nodes))
    return unique_nodes

if __name__ == "__main__":
    nodes = fetch_and_extract()
    
    if len(nodes) > 0:
        # Сохраняем результат
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(nodes))
        print(f"\n[SUCCESS] Миссия выполнена! Собрано уникальных ключей: {len(nodes)}")
    else:
        # Если вдруг пусто — пишем лог-заглушку
        with open("sub.txt", "w") as f:
            f.write("ss://Y2hhY2hhMjAtaWV0Zi1wb2x5MTMwNTo0MzIxQDEyNy4wLjAuMTo4MDgw#System_Empty_Check_Sources")
        print("[!] Внимание: Ключи не найдены. Проверь соединение.")
