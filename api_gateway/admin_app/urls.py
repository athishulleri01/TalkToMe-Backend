from django.urls import path, include
from  .views import UserAdminListView, UserAdminToggleBlockView
urlpatterns = [
  path("user/all/", UserAdminListView.as_view(), name="UserView"),
    path("user/block/<int:id>/", UserAdminToggleBlockView.as_view(), name="UserViews"),
]
