from django.urls import path,include
from django.views.generic import TemplateView

from . import views
from .views import PostCreate,UpdatePost,DeletePost,CategoryCreate,UpdateCategory,DeleteCategory,CreateTag,UpdateTag,DeleteTag,SiteSettings




app_name = 'Posts'
urlpatterns = [
	path("Welcome/", views.Welcome, name = "Welcome" ),
	path("Single/<int:pk>", views.Single, name = "Single" ),
	path("Category/<int:pk>", views.CategoryPage, name = "CategoryPage" ),
	path("Tag/<int:pk>", views.TagPage, name = "TagPage" ),
	path("Search/", views.Search, name = "Search" ),
	path("", views.ShowPosts, name = "ShowPosts" ),
	path("CreatePost/", PostCreate.as_view(), name = "CreatePost" ),
	path("UpdatePost/<int:pk>/", UpdatePost.as_view(), name = "UpdatePost" ),
	path("DeletePost/<int:pk>/", DeletePost.as_view(), name = "DeletePost" ),
	path("AddComment/<int:pk>/", views.AddComment, name = "AddComment" ),
	path("CommentApprove/<int:pk>/", views.CommentApprove, name = "CommentApprove" ),
	path("CommentRemove/<int:pk>/", views.CommentRemove, name = "CommentRemove" ),
	path("ShowCategories/", views.ShowCategories, name = "ShowCategories" ),
	path("CreateCategory/", CategoryCreate.as_view(), name = "CreateCategory" ),
	path("UpdateCategory/<int:pk>/", UpdateCategory.as_view(), name = "UpdateCategory" ),
	path("DeleteCategory/<int:pk>/", DeleteCategory.as_view(), name = "DeleteCategory" ),
	path("ShowTags/", views.ShowTags, name = "ShowTags" ),
	path("CreateTag/", CreateTag.as_view(), name = "CreateTag" ),
	path("UpdateTag/<int:pk>/", UpdateTag.as_view(), name = "UpdateTag" ),
	path("DeleteTag/<int:pk>/", DeleteTag.as_view(), name = "DeleteTag" ),
	path("Settings/<int:pk>", SiteSettings.as_view() , name = "SiteSettings" ),
	path("UserPage/", views.UserPage, name = "UserPage" ),
	path("DeactivateUser/<int:pk>", views.DeactivateUser, name = "DeactivateUser" ),
	path("MakeAdmin/<int:pk>", views.MakeAdmin, name = "MakeAdmin" ),
	path("Profile/<int:pk>", views.ProfileSettings, name = "ProfileSettings" ),
]