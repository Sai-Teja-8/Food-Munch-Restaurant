from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse,JsonResponse
from random import randint
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
from .models import *
from django.urls import reverse
from datetime import datetime
import re

# Create your views here.

def login(request):
    MobileNumber=request.POST.get("LoginMobileNumber")
    Password=request.POST.get("LoginPassword")
    ErrorFlag=False
    ErrorMsgList=[]
    if request.method=="POST":
        ExistingUser=SignupSection.objects.filter(MobileNumber=MobileNumber,Password=Password).first()
        if ExistingUser:
            ErrorFlag=False
            request.session["user_id"]=ExistingUser.id
            NewUser=LoginSection.objects.create(User=ExistingUser)
            NewUser.save()
            UserId=request.session["user_id"]
            return redirect(reverse("RestrauntMainPage", kwargs={"UserId": UserId}))
            #return render(request,"BasicRestrauntStructure.html")
        else:
            ErrorFlag=True
            ErrorMsgList.append("Invalid mobile number or password")
            LoginDetails={
                "ErrorFlag":ErrorFlag,
                "ErrorMsgList":ErrorMsgList
            }
            return render(request,"LoginPage.html",context=LoginDetails)
    else:
        if request.session.get("user_id"):
            return redirect("RestrauntMainPage",UserId=request.session["user_id"])
        else:
            return render(request,"LoginPage.html")

def signup(request):
    CustomerName=request.POST.get("SignupCustomerName")
    MobileNumber=request.POST.get("SignupMobileNumber")
    EmailId=request.POST.get("SignupEmailId")
    Password1=request.POST.get("SignupPassword1")
    Password2=request.POST.get("SignupPassword2")
    regex='^\w+([\.-]?\w+)+@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    ErrorFlag=False
    ErrorMsgList=[]
    if request.method=="POST":
        ExistingUser=SignupSection.objects.filter(MobileNumber=MobileNumber).first()
        if ExistingUser:
            ErrorFlag=True
            ErrorMsgList.append("User with this mobile number already exists")
            SignUpDetails={
                "ErrorFlag":ErrorFlag,
                "ErrorMsgList":ErrorMsgList
            }
            return render(request,'SignupPage.html',context=SignUpDetails)
        else:
            if Password1==Password2 and (len(MobileNumber)==10 and MobileNumber.isnumeric()) and re.search(regex,EmailId):
                ErrorFlag=False
                NewUser=SignupSection(CustomerName=CustomerName,MobileNumber=MobileNumber,EmailId=EmailId,Password=Password2)
                NewUser.save()
                request.session["user_id"]=NewUser.id
                UserId=request.session["user_id"]
                return redirect(reverse("RestrauntMainPage",kwargs={"UserId":UserId}))
            else:
                if not Password1==Password2:
                    ErrorFlag=True
                    ErrorMsgList.append("Password did not match")
                if not len(MobileNumber)==10:
                    ErrorFlag=True
                    ErrorMsgList.append("Mobile Number must be exactly 10 digits")
                if not MobileNumber.isdigit():
                    ErrorFlag=True
                    ErrorMsgList.append("Mobile Number must be only numbers not alphabets or any other or any special characters")
                if not re.search(regex,EmailId):
                    ErrorFlag=True
                    ErrorMsgList.append("Invalid Email Id")
                SignUpDetails={
                    "ErrorFlag":ErrorFlag,
                    "ErrorMsgList":ErrorMsgList
                }
                return render(request,'SignupPage.html',context=SignUpDetails)
    else:
         return render(request,"SignupPage.html")   

def LogOut(request):
    request.session.clear()
    return redirect("login")

def RestrauntMainPage(request,UserId):
    try:
        LoginDetails=SignupSection.objects.get(id=UserId)
        LoginMember=LoginDetails.CustomerName
        return render(request,'BasicRestrauntStructure.html',{"LoginMember":LoginMember})
    except:
        return render(request,"404.html")
    
def exploremenu(request):
    LoginUser={
        "UserId":request.session.get("user_id")
    }
    return render(request,'ExploreMenuSection.html',context= LoginUser)

def viewmenu_Non_Veg_Section(request):
    NonVeg_Items={
        "SectionName":"Non-Veg_Items_Images",
        "FoodItem":"Non-Veg Starters",
        "UniqueId":"UI80001",
        "ItemDetails":zip(["chicken-biryani","Tilapia-with-Tomatoes","egg-dum-biryani","afghani-tandoori-chicken_360","grilled-chicken","biryani","fish-finger","badam-korma"],["Chicken Biryani Jambo Pack","Brazilian Fish Stew","Egg Dum Biryani","Fish Dum Biryani","Grilled Chicken Escalope with Fresh Salsa","Malabar Fish Biryani","Curried Parmesan Fish Fingers","Mutton Korma"],["$ 5.79","$ 39","$ 2.89","$ 4","$ 4.89","$ 7","$ 5.12","$ 3"])
        }
    return render(request,'ViewMenuSection.html',context=NonVeg_Items)

def viewmenu_Veg_Section(request):
    Veg_Items={
        "SectionName":"Veg_Items_Images",
        "FoodItem":"Veg Starters",
        "UniqueId":"UI80002",
        "ItemDetails":zip(["Chevre-and-Tomato-Tart","coconut-curry-cauliflower","Eggplant-Parmigiana-Vegetarian-Dish","Jackfruit-Enchiladas","Pesto-Zoodles-Vegetarian-dish","Ricotta-Wheat-Pizza","Veggie-mushroom-burger","veggie-primavera"],["Chevre and Tomato Tart","Coconut Curry Cauliflower","Eggplant Parmigiana Vegetarian Dish","Jackfruit Enchiladas","Pesto Zoodles Vegetarian Dish","Ricotta Wheat Pizza","Veggie Mushroom Burger","Veggie Primavera"],["$ 5","$ 6.89","$ 4","$ 6.8","$ 4.3","$ 7","$ 3.6","$ 8"])
    }
    return render(request,'ViewMenuSection.html',context=Veg_Items)

def viewmenu_Soups_Section(request):
    Soups_Items={
        "SectionName":"Soups_Images",
        "FoodItem":"Soups",
        "UniqueId":"UI80003",
        "ItemDetails":zip(["Vegetable-Quinoa-Soup-Vegetarian","minestrone-soup","Vegan-Tomato-Soup","Roasted-Butternut-Squash-Soup","Roasted-Tomato-soup","Easy-and-Delicious-Minestrone-Soup","tomato-beetroot-carrot-soup","Green-Soup"],["Vegetable Quinoa Soup","Minestrone Soup","Vegan Tomato Soup","Roasted Butternut Squash Soup","Roasted Tomato Soup","Minestrone Soup","Tomato Beetroot Carrot Soup","Green Soup"],["$ 8.4","$ 3.99","$ 7.2","$ 8","$ 1.4","$ 6","$ 9.26","$ 3.5"])
    }
    return render(request,'ViewMenuSection.html',context=Soups_Items)

def viewmenu_Fish_and_Sea_Food_Section(request):
    Fish_and_Sea_Food_Items={
        "SectionName":"Fish_and_Sea_Food_Item_Images",
        "FoodItem":"Fish & Sea Food",
        "UniqueId":"UI80004",
        "ItemDetails":zip(["Southeast-Asian-Food-Tom-Yum-Goong","Shark and Ray Gardens","Mediterranean Octopus","gaint-river-prawn","stir-fired-crab","teriyaki-shark-steaks","blue-jellyfish","Mustelids"],["Southeast Asian Food Tom-Yum-Goong","Shark and Ray Gardens","Mediterranean Octopus","Gaint River Prawn","Stir Fired Crab","Teriyaki Shark Steaks","Blue Jelly Fish","Mustelids"],["$ 12","$ 15.80","$ 17.78","$ 22","$ 16.8080","$ 22","$ 19.99","$ 31.13"])
    }
    return render(request,'ViewMenuSection.html',context=Fish_and_Sea_Food_Items)

def viewmenu_Main_Course_Section(request):
    Main_Course_Items={
        "SectionName":"Main_Course_Images",
        "FoodItem":"Main Course",
        "UniqueId":"UI80005",
        "ItemDetails":zip(["Slow-Cooker-Butter-Chicken","Chicken-Korma","Mughali-Chicken","Easy-Chana-Masala","dal-makhani-indian-food","Gobi-Aloo","parsi-brown-rice","Kati Rolls"],["Butter Chicken","Chicken Korma","Mughali Chicken","Chana Masala","Dal Makhani Indian Food","Gobi Aloo","Parsi Brown Rice","Kati Rolls"],["$ 3.67","$ 1.42","$ 5","$ 2","$ 1.45","$ 4.68","$ 1.43","$ 1.11"])
    }
    return render(request,'ViewMenuSection.html',context=Main_Course_Items)

def viewmenu_Noodles_Section(request):
    Noodles_Items={
        "SectionName":"Noodles_Images",
        "FoodItem":"Noodles",
        "UniqueId":"UI80006",
        "ItemDetails":zip(["maagi-noodles","veg-noodles","vegetable-chow-mein-noodles","pasta-carbonara-recipe","green-noodles-with-spinach-pesto","Thai-Basil-Noodles-with-eggs","chicken-noodles","cold-soba-noodles"],["Maagi Noodles","Veg Noodles","Vegetable Chow Mein Noodles","Pasta Carbonara Recipe","Green Noodles With Spinach Pesto","Thai Basil Noodles with Eggs","Chicken Noodles","Cold Soba Noodles"],["$ 4","$ 1.82","$ 2","$ 2.23","$ 1.47","$ 4","$ 2","$ 3.18"])
    }
    return render(request,'ViewMenuSection.html',context=Noodles_Items)

def viewmenu_Salads_Section(request):
    Salads_Items={
        "SectionName":"Salads_Images",
        "FoodItem":"Salads",
        "UniqueId":"UI80007",
        "ItemDetails":zip(["vegetable-salad-recipe","creamy-cucumber-dill-salad","boiled-peanut-salad","edamame-corn-salad","beetroot-chickpea-salad","mango-avocado-salad","watermelon-salad","macaroni-salad"],["Vegetable Salad Recipe","Creamy Cucumber Dill Salad","Boiled Peanut Salad","Edamame Corn Salad","Beetroot Chickpea Salad","Mango Avocado Salad","Watermelon Salad","Macaroni Salad"],["$ 2","$ 1.29","$ 2.54","$ 2.53","$ 1.56","$ 3","$ 1.98","$ 3.8"])
    }
    return render(request,'ViewMenuSection.html',context=Salads_Items)

def viewmenu_Desserts_Section(request):
    Desserts_Items={
        "SectionName":"Desserts_Images",
        "FoodItem":"Desserts",
        "UniqueId":"UI80008",
        "ItemDetails":zip(["strawberry-crunch-poke-cake","key-lime-pie-mousse","granita","dolewhip","nutellapops","Buckeye Bundt Cake","Sweet-Homemade-Pastel-Cupcakes","Chocolate-Cakes"],["Strawberry Crunch Poke Cake","Key Lime Pie Mousse","Granita","Dolewhip","Nutellapops","Buckeye Bundt Cake","Sweet Homemade Pastel Cupcakes","Chocolate Cakes"],["$ 9.45","$ 11.21","$ 8.34","$ 8.49","$ 10","$ 13.67","$ 12.65","$ 11.11"])
    }
    return render(request,'ViewMenuSection.html',context=Desserts_Items)

def watch_video(request):
    UserId=request.session.get("user_id")
    video=Video.objects.all()
    return render(request,'video.html',{"Video":video,"UserId":UserId})

def paymentgateway(request):
    Image=request.GET.get("Image","")
    ItemName=request.GET.get("ItemName","")
    Cost=request.GET.get("Cost","")
    SectionName=request.GET.get("SectionName","")
    request.session["item_name"]=ItemName
    request.session["item_cost"]=Cost
    return render(request,'PaymentSection.html',{"ItemName":ItemName,"Cost":Cost,"Image":Image,"SectionName":SectionName})

def successpage(request):
    ErrorFlag=False
    ErrorMsgList=[]
    regex='^\w+([\.-]?\w+)+@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    CurrentDate=datetime.now()
    CurrentYear=CurrentDate.year
    CurrentMonth=CurrentDate.month
    UserId=request.session.get("user_id")
    ItemName=request.session.get("item_name")
    Cost=request.session.get("item_cost")
    if request.method=="POST":
        CustomerName=request.POST.get("CustomerFullName")
        EmailId=request.POST.get("CustomerEmailId")
        MobileNumber=request.POST.get("CustomerMobileNumber")
        Address=request.POST.get("CustomerAddress")
        City=request.POST.get("CustomerCity")
        State=request.POST.get("CustomerState")
        PinCode=request.POST.get("CustomerPinCode")
        PaymentMethod=request.POST.get("CustomerPaymentMethod")
        CardName=request.POST.get("CustomerCardName")
        CardNumber=request.POST.get("CustomerCardNumber")
        CardExpiry=request.POST.get("CustomerCardExpiry")
        Cvv=request.POST.get("CustomerCvv")

        if int(CardExpiry[3:])>CurrentYear:
            ErrorFlag=False
        elif int(CardExpiry[3:])==CurrentYear:
            if int(CardExpiry[:2])>=CurrentMonth:
                ErrorFlag=False
            else:
                ErrorFlag=True
                ErrorMsgList.append("Your Card has expired its month. Finish the payment usying another card")
        else:
            ErrorFlag=True
            ErrorMsgList.append("Your Card has expired its year. Finish the payment usying another card")
        if not len(MobileNumber)==10:
            ErrorFlag=True
            ErrorMsgList.append("Mobile Number must be exactly 10 digits")
        if not MobileNumber.isnumeric():
            ErrorFlag=True
            ErrorMsgList.append("Mobile Number must contain only digits not alphabets or any special characters")
        if not CardName.upper() in ["VISA","MASTERCARD","RUPAY","MAESTRO","UNIONPAY","AMERICAN EXPRESS","DISCOVER","JCB","DINERS CLUB","CIRRUS"]:
            ErrorFlag=True
            ErrorMsgList.append("Card is Not Acceptable.Try usying another card")
        if not len(PinCode)==6:
            ErrorFlag=True
            ErrorMsgList.append("PinCode must be exactly 6 digits")
        if len(Cvv)!=3:
            ErrorFlag=True
            ErrorMsgList.append("Cvv must be exactly 3 digits")
        if not re.search(regex,EmailId):
            ErrorFlag=True
            ErrorMsgList.append("Not a valid Email address")
        if len(CardNumber)!=19:
            ErrorFlag=True
            ErrorMsgList.append("Card Number must be exactly 16 digits")
        if not ErrorFlag==True:
            StoreData=PaymentSectionDetails(CustomerName=CustomerName,EmailId=EmailId,MobileNumber=MobileNumber,Address=Address,City=City,State=State,PinCode=PinCode,PaymentMethod=PaymentMethod,CardName=CardName,CardNumber=CardNumber,CardExpiry=CardExpiry,Cvv=Cvv)
            OrderData=OrderDetails(UserId=UserId,ItemName=ItemName,Cost= Cost)
            StoreData.save()
            OrderData.save()
            return render(request,'SuccessPage.html',{"UserId":request.session.get("user_id")})
        else:
            SubmitForm={
                "ErrorFlag":ErrorFlag,
                "ErrorMsgList":ErrorMsgList
            }
            return render(request,'PaymentSection.html',context=SubmitForm)

def error_404_view(request,exception):
    return render(request,'404.html')




