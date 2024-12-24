# Loyihaning nomi

Loyihaning nomi CountryAward yani davlat mukofotlari , loyihada davlat mukofotlari sayti uchun barcha api lar tuzulgan

## Texnologiyalar

- Python
- Django
- PostgreSQL
- Django Rest Framework

## O'rnatish

1. Repozitoriyani klonlash:

   ```bash
  git clone https://github.com/Rahmonqul/Award_Contry

2. Loyihaga o'ting:
  cd CountryAward
3. Virtual muhit yaratish va faollashtirish:
  python3 -m venv venv
  source venv/bin/activate  # Linux/Mac uchun
  venv\Scripts\activate     # Windows uchun
4. Kerakli kutubxonalarni o'rnatish:
   pip install -r requirements.txt
5. .env faylini yaratish va kerakli o'zgaruvchilarni (masalan, ma'lumotlar bazasi ulanishi) sozlash.
6. Ma'lumotlar bazasini migratsiya qilish:
   python manage.py migrate
7. Djangoni ishga tushirish:
   python manage.py runserver

## Deploy qilish

1. Heroku hisobini yaratish
2. Heroku ilovasini yaratish
   heroku create CountryAward
3.  Procfile yaratish 
      Heroku ilovasining ishga tushish jarayonini belgilash uchun, loyihangizning asosiy papkasida Procfile faylini yaratib, unga quyidagi satrni qo'shing:
         web: gunicorn CountryAward.wsgi
4. requirements.txt va runtime.txt fayllarini yaratish
      Heroku uchun kerakli fayllarni yaratish:
         requirements.txt faylini yaratish (agar mavjud bo'lmasa):  pip freeze > requirements.txt
         runtime.txt faylini yaratish va unga Python versiyasini qo'shish: python-3.x.x
5. Heroku'da PostgreSQL ma'lumotlar bazasini sozlash
      Agar siz PostgreSQL ma'lumotlar bazasidan foydalansangiz, Heroku'da quyidagi buyruq bilan ma'lumotlar bazasini yaratishingiz mumkin:
          heroku addons:create heroku-postgresql:hobby-dev
6. Loyihani Heroku'ga push qilish
      Git yordamida loyihangizni Heroku serveriga yuboring:
          git push heroku master
7. Ma'lumotlar bazasini migratsiya qilish
      Heroku'da migratsiyalarni bajarish uchun quyidagi buyruqni bajaring:
          heroku run python manage.py migrate
8. Djangoni ishga tushirish
      Heroku ilovasini ishga tushirgandan so'ng, brauzer orqali ilovangizni ko'rishingiz mumkin. Brauzerga quyidagi manzilni kiriting:
          https://CountryAward.herokuapp.com


