from django.urls import path, include
from .views import (PostList, PostCreate, PostDetail, PostEdit, SearchResponse,
                    response_accept, response_delete, PostDelete)

urlpatterns = [
   path('', (PostList.as_view()), name='posts'),
   path('create/', PostCreate.as_view(), name='post_create'),
   path('<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
   path('<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('search/', SearchResponse.as_view(), name='search_page'),
   path('response/<int:pk>/accept', response_accept, name='response_accept'),
   path('response/<int:pk>/delete', response_delete, name='response_delete'),
]