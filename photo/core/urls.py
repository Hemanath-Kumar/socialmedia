from django.urls import path
from .import views

urlpatterns=[

    #index
    path("",views.index,name="index"),
    path("index",views.index,name="index"),
    path("profile/index",views.index,name="index"),#profile reverse

    #signin,singup,logout
    path("signup",views.signup,name="signup"),
    path("signin",views.signin,name="signin"),
    path("logout",views.logout,name="logout"),
    path("profile/logout",views.logout,name="logout"),
    
    #account
    path("account",views.account,name="account"),
    path("profile/account",views.account,name="account"),#profile reverse to account
    
    path("upload",views.post,name="upload"),
    path("profile/upload",views.post,name="upload"),
    path("post-like",views.likepost,name="like"),

    #profile page
    path("profile/<str:pk>",views.profile_account,name="profile_account"),
    path("follows",views.follows,name="follow"),

    path("following",views.userfollowing,name="following"),
    path("profile/following",views.userfollowing,name="following"),


    path("follower",views.follower,name="follower"),
    path("profile/follower",views.follower,name="follower"),


    





    
]

