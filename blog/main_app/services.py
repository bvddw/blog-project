from main_app.models import Article, UserTopic, Topic
from django.contrib.auth import get_user_model
from django.db.models import Count, Q

UserModel = get_user_model()


def get_sorted_articles(user_id):
    """
    We will display a list of articles. If user has preferred articles, we will show relevant articles to them. If
    no, will show just 3 random articles. The more the article has topics that the user prefers, the more preferable
    it is for him, so ordering by amount preferred topics in article.
    """
    try:
        user = UserModel.objects.get(id=user_id)
    except UserModel.DoesNotExist:
        return None

    # take only preferred topics by current user
    preferred_topics = UserTopic.objects.filter(user=user).values_list('topic__title', flat=True)
    # take only articles, that connected to preferred topics
    articles = Article.objects.all().annotate(number_of_topics=Count('topics', filter=Q(topics__title__in=preferred_topics))).annotate(number_of_comments=Count('comment'))
    # let's display articles in relevant order for each user. Even if user has not preferred topics, we will show
    # articles just ordered by creation time.
    articles = articles.order_by('-number_of_topics')
    return articles


def get_sorted_topics(user):
    topics = Topic.objects.all()
    high_priority = []
    mid_priority = []
    low_priority = []
    for topic in topics:
        if topic.id in UserTopic.objects.filter(user=user).values_list('topic', flat=True):
            if UserTopic.objects.get(user=user, topic=topic).notify:
                high_priority.append({'topic': topic, 'priority': 2})
            else:
                mid_priority.append({'topic': topic, 'priority': 1})
        else:
            low_priority.append({'topic': topic, 'priority': 0})
    high_priority.extend(mid_priority)
    high_priority.extend(low_priority)
    return high_priority