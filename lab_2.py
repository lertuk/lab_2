import csv
from playwright.sync_api import sync_playwright

def scrape_laptops_edge():
    url = "https://webscraper.io/test-sites/e-commerce/ajax/computers/laptops"
    output_file = "laptops_data.csv"
    
    with sync_playwright() as p:
        # ГОЛОВНА ЗМІНА: Використовуємо вже встановлений у Windows Microsoft Edge
        # Це позбавляє необхідності робити playwright install
        browser = p.chromium.launch(channel="msedge", headless=True)
        page = browser.new_page()
        
        print(f"Відкриття сторінки: {url}")
        page.goto(url)
        
        # ОЧІКУВАННЯ: Чекаємо завантаження динамічних карток товарів
        print("Очікування відмальовки товарів через JavaScript/AJAX...")
        page.wait_for_selector(".product-wrapper", timeout=10000)
        
        # Знаходимо всі відрендерені картки товарів
        product_cards = page.locator(".product-wrapper").all()
        laptops = []
        
        for card in product_cards:
            title = card.locator("a.title").inner_text().strip()
            price = card.locator(".price").inner_text().strip()
            description = card.locator(".description").inner_text().strip()
            reviews = card.locator(".review-count").inner_text().strip()
            
            laptops.append({
                "Назва": title,
                "Ціна": price,
                "Опис": description,
                "Кількість відгуків": reviews
            })
            
        browser.close()
        
        # Збереження зібраних даних у файл CSV
        fieldnames = ["Назва", "Ціна", "Опис", "Кількість відгуків"]
        with open(output_file, mode="w", encoding="utf-8-sig", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=";")
            writer.writeheader()
            writer.writerows(laptops)
            
        print(f"Успішно зібрано записів: {len(laptops)}")
        print(f"Результат збережено у: {output_file}")

if __name__ == "__main__":
    scrape_laptops_edge()