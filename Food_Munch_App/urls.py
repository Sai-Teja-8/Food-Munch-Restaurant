from django.urls import path
from . import views

urlpatterns=[
    path('',views.login,name="login"),
    path('Signup/',views.signup,name="create account"),
    path('Log Out/',views.LogOut,name="Log Out"),
    path('FoodMunch/<int:UserId>/',views.RestrauntMainPage,name="RestrauntMainPage"),
    path('Food Munch/Explore Menu/',views.exploremenu,name="exploremenu"),
    path('Food Munch/view menu/Non-Veg Section/',views.viewmenu_Non_Veg_Section,name='viewmenu Non-Veg Section'),
    path("Food Munch/view menu/veg Section",views.viewmenu_Veg_Section,name="viewmenu Veg Section"),
    path("Food Munch/view menu/Soups Section",views.viewmenu_Soups_Section,name="viewmenu Soups Section"),
    path("Food Munch/view menu/Fish & Sea Foods Section",views.viewmenu_Fish_and_Sea_Food_Section,name="viewmenu Fish & Sea Food Section"),
    path("Food Munch/view menu/Main Course Section",views.viewmenu_Main_Course_Section,name="viewmenu Main Course Section"),
    path("Food Munch/view menu/Noodles Section",views.viewmenu_Noodles_Section,name="viewmenu Noodles Section"),
    path("Food Munch/view menu/Salads Section",views.viewmenu_Salads_Section,name="viewmenu Salads Section"),
    path("Food Munch/view menu/Desserts Section",views.viewmenu_Desserts_Section,name="viewmenu Desserts Section"),
    path("Food Munch/Fresh Healthy Organic Food/Watch Video/",views.watch_video,name="watch_video"),
    path('Food Munch/view menu/payment/',views.paymentgateway,name="paymentgateway"),
    path('Food Munch/view menu/payment/success',views.successpage,name="successpage")
]