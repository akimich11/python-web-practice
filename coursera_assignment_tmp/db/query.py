from datetime import datetime

from django.db.models import Q, Count, Avg
import pytz

from db.models import User, Blog, Topic


def create():
    user1 = User.objects.create(first_name='u1', last_name='u1')
    user2 = User.objects.create(first_name='u2', last_name='u2')
    user3 = User.objects.create(first_name='u3', last_name='u3')
    blog1 = Blog.objects.create(title='blog1', author=user1)
    blog2 = Blog.objects.create(title='blog2', author=user1)
    blog1.subscribers.add(user1, user2)
    blog2.subscribers.add(user2)
    topic1 = Topic.objects.create(title='topic1', blog=blog1, author=user1)
    date = pytz.utc.localize(datetime.strptime('2017-01-01', '%Y-%m-%d'))
    Topic.objects.create(title='topic2_content', blog=blog1, author=user3, created=date)
    topic1.likes.add(user1, user2, user3)


def edit_all():
    User.objects.all().update(first_name='uu1')


def edit_u1_u2():
    User.objects.filter(Q(first_name='u1') | Q(first_name='u2')).update(first_name='uu1')


def delete_u1():
    User.objects.filter(first_name='u1').delete()


def unsubscribe_u2_from_blogs():
    # Blog.subscribers.through.objects.filter(user__first_name='u2').delete()
    for blog in Blog.objects.all():
        blog.subscribers.filter(first_name='u2').delete()


def get_topic_created_grated():
    # date = datetime(year=2018, month=1, day=1, tzinfo=UTC)
    date = pytz.utc.localize(datetime.strptime('2018-01-01', '%Y-%m-%d'))
    return Topic.objects.filter(created__gt=date)


def get_topic_title_ended():
    return Topic.objects.filter(title__endswith='content')


def get_user_with_limit():
    return User.objects.order_by('-id')[:2]


def get_topic_count():
    # you can use Count('topic')
    return Blog.objects.all().annotate(topic_count=Count('topic__pk')).order_by('topic_count')


def get_avg_topic_count():
    return Blog.objects.all().annotate(topic_count=Count('topic__pk')).aggregate(avg=Avg('topic_count'))


def get_blog_that_have_more_than_one_topic():
    return Blog.objects.all().annotate(topic_count=Count('topic__pk')).filter(topic_count__gt=1)


def get_topic_by_u1():
    return Topic.objects.filter(author__first_name='u1')


def get_user_that_dont_have_blog():
    return User.objects.filter(blog__isnull=True)


def get_topic_that_like_all_users():
    return Topic.objects.annotate(likes_count=Count('likes__pk')).filter(likes_count=User.objects.count())


def get_topic_that_dont_have_like():
    return Topic.objects.filter(likes__likes__author__isnull=True)
