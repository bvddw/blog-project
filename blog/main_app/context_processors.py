from main_app.models import Topic


def custom_context(request):
    return {'topics': Topic.objects.all()}
