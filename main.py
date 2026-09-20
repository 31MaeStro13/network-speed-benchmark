import requests
import functools
import time
import sys



def measure_time(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        return result, duration
    return wrapper




@measure_time
def download_payload(url: str, chunk_size: int = 64 * 1024) -> int:
    
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
        "Cache-Control": "no-cache, no-store, must-revalidate",
        "Pragma": "no-cache",
    }

    sep = "&" if "?" in url else "?"
    busted_url = f"{url}{sep}_cb={time.time_ns()}"

    response = requests.get(
        busted_url, 
        headers=headers, 
        timeout=(5.0, 30.0), 
        stream=True
    )

    response.raise_for_status()
    
    content_type = response.headers.get("Content-Type", "")
    if "text/html" in content_type:
        raise ValueError(f"Сервер вернул HTML-страницу вместо файла/картинки ({content_type})")
    
    total_bytes = 0
    for chunk in response.iter_content(chunk_size=chunk_size):
        if chunk:  # фильтруем keep-alive чанки
            total_bytes += len(chunk)
    
    return total_bytes


def main():

    if len(sys.argv) < 2:
        print("Использование: python main.py <URL>")
        sys.exit(1)
    image_url = sys.argv[1]
    
    if not image_url.startswith(("http://", "https://")):
        print("[!] Ошибка: URL должен начинаться с http:// или https://", file=sys.stderr)
        sys.exit(1)

    total_bytes = 0
    total_time = 0
    successful_requests = 0

    for i in range(1, 11):
        try:
            bytes_count, duration = download_payload(image_url)

            total_bytes += bytes_count
            total_time += duration
            successful_requests += 1

            mb = bytes_count / (1024 * 1024)

            speed = mb / duration if duration > 0 else 0.0

            print(f"Запрос {i}: {duration:.2f} сек | Скорость: {speed:.2f} МБ/с")
        
        except requests.exceptions.Timeout:
            print(f"Запрос {i:02d}: [ОШИБКА] Таймаут соединения (>10 сек)")
        except requests.exceptions.RequestException as err:
            print(f"Запрос {i:02d}: [ОШИБКА] Сетевой сбой: {err}")
        except ValueError as err:
            print(f"[ОШИБКА ВАЛИДАЦИИ] {err}")
            sys.exit(1)

    if successful_requests > 0:
        total_mb = total_bytes / (1024 * 1024)
        avg_time = total_time / successful_requests
        avg_speed = total_mb / total_time
        print("\n" + "=" * 40)
        print(f"Успешных запросов:     {successful_requests}/10")
        print(f"Общий объем данных:    {total_mb:.2f} МБ")
        print(f"Среднее время запроса: {avg_time:.2f} сек")
        print(f"Средняя скорость:      {avg_speed:.2f} МБ/с")
        print("=" * 40)
    else:
        print("\n[!] Все запросы завершились ошибкой.")

if __name__ == "__main__":
    main()
