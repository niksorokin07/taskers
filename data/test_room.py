from requests import get, post, delete

print(get('http://localhost:5000/api/v2/rooms/1').json())

print(get('http://localhost:5000/api/v2/rooms/15').json())  # несуществующий id

print(get('http://localhost:5000/api/v2/rooms/q').json())  # id не инт

print(get('http://localhost:5000/api/v2/rooms').json())
print(delete("http://localhost:5000/api/v2/rooms/2").json())  # удаление

print(post("http://localhost:5000/api/v2/rooms",  # верный запрос
           json={'team_leader': 1,
                 'title': 'Заголовок',
                 'about': '1',
                 'collaborators': '1, 2'}).json())

print(get('http://localhost:5000/api/v2/rooms').json())  # id добавился

print(post("http://localhost:5000/api/v2/rooms",
           json={"title": "Фамилия"}).json())  # недостаточно данных

print(post("http://localhost:5000/api/v2/rooms",  # неправильный запрос(не те аргументы)
           json={"surname": "Фамилия", "name": "name",
                 "age": 2, "position": "position", "speciality": "speciality",
                 "address": "address", "email": "email25@email",
                 "password": "Qazqwer25"}).json())

print(delete('http://localhost:5000/api/v2/rooms/q').json())  # не int
print(delete('http://localhost:5000/api/v2/rooms/100').json())  # удаление не существующего