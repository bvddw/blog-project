from topics.models import Topic


def custom_context(request):
    return {'topics': Topic.objects.all()}
