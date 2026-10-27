# UAP News & Blog Portal

Three apps:
- accounts   : Department, Profile
- content    : Category, Tag, Post, Comment, Bookmark
- moderation : ReviewLog, Report, Notification

Run:
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py createsuperuser
    python manage.py runserver
