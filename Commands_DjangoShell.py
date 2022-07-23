from news.models import *


# Доступ администратор - is_staff | Статус активный - is_active | Сделать суперюзера - is_superuser | Добавить почту - email
user1 = User.objects.create(username = 'mafilova', email='mafilova@hot.com', first_name = 'Mafilova', last_name='Makarova', is_active=True)
user2 = User.objects.create(username = 'manifa', email='manifa@mail.com', first_name = 'Manifas', last_name='Sidorova', is_active=True)
user3 = User.objects.create(username = 'manila', email='manila@iau.com', first_name = 'Manila', last_name='Milkovich', is_active=True)


# Создаем Автора на основе пользователя
author1 = Author.objects.create(author_user = user1)
author2 = Author.objects.create(author_user = user2)
author3 = Author.objects.create(author_user = user3)


# Добавить\Создать названия категорий
category01 = Category.objects.create(category_name='Ай-Ти')
category02 = Category.objects.create(category_name='Аналитика')
category03 = Category.objects.create(category_name='Безопасность')
category04 = Category.objects.create(category_name='Видео')
category05 = Category.objects.create(category_name='Погода')


# Добавить\Создать статью и\или новость
article01 = Post.objects.create(post_author=author1, position='PA', headline='Заголовок_статьи_1', post_text='Текст_статьиt_1')
article02 = Post.objects.create(post_author=author2, position='PA', headline='Заголовок_статьи_2', post_text='Текст_статьиt_2')
article03 = Post.objects.create(post_author=author3, position='PA', headline='Заголовок_статьи_3', post_text='Текст_статьиt_3')

news01 = Post.objects.create(post_author=author3, position='PN', headline='Заголовок_новости_1', post_text='Текст_новости_1')
news02 = Post.objects.create(post_author=author2, position='PN', headline='Заголовок_новости_2', post_text='Текст_новости_2')
news03 = Post.objects.create(post_author=author1, position='PN', headline='Заголовок_новости_3', post_text='Текст_новости_3')


# Привязываем статью\новость к котегориям
article01.post_category.add(category01)
article02.post_category.add(category02)
article03.post_category.add(category03)

news01.post_category.add(category04)
news02.post_category.add(category05)
news03.post_category.add(category02)


# Добовляем комментарий к статье\новосте
comment01 = Comment.objects.create(comment_post=article01, comment_user=user1, comment_text='Текст_статьи_комментария_1')
comment02 = Comment.objects.create(comment_post=article02, comment_user=user2, comment_text='Текст_статьи_комментария_2')
comment03 = Comment.objects.create(comment_post=article03, comment_user=user1, comment_text='Текст_статьи_комментария_3')
comment04 = Comment.objects.create(comment_post=article03, comment_user=user3, comment_text='Текст_статьи_комментария_4')
comment05 = Comment.objects.create(comment_post=article01, comment_user=user2, comment_text='Текст_статьи_комментария_5')

comment06 = Comment.objects.create(comment_post=news01, comment_user=user1, comment_text='Текст_новости_комментария_1')
comment07 = Comment.objects.create(comment_post=news02, comment_user=user3, comment_text='Текст_новости_комментария_3')
comment08 = Comment.objects.create(comment_post=news03, comment_user=user2, comment_text='Текст_новости_комментария_2')


# Ставим лайк\дизлайк статье\новости
comment01.like()
comment02.like()
comment03.like()
comment04.like()
comment01.like()
comment02.like()
comment03.like()
comment04.like()
comment02.like()
comment01.like()
comment05.like()
comment01.like()
comment06.like()
comment01.like()

comment01.dislike()
comment04.dislike()
comment03.dislike()
comment01.dislike()

article01.like()
article01.like()
article01.like()
article01.like()
article01.like()
article02.like()
article02.like()
article02.like()
article03.like()
article03.like()
article03.like()
article03.like()

news01.dislike()
news01.dislike()
news01.dislike()
news02.like()
news03.like()
news03.like()
news02.like()


# Обновляем рейтинг Author
author1.update_rating()
author2.update_rating()
author3.update_rating()


# Выводим рейтинг Author
author1.author_rating
author2.author_rating
author3.author_rating


# Вывод рейтинг Author с наибольшим колличеством оценок
best = Author.objects.all().order_by('-author_rating').values('author_user', 'author_rating')[0]
print(best)

best1 = Author.objects.all().order_by('-author_rating').values('author_user__first_name', 'author_rating')[0]
print(best1)


# Вывод статьи\новости с наибольшим рейтингом
Post.objects.all().order_by('-post_rating').values('create_date', 'post_author__author_user__username', 'post_rating', 'headline', 'post_text')[0]


# Вывод комментария и заголовка статьи\новости с которым он связан
Comment.objects.all().order_by().values('comment_create', 'comment_user__username', 'comment_post__headline', 'comment_rating', 'comment_text')[0]



Post.objects.all().values('post_author__author_user__last_name', 'headline')
Post.objects.filter(post_author=author2)
Post.objects.filter(headline='Заголовок_новости_1').values('post_author__author_user__first_name')


Comment.objects.all().values('comment_post__headline', 'comment_user__first_name')
Comment.objects.filter(comment_post=article01).values('comment_text')
Comment.objects.filter(comment_text='Текст_статьи_комментария_5').values('comment_rating')


Author.objects.filter(id=6)
Author.objects.all().values('author_user__first_name', 'id')
