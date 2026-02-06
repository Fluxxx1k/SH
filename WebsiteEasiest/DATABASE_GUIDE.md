# Secret Hitler - Database Implementation Guide

## Обзор

Реализована полная система управления данными на основе SQLAlchemy, которая заменяет старое JSON-хранилище. Система обеспечивает:

- ✅ Типобезопасность через SQLAlchemy ORM
- ✅ Транзакции и ACID гарантии
- ✅ Миграции и версионирование схемы
- ✅ Поддержка PostgreSQL и SQLite
- ✅ Обратную совместимость с существующим кодом

## Архитектура

### Структура модулей

```
WebsiteEasiest/
├── data/
│   ├── database/
│   │   ├── __init__.py           # Инициализация БД, session manager
│   │   ├── models.py             # SQLAlchemy модели
│   │   ├── repositories.py       # Data Access Objects (DAO)
│   │   ├── player_operations.py  # Операции с игроками
│   │   ├── game_operations.py    # Операции с играми
│   │   ├── adapter.py            # Адаптер для совместимости
│   │   └── migrations.py         # Миграции БД
│   └── database_py/              # Старые функции (будут убраны)
```

### Слои архитектуры

```
┌─────────────────────────────────────────┐
│         Flask Routes (app2.py)          │ <- Представление
├─────────────────────────────────────────┤
│  Operations (player_ops, game_ops)      │ <- Бизнес-логика
├─────────────────────────────────────────┤
│  Repositories (PlayerRepo, GameRepo)    │ <- Data Access Objects
├─────────────────────────────────────────┤
│         SQLAlchemy Models               │ <- Schema/Модели
├─────────────────────────────────────────┤
│      Database (PostgreSQL/SQLite)       │ <- Хранилище
└─────────────────────────────────────────┘
```

## Настройка и инициализация

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

Новые зависимости:
- `SQLAlchemy>=2.0.0` - ORM
- `psycopg2-binary>=2.9.0` - драйвер PostgreSQL (опционально)
- `alembic>=1.12.0` - миграции (планируется)
- `python-dotenv>=1.0.0` - конфигурация

### 2. Конфигурация БД

#### Вариант А: SQLite (для разработки)

Создайте файл `.env`:
```env
DATABASE_URL=
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
```

Если `DATABASE_URL` пуст или не указан, система автоматически использует SQLite:
```
sqlite:///WebsiteEasiest/data/app.db
```

#### Вариант Б: PostgreSQL (для production)

Установите PostgreSQL и создайте БД:
```bash
createdb sh_game
```

Обновите `.env`:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/sh_game
FLASK_ENV=production
```

### 3. Инициализация БД

```python
# В Python скрипте или интерпретаторе
from WebsiteEasiest.data.database.migrations import migrate_init_db
migrate_init_db()

# Или через Flask shell
flask shell
>>> from WebsiteEasiest.data.database.migrations import migrate_init_db
>>> migrate_init_db()
```

## API Документация

### Player Operations

#### Создание игрока
```python
from WebsiteEasiest.data.database.player_operations import create_player_db

success, error = create_player_db("player_name", "password123")
if success:
    print("Игрок создан")
else:
    print(f"Ошибка: {error}")
```

#### Получение данных игрока
```python
from WebsiteEasiest.data.database.player_operations import get_data_of_player_db

success, player_data = get_data_of_player_db("player_name")
if success:
    print(f"Username: {player_data['player_name']}")
    print(f"Игр сыграно: {player_data['games_played']}")
    print(f"Побед: {player_data['games_won']}")
```

#### Аутентификация
```python
from WebsiteEasiest.data.database.player_operations import login_player_db

success, error = login_player_db("player_name", "password")
if success:
    print("Вход выполнен успешно")
else:
    print(f"Ошибка: {error}")
```

#### Проверка существования
```python
from WebsiteEasiest.data.database.player_operations import exists_player_db

if exists_player_db("player_name"):
    print("Игрок существует")
```

#### Подсчёт игроков
```python
from WebsiteEasiest.data.database.player_operations import count_players_db

total = count_players_db()
print(f"Всего игроков: {total}")
```

### Game Operations

#### Создание игры
```python
from WebsiteEasiest.data.database.game_operations import create_game_db

success, error = create_game_db(
    "game_name",
    "creator_username",
    password="secret123",
    data={
        'max_players': 5,
        'red_win_num': 5,
        'black_win_num': 6
    }
)
if success:
    print("Игра создана")
else:
    print(f"Ошибка: {error}")
```

#### Получение данных игры
```python
from WebsiteEasiest.data.database.game_operations import get_data_of_game_db

success, game_data = get_data_of_game_db("game_name")
if success:
    print(f"Статус: {game_data['status']}")
    print(f"Игроки: {game_data['players']}")
    print(f"Создана: {game_data['created_by']}")
```

#### Получение логов игры
```python
from WebsiteEasiest.data.database.game_operations import get_logs_of_game_db

success, logs = get_logs_of_game_db("game_name")
if success:
    for log in logs:
        print(f"[{log['timestamp']}] {log['log_type']}: {log['message']}")
```

#### Сохранение состояния игры
```python
from WebsiteEasiest.data.database.game_operations import save_data_of_game_db

game_state = {
    'current_state': {
        'deck': ['R', 'B', 'R', ...],
        'round': 1,
        'president': 0
    },
    'settings': {
        'max_players': 5
    }
}

if save_data_of_game_db("game_name", game_state):
    print("Состояние сохранено")
```

#### Завершение игры
```python
from WebsiteEasiest.data.database.game_operations import end_game_db

success, error = end_game_db(
    "game_name",
    game_data={
        'result': {
            'winning_side': 'red',
            'winner_name': 'liberal_victory',
            'details': {'duration': 30, 'rounds': 5}
        }
    },
    delete=False  # False = mark as finished, True = delete
)
```

#### Логирование событий игры
```python
from WebsiteEasiest.data.database.game_operations import log_game_event_db

success, error = log_game_event_db(
    "game_name",
    "vote",
    message="Player X voted YES",
    player_name="player_x",
    data={'vote': 'yes', 'target': 'player_y'}
)
```

### Использование Repositories напрямую

Для более сложных операций используйте репозитории:

```python
from WebsiteEasiest.data.database import get_session
from WebsiteEasiest.data.database.repositories import PlayerRepository, GameRepository

session = get_session()

# Найти игрока
player = PlayerRepository.get_by_username(session, "player_name")

# Найти игру
game = GameRepository.get_by_name(session, "game_name")

# Добавить игрока в игру
GameRepository.add_player(session, game.id, player.id)

# Обновить статус игры
from WebsiteEasiest.data.database.models import GameStatus
GameRepository.update_status(session, game.id, GameStatus.PLAYING)

session.close()
```

## Модели БД

### Player
```
- id: Integer (PK)
- username: String (UNIQUE, INDEX)
- password_hash: String
- email: String (UNIQUE)
- created_at: DateTime
- last_login: DateTime
- is_active: Boolean
- games_played: Integer
- games_won: Integer
- Relationships:
  - games: List[Game] (many-to-many)
  - created_games: List[Game] (creator)
  - game_players: List[GamePlayer]
```

### Game
```
- id: Integer (PK)
- name: String (UNIQUE, INDEX)
- status: Enum(created, waiting_for_start, playing, finished)
- created_by_id: Integer (FK)
- password: String (hashed)
- created_at: DateTime
- started_at: DateTime
- finished_at: DateTime
- settings: JSON (max_players, red_win_num, etc.)
- current_state: JSON (deck, roles, votes, etc.)
- Relationships:
  - creator: Player
  - players: List[Player] (many-to-many)
  - game_players: List[GamePlayer]
  - logs: List[GameLog]
  - result: GameResult
```

### GamePlayer
```
- id: Integer (PK)
- game_id: Integer (FK, INDEX)
- player_id: Integer (FK)
- role: String (hitler, communist, liberal, etc.)
- is_alive: Boolean
- is_president: Boolean
- is_chancellor: Boolean
- joined_at: DateTime
- left_at: DateTime
- votes: JSON
- actions: JSON
- Relationships:
  - game: Game
  - player: Player
```

### GameLog
```
- id: Integer (PK)
- game_id: Integer (FK, INDEX)
- log_type: String (INDEX) (action, vote, result, state_change)
- player_id: Integer (FK)
- data: JSON
- message: Text
- timestamp: DateTime (INDEX)
- Relationships:
  - game: Game
```

### GameResult
```
- id: Integer (PK)
- game_id: Integer (FK, UNIQUE)
- winning_side: String (red, black)
- winner_name: String (hitler, stalin, liberal_victory)
- finished_at: DateTime
- duration_seconds: Integer
- details: JSON
- Relationships:
  - game: Game
```

### IPLog
```
- id: Integer (PK)
- player_id: Integer (FK, INDEX)
- ip_address: String
- timestamp: DateTime (INDEX)
- is_creation: Boolean
- Relationships:
  - player: Player
```

## Миграция с JSON на БД

### Этап 1: Параллельная работа
- Новый код использует БД через adapter.py
- Старый JSON код отключен, но в папке остается
- Тестирование совместимости

### Этап 2: Миграция данных (будет реализовано)
```python
# Скрипт миграции из JSON в БД
from WebsiteEasiest.data.database_py import games, players
from WebsiteEasiest.data.database import get_session
from WebsiteEasiest.data.database.repositories import PlayerRepository

# 1. Прочитать старые JSON файлы
# 2. Создать записи в БД
# 3. Проверить целостность
# 4. Удалить JSON файлы
```

### Этап 3: Полная очистка
- Удалить database_py
- Удалить JSON файлы из data/games, data/players
- Оставить только БД

## Тестирование

### Проверка инициализации БД
```python
from WebsiteEasiest.data.database import get_session
from WebsiteEasiest.data.database.models import Player, Game

session = get_session()
print(f"Players count: {session.query(Player).count()}")
print(f"Games count: {session.query(Game).count()}")
session.close()
```

### Создание тестовых данных
```python
from WebsiteEasiest.data.database.player_operations import create_player_db
from WebsiteEasiest.data.database.game_operations import create_game_db

# Создать игрока
success, error = create_player_db("testuser", "password123")
assert success, f"Failed to create player: {error}"

# Создать игру
success, error = create_game_db("testgame", "testuser")
assert success, f"Failed to create game: {error}"

print("All tests passed!")
```

## Возможные проблемы и решения

### Проблема: "Database not initialized"
**Решение:**
```python
from WebsiteEasiest.data.database.migrations import migrate_init_db
migrate_init_db()
```

### Проблема: PostgreSQL не подключается
**Решение:**
```bash
# Убедитесь, что PostgreSQL запущен
psql -U postgres -c "CREATE DATABASE sh_game"

# Обновите .env с правильными учетными данными
DATABASE_URL=postgresql://user:password@localhost:5432/sh_game
```

### Проблема: Миграция с JSON на БД
**Решение:** Используйте миграционный скрипт (будет реализован в следующей версии)

## Безопасность

### Хеширование паролей
Пароли автоматически хешируются с помощью `werkzeug.security.generate_password_hash`:
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Создание
hash = generate_password_hash("password")  # Автоматически в create_player

# Проверка
if check_password_hash(hash, "password"):
    # Пароль верен
```

### SQL Injection
SQLAlchemy ORM защищает от SQL injection через параметризованные запросы:
```python
# БЕЗОПАСНО: параметр передается отдельно
player = PlayerRepository.get_by_username(session, user_input)

# НЕБЕЗОПАСНО (не используется):
# session.execute(f"SELECT * FROM player WHERE username = '{user_input}'")
```

### IP Логирование
IP адреса логируются при регистрации и входе для безопасности:
```python
from WebsiteEasiest.data.database.models import IPLog

# Видеть все IP для игрока
session.query(IPLog).filter(IPLog.player_id == player_id).all()
```

## Производительность

### Индексы
- `Player.username` - быстрый поиск по имени
- `Game.name` - быстрый поиск по названию игры
- `Game.status` - быстрая фильтрация по статусу
- `GameLog.game_id`, `GameLog.timestamp` - быстрые логи
- `IPLog.player_id`, `IPLog.timestamp` - быстрые логи IP

### Оптимизация запросов
```python
# ПЛОХО: N+1 проблема
for game in GameRepository.get_active_games(session):
    print(len(game.players))  # Отдельный запрос для каждой игры!

# ХОРОШО: Eager loading
from sqlalchemy.orm import joinedload
session.query(Game).options(joinedload(Game.players)).filter(...)
```

## Что дальше

1. **Alembic миграции** - версионирование БД схемы
2. **Кэширование** - Redis для hot data
3. **Асинхронность** - async SQLAlchemy (для WebSocket)
4. **API** - REST API вместо Flask шаблонов
5. **Tests** - Unit и integration тесты

## Контакты и вопросы

Для вопросов и предложений смотрите документацию SQLAlchemy:
- https://docs.sqlalchemy.org/
- https://docs.sqlalchemy.org/en/20/orm/

---

**Версия:** 1.0  
**Дата:** 2026-02-06

