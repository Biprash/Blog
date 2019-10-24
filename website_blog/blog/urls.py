from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.About, name='about'),
    path('post/new/', views.NewPost.as_view(), name='new_post'),
    path('post/<int:pk>/', views.DetailViewPost, name='post_detail'),
    path('draft/<int:pk>/', views.DraftPost, name='draft'),
    path('draft/publish/<int:pk>/', views.PublishDraftPost, name='draft_publish'),
    path('post/delete/<int:pk>/', views.DeletePost, name='delete_post'),
    path('post/edit/<int:pk>/', views.EditPost, name='edit_post'),
    path('user/detail/<int:pk>/', views.UserDetailView, name='user_detail'),
    path('user/<int:pk>/',views.UserProfile, name='profile'),
    path('comment/approve/<int:pk>/',views.ApproveComment, name='approve_comment'),
    path('comment/delete/<int:pk>/',views.DeleteComment, name='delete_comment'),

    path('search/', views.search_view, name='search')
]