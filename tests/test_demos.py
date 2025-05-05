import requests

BASE_URL = "http://localhost:8000"

def main():
    print("1. Регистрируем пользователя")
    register_response = requests.post(
        f"{BASE_URL}/register",
        json={"username": "demo_user", "password": "demo_pass"}
    )
    print(f"Статус регистрации: {register_response.status_code}")
    print(register_response.json())


    print("\n2. Получаем токен")
    token_response = requests.post(
        f"{BASE_URL}/token",
        data={"username": "demo_user", "password": "demo_pass"},  
        headers={"Content-Type": "application/x-www-form-urlencoded"}  
    )
    print("Ответ токена:", token_response.text)  
    token = token_response.json()["access_token"]
   
    print("\n3. Добавляем книги")
    books = [
        {"title": "1984", "author": "George Orwell"},
        {"title": "Dune", "author": "Frank Herbert"},
        {"title": "Brave New World", "author": "Aldous Huxley"}
    ]
    
    book_ids = []
    for book in books:
        response = requests.post(
            f"{BASE_URL}/books",
            json=book,
            headers={"Authorization": f"Bearer {token}"}
        )
        print("Status Code:", response.status_code)
        print("Response Text:", response.text)  
        response.raise_for_status()  
        book_id = response.json()["id"]
        book_ids.append(book_id)

    print("\n4. Создаем отзывы")
    reviews = [
        {"rating": 5, "comment": "Masterpiece!", "book_id": book_ids[0]},
        {"rating": 4, "comment": "Very good", "book_id": book_ids[0]},
        {"rating": 5, "comment": "Life changing", "book_id": book_ids[0]},
        {"rating": 3, "comment": "Overrated", "book_id": book_ids[1]},
        {"rating": 5, "comment": "Best sci-fi ever", "book_id": book_ids[2]}
    ]
    
    for review in reviews:
        try:
            response = requests.post(
                f"{BASE_URL}/reviews",
                json=review,
                headers={"Authorization": f"Bearer {token}"}
            )
            print(f"Отзыв: {response.status_code} - {response.text}")
            headers = {
                "Authorization": f"Bearer {token}", 
                "Content-Type": "application/json"
            }

            response = requests.post(
                f"{BASE_URL}/reviews",
                json=review,
                headers=headers
            )
        except Exception as e:
            print(f"Ошибка: {str(e)}")

    print("\n5. Запрашиваем рекомендации")
    recommendations = requests.get(f"{BASE_URL}/recommendations")
    print("Топ рекомендаций:")
    for idx, book in enumerate(recommendations.json()["recommendations"], 1):
        print(f"{idx}. {book['title']} by {book['author']}")

    print("\n6. Тест защиты эндпоинтов")
    bad_response = requests.post(
        f"{BASE_URL}/reviews",
        json={"rating": 1, "comment": "Hack attempt", "book_id": 1}
    )
    print(f"Попытка без авторизации: {bad_response.status_code}")

if __name__ == "__main__":
    main()

def test_demo_script_runs():
    main()