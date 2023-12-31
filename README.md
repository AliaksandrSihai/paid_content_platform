# paid_content_platform
**All dependence in requirements.txt, an example of all the environment variables in the file .env_sample, test coverage = 94 %, flake8 = 100%**.
<br>**Before launching, you must register in stripe.com and add your api_secret key to the .env file ( necessary to create).**

<br>**To run the project:**
- `git clone https://github.com/AliaksandrSihai/paid_content_platform`
- next need to create a .env file, add your api_secret key to this file, fill in all other configurations (required configurations in .env_sample) and create a database.
- go to https://stripe.com/docs/stripe-cli#install install(with your operating system) and log in to the CLI, after logging in, add your webhook signing secret to the .env file(STRIPE_WEBHOOK_KEY=your webhook signing secret).
  
  - `python -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
  - `python manage.py migrate `
  - create a superuser, you need to add to the file users/management/commands/csu.py the necessary data (phone, password), and run: `python manage.py csu`
  - ` python manage.py runserver`
  
  <br>**with Docker:**
  - `git clone https://github.com/AliaksandrSihai/paid_content_platform && docker-compose up --build `
  - create a superuser, you need to add to the file users/management/commands/csu.py the necessary data (phone, password), and run: `docker-compose exec paid_content python manage.py csu`.
  
- log in to the admin panel and create all the necessary subscriptions(leave the stripe_price_id field empty).

## Used stack:
- **Django**
- **Django REST framework**
- **PostgreSQL**
- **Stripe**
- **Docker**
- **Nginx**
## Test:
- **Unittest**
## Documentation:
- **Drf-yasg**

## About project
  The project implements a platform for publishing posts, which can be both free 
  (which are available to all users without registration) and paid 
  (which are available only to those users who have registered and paid  for a subscription). 
  Anonymous users cannot create or ike any posts.The posts have a counter of views and add likes. 
  Registration of new users by phone number. Paying for a subscription using Stripe.

---
  В проекте реализована платформа для публикации постов, которые могут быть как бесплатными 
  (которые доступны всем пользователям без регистрации), так и платными 
  (которые доступны только тем пользователям, которые зарегистрировались и оплатили подписку). 
  Анонимные пользователи не могут создавать или лайкать какие-либо посты.
  У постов реализован счетчик просмотров и добавление в понравившиеся(лайки).
  Регистрация нового пользователя происходит по номеру телефона. Оплата подписки с помощью Stripe.




