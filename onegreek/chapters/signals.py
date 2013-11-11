from django.dispatch import Signal

chapter_created = Signal(providing_args=["request", "chapter"])