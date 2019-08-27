from django.urls import path
from mainapp.views import user_list, user_list2, add_user, user_update, user_delete, get_fruit_all, find_fruit, \
    find_store

urlpatterns = [
    path('list/', user_list),
    path('list2/', user_list2),
    path('add/', add_user),
    path('update/', user_update),
    path('delete/', user_delete),
    path('fruits/', get_fruit_all),
    path('find',find_fruit),
    path('store',find_store)
]
