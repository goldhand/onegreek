try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

urlpatterns = patterns('comments.views',
                       #url(r'^post/ajax/$', 'post_comment_ajax', name='comments-post-comment-ajax'),
                       url(r'', include('django.contrib.comments.urls')),
                       )
