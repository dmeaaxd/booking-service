-- Вставка тестовых пользователей
INSERT INTO users (email, hashed_password) VALUES
('user1@example.com', '$2b$12$rG9QlZ8k7hT4vX2wY6pZ1u'),
('user2@example.com', '$2b$12$sH8Mk9jL6n5vC4xW3yZ2bq'),
('user3@example.com', '$2b$12$tI9Nl0kM8j7hU6vW5xY4z3'),
('admin@hotel.com', '$2b$12$uJ0Ol9kN8l7iH6gF5dS4r2'),
('guest@test.com', '$2b$12$vK1Pm0lN9k8jH7gF6eS5t3');

-- Вставка тестовых отелей
INSERT INTO hotels (name, stars, location, services, rooms_quantity, image_id) VALUES
('Grand Plaza Hotel', 5, 'Москва, ул. Тверская, 1', '{"wifi": true, "parking": true, "pool": true, "spa": true, "restaurant": true, "breakfast": true}', 150, 101),
('Cosmos Comfort', 4, 'Санкт-Петербург, Невский пр., 25', '{"wifi": true, "parking": true, "pool": false, "spa": false, "restaurant": true, "breakfast": true}', 80, 102),
('Skyline Resort', 3, 'Сочи, ул. Курортная, 15', '{"wifi": true, "parking": false, "pool": true, "spa": false, "restaurant": false, "breakfast": true}', 50, 103),
('Business Class', 4, 'Казань, ул. Баумана, 10', '{"wifi": true, "parking": true, "pool": false, "spa": false, "restaurant": true, "breakfast": false}', 60, 104),
('Eco Lodge', 2, 'Калининград, ул. Лесная, 5', '{"wifi": false, "parking": true, "pool": false, "spa": false, "restaurant": false, "breakfast": true}', 30, 105);

-- Вставка тестовых номеров для отеля 1
INSERT INTO rooms (hotel_id, name, description, price, services, quantity, image_id) VALUES
(1, 'Люкс с видом на город', 'Просторный номер с панорамным видом на город, king-size кроватью и гостиной зоной', 8500, '{"tv": true, "ac": true, "minibar": true, "safe": true, "hairdryer": true}', 20, 201),
(1, 'Стандарт двухместный', 'Комфортный номер с двумя односпальными кроватями и современной мебелью', 4500, '{"tv": true, "ac": true, "minibar": false, "safe": true, "hairdryer": true}', 40, 202),
(1, 'Семейный номер', 'Просторный номер для семьи с двумя спальнями и детской зоной', 12000, '{"tv": true, "ac": true, "minibar": true, "safe": true, "hairdryer": true, "crib": true}', 15, 203);

-- Вставка тестовых номеров для отеля 2
INSERT INTO rooms (hotel_id, name, description, price, services, quantity, image_id) VALUES
(2, 'Бизнес-класс', 'Номер для деловых поездок с рабочим столом и хорошим освещением', 6000, '{"tv": true, "ac": true, "minibar": true, "safe": true, "hairdryer": true, "desk": true}', 25, 204),
(2, 'Эконом', 'Компактный номер со всеми необходимыми удобствами', 3500, '{"tv": true, "ac": true, "minibar": false, "safe": false, "hairdryer": true}', 35, 205),
(2, 'Улучшенный двухместный', 'Просторный номер с большой кроватью и зоной для отдыха', 5000, '{"tv": true, "ac": true, "minibar": true, "safe": true, "hairdryer": true}', 20, 206);

-- Вставка тестовых номеров для отеля 3
INSERT INTO rooms (hotel_id, name, description, price, services, quantity, image_id) VALUES
(3, 'Стандарт с видом на море', 'Номер с балконом и видом на Черное море', 5500, '{"tv": true, "ac": true, "minibar": false, "safe": true, "hairdryer": true, "balcony": true}', 30, 207),
(3, 'Семейный сьют', 'Просторный номер для семьи с кухней и гостиной', 9000, '{"tv": true, "ac": true, "minibar": true, "safe": true, "hairdryer": true, "kitchen": true}', 10, 208),
(3, 'Эконом плюс', 'Улучшенный эконом-класс с современным ремонтом', 4000, '{"tv": true, "ac": true, "minibar": false, "safe": false, "hairdryer": true}', 10, 209);

-- Вставка тестовых бронирований
INSERT INTO bookings (room_id, user_id, date_from, date_to, price) VALUES
(1, 1, '2024-01-15', '2024-01-20', 8500),
(2, 2, '2024-02-01', '2024-02-05', 4500),
(3, 3, '2024-03-10', '2024-03-15', 12000),
(4, 1, '2024-04-20', '2024-04-25', 6000),
(5, 4, '2024-05-05', '2024-05-10', 3500),
(6, 5, '2024-06-15', '2024-06-20', 5000),
(7, 2, '2024-07-01', '2024-07-07', 5500),
(8, 3, '2024-08-10', '2024-08-15', 9000),
(9, 4, '2024-09-20', '2024-09-25', 4000),
(1, 5, '2024-10-05', '2024-10-10', 8500);

-- Проверка вставленных данных
SELECT 'Users count: ' || COUNT(*) FROM users
UNION ALL
SELECT 'Hotels count: ' || COUNT(*) FROM hotels
UNION ALL
SELECT 'Rooms count: ' || COUNT(*) FROM rooms
UNION ALL
SELECT 'Bookings count: ' || COUNT(*) FROM bookings;
