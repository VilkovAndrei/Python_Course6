# Курсовая 6. Основы веб-разработки на Django 

Веб-приложение сервиса управления рассылками, администрирования и получения статистики попыток рассылок.


<!-- USAGE EXAMPLES -->
## Подготовка к использованию проекта

Перед запуском web-приложения создайте базу данных, создайте и примените миграции, установите необходимые пакеты из файла requirements.txt и заполните файл .env по образцу env.sample. Используйте команду "python manage.py csu" для создания суперпользователя. Для запуска используйте команду "python manage.py runserver". Для запуска рассылок "python manage.py start_mailing".
Фикстуры для заполнения базы данных находятся в файле data.json      
### Фикстуры
Фикстуры для заполнения базы данных находятся в файле data.json

### Пользователи:
Админ (superuser) - admin@test.com

Обычный пользователь - user@test.com, user2@test.com

Менеджер пользователей сервиса - manager@test.com входит в группу mailing_manager

Менеджер блога - content_manager@test.com входит в группу blog_manager

Пароль для пользователей (кроме Админа): 'for2est2'

## Структура проекта

config/

    settings.py - настройки приложений
    urls.py - файл маршрутизации

blog/

    templates/blog - html шаблоны для приложения blog
    admin.py - настройки админки
    forms.py - настройки форм
    models.py - модели приложения
    urls.py - файл маршрутизации приложения
    views.py - контроллеры

main/

    management/commands
        start_mailing - кастомная команда начала рассылки
    static - директория с файлами для стилистического оформления сайта
    templates/main - html шаблоны для приложения main
    templatetags/
        my_tags - кастомные тэги
    admin.py - настройки админки
    forms.py - настройки форм
    models.py - модели приложения
    services.py - сервисные функции
    urls.py - файл маршрутизации приложения
    views.py - контроллеры

media/ - директория хранения загружаемых файлов с изображениями

static/ - директория с файлами для стилистического оформления сайта

users/

    management/commands
        csu - кастомная команда создания суперпользователя
    template/users - html шаблоны для приложения users
    admin.py - настройки админки
    forms.py - настройки форм
    models.py - модели приложения
    urls.py - файл маршрутизации приложения
    views.py - контроллеры

manage.py - точка входа веб-приложения.

requirements.txt - список зависимостей для проекта.

env.sample - пример заполнения переменных окружения.
