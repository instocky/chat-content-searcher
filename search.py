import json
import re
from datetime import datetime

def load_json_file(file_path):
    """Загрузка JSON файла"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

def extract_sentence(text, keyword):
    """Извлечение строки, содержащей ключевое слово"""
    if not text:
        return ""
    
    # Разбиваем текст на строки
    lines = text.split('\n')
    
    # Ищем строку с ключевым словом (регистронезависимо)
    for line in lines:
        line = line.strip()
        if keyword.lower() in line.lower() and line:
            # Ограничиваем длину строки если она слишком длинная
            if len(line) > 150:  # можно настроить максимальную длину
                # Находим позицию ключевого слова
                pos = line.lower().find(keyword.lower())
                # Берем часть строки вокруг ключевого слова
                start = max(0, pos - 70)  # 70 символов до
                end = min(len(line), pos + len(keyword) + 70)  # 70 символов после
                line = ('...' if start > 0 else '') + \
                       line[start:end] + \
                       ('...' if end < len(line) else '')
            return line
            
    return ""

def format_datetime(dt_string):
    """Форматирование даты и времени"""
    try:
        dt = datetime.fromisoformat(dt_string.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%dT%H:%M:%S')
    except:
        return dt_string

def search_in_json(data, search_key):
    """Поиск по JSON и форматированный вывод результатов"""
    if len(search_key) < 3:
        print("Ошибка: ключ поиска должен содержать минимум 3 символа")
        return
    
    matches = []
    
    # Поиск совпадений
    for chat in data:
        for message in chat.get('chat_messages', []):
            text = message.get('text', '')
            if search_key.lower() in text.lower():
                sentence = extract_sentence(text, search_key)
                if sentence:  # Добавляем только если нашли предложение
                    matches.append({
                        'name': chat.get('name', 'Без названия'),
                        'created_at': format_datetime(chat.get('created_at', '')),
                        'updated_at': format_datetime(chat.get('updated_at', '')),
                        'context': sentence
                    })
    
    # Вывод результатов
    print(f'\nПоиск по ключу: "{search_key}"')
    print(f'Найдено совпадений: {len(matches)}\n')
    
    for idx, match in enumerate(matches, 1):
        print(f'[{idx}]')
        print(f'Чат: {match["name"]}')
        print(f'Создан: {match["created_at"]}')
        print(f'Обновлен: {match["updated_at"]}')
        print(f'Контекст: "{match["context"]}"')
        print('---------------\n')

def main():
    """Основная функция"""
    # Путь к файлу JSON
    # file_path = 'data-2024-10-13-17-39-29.json'
    # file_path = 'data.json'
    file_path = 'conversations.json'
    
    # Загрузка данных
    data = load_json_file(file_path)
    if not data:
        return
    
    # Ввод ключа поиска
    search_key = input("Введите ключ для поиска (минимум 3 символа): ").strip()
    
    # Поиск и вывод результатов
    search_in_json(data, search_key)

if __name__ == "__main__":
    main()