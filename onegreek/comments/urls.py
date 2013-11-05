from django.conf.urls import patterns, url

urlpatterns = patterns('comments.views',
    url(r'^post/$',          'post_comment',       name='comments-post-comment'),
    url(r'^posted/$',        'comment_done',       name='comments-comment-done'),
    url(r'^flag/(\d+)/$',    'flag',             name='comments-flag'),
    url(r'^flagged/$',       'flag_done',        name='comments-flag-done'),
    url(r'^delete/(\d+)/$',  'delete',           name='comments-delete'),
    url(r'^deleted/$',       'delete_done',      name='comments-delete-done'),
    url(r'^approve/(\d+)/$', 'approve',          name='comments-approve'),
    url(r'^approved/$',      'approve_done',     name='comments-approve-done'),
)

urlpatterns += patterns('',
    url(r'^cr/(\d+)/(.+)/$', 'django.contrib.contenttypes.views.shortcut', name='comments-url-redirect'),
)
