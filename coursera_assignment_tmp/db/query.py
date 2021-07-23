from datetime import datetime
from django.utils import timezone

from django.db.models import Q, Count, Avg
import pytz

from db.models import User, Blog, Topic


def create_user(first_name, last_name):
    user = User(first_name=first_name, last_name=last_name)
    user.save()
    return user


def create_blog(title, author):
    blog = Blog(title=title, author=author)
    blog.save()
    return blog


def create_topic(title, blog, author, created=timezone.now()):
    topic = Topic(title=title, blog=blog, author=author, created=created)
    topic.save()
    return topic


def create():
    user1 = create_user(first_name='u1', last_name='u1')
    user2 = create_user(first_name='u2', last_name='u2')
    user3 = create_user(first_name='u3', last_name='u3')
    blog1 = create_blog(title='blog1', author=user1)
    blog2 = create_blog(title='blog2', author=user1)
    blog1.subscribers.add(user1, user2)
    blog2.subscribers.add(user2)
    topic1 = create_topic(title='topic1', blog=blog1, author=user1)
    date = pytz.utc.localize(datetime.strptime('2017-01-01', '%Y-%m-%d'))
    create_topic(title='topic2_content', blog=blog1, author=user3, created=date)
    topic1.likes.add(user1, user2, user3)


def edit_all():
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    User.objects.filter(Q(first_name='u1') | Q(first_name='u2')).update(first_name='uu1')


def delete_u1():
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    for blog in Blog.objects.all():
        blog.subscribers.filter(first_name='u2').delete()


def get_topic_created_grated():
    date = pytz.utc.localize(datetime.strptime('2018-01-01', '%Y-%m-%d'))
    return Topic.objects.filter(created__gt=date)


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.order_by('-id')[:2]


def get_topic_count():
    return Topic.objects.values('blog_id').annotate(topic_count=Count('pk')).order_by('topic_count')


def get_avg_topic_count():
    return Topic.objects.values('blog_id').annotate(topic_count=Count('pk')).aggregate(Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    return Topic.objects.values('blog_id').annotate(topic_count=Count('pk')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.filter(blog__isnull=True)


def get_topic_that_like_all_users():
    return Topic.objects.raw("""select * from db_topic natural join db_topic_likes where
                                (select count(topic_id) from db_topic_likes group by topic_id) =
                                (select count(*) from db_user)""")


def get_topic_that_dont_have_like():
    return Topic.objects.filter(likes__likes__author__isnull=True)
