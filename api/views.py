from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from base.models import Item
from base.models import Product
from base.models import User, UserProfile
from .serializers import ItemSerializer
from .serializers import ProductSerializer
from .serializers import UserProfileSerializer
from .serializers import UpdateFavoritesSerializer
from .serializers import UpdateCartSerializer
from .serializers import UpdateOrderSerializer
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponseNotAllowed
import json

@csrf_exempt
def userApi(request, id=0):
    if request.method == 'GET':
        if id == 0:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            try:
                item = Item.objects.get(id=id)
                serializer = ItemSerializer(item)
                return JsonResponse(serializer.data, safe=False)
            except Item.DoesNotExist:
                return JsonResponse({"message": "Item not found"}, status=404)

    elif request.method == 'POST':
        user_data = JSONParser().parse(request)
        serializer = ItemSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "Added Successfully"}, safe=False)
        return JsonResponse({"message": "Failed to Add"}, safe=False)

    elif request.method == 'PUT':
        user_data = JSONParser().parse(request)
        try:
            item = Item.objects.get(id=id)
            serializer = ItemSerializer(item, data=user_data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({"message": "Updated Successfully"}, safe=False)
            return JsonResponse({"message": "Failed to Update"}, safe=False)
        except Item.DoesNotExist:
            return JsonResponse({"message": "Item not found"}, status=404)

    elif request.method == 'DELETE':
        try:
            item = Item.objects.get(id=id)
            item.delete()
            return JsonResponse({"message": "Deleted Successfully"}, safe=False)
        except Item.DoesNotExist:
            return JsonResponse({"message": "Item not found"}, status=404)
@csrf_exempt
def products(request):
    if request.method == 'POST':
        product_data = request.POST.dict()  # Convert form data to a dictionary
        product_data['pictures'] = request.FILES.get('pictures')  # Get the uploaded image
        serializer = ProductSerializer(data=product_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"product": "Product added successfully"}, safe=False)
        else:
            return JsonResponse(serializer.errors, safe=False)

    return HttpResponseNotAllowed(['POST'])
@csrf_exempt
def getproducts(request,name=""):
    if request.method == 'GET':
        if name=="":
            products = Product.objects.all()
            serializer = ProductSerializer(products, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            try:
                products = Product.objects.filter(name__icontains=name)
                if products.exists():
                    serializer=ProductSerializer(products,many=True)
                    return JsonResponse(serializer.data, safe=False)
                else:
                    return JsonResponse({"message": "Product not found"}, status=404)
            except Product.DoesNotExist:
                return JsonResponse({"message":"Product not found"},status=404)
    # return HttpResponseNotAllowed(['GET'])
@csrf_exempt
def signup_api(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        serializer = ItemSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User created successfully"}, safe=False)
        return JsonResponse({"message": "Invalid request data"}, safe=False)
    elif request.method == 'GET':
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return JsonResponse(serializer.data, safe=False)
    else:
        return HttpResponseNotAllowed(['POST', 'GET'])
@csrf_exempt
def login_api(request):
    if request.method == 'POST':
        user_data = JSONParser().parse(request)
        username = user_data.get('username')
        password = user_data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            return JsonResponse({"message": "Successfully Loged in"}, safe=False)
        return JsonResponse({"message": "Failed to Login"}, safe=False)
    if request.method == 'GET':
        if id == 0:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return JsonResponse(serializer.data, safe=False)
        else:
            try:
                item = Item.objects.get(id=id)
                serializer = ItemSerializer(item)
                return JsonResponse(serializer.data, safe=False)
            except Item.DoesNotExist:
                return JsonResponse({"message": "Item not found"}, status=404)
@csrf_exempt
def create_user_profile(request):
    user_data = JSONParser().parse(request)
    serializer = ItemSerializer(data=user_data)
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"message": "Added Successfully"}, safe=False)
    return JsonResponse({"message": "Failed to Add"}, safe=False)
@csrf_exempt
def update_user_profile(request, username):
    # Retrieve the user and user profile
    user = get_object_or_404(User, username=username)
    user_profile = get_object_or_404(UserProfile, user=user)

    # Handle GET request to retrieve user profile data
    if request.method == 'GET':
        serializer = UserProfileSerializer(user_profile)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK, safe=False)

    # Handle PUT request to update user profile data
    elif request.method == 'PUT':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"message": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)

        # Deserialize the request data
        serializer = UserProfileSerializer(user_profile,data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"message": "User profile updated successfully"}, status=status.HTTP_200_OK)
        return JsonResponse({"message": "Failed to update user profile", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # Return error for unsupported methods
    else:
        return JsonResponse({"message": "Invalid request method"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(['POST'])
def update_orders(request):
    serializer = UpdateCartSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        product_name = serializer.validated_data['product_name']
        action = serializer.validated_data['action']
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            
            if action == 'add':
                if product_name not in user_profile.item_ordered:
                    user_profile.item_ordered.append(product_name)
                    user_profile.save()
                    return JsonResponse({"message": "Product added to favorites"}, status=200)
                else:
                    return JsonResponse({"message": "Product already in favorites"}, status=400)
            
            elif action == 'remove':
                if product_name in user_profile.item_ordered:
                    user_profile.item_ordered.remove(product_name)
                    user_profile.save()
                    return JsonResponse({"message": "Product removed from favorites"}, status=200)
                else:
                    return JsonResponse({"message": "Product not found in favorites"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found."}, status=404)
    else:
        print(serializer.errors)  # Add this to see validation errors
        return JsonResponse({"error": serializer.errors}, status=400)

@api_view(['POST'])
def update_favorites(request):
    print("Request Data:", request.data)  # Log the incoming data
    serializer = UpdateFavoritesSerializer(data=request.data)
    
    if serializer.is_valid():
        username = serializer.validated_data['username']
        product_name = serializer.validated_data['product_name']
        action = serializer.validated_data['action']
        
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            
            if action == 'add':
                if product_name not in user_profile.favorites:
                    user_profile.favorites.append(product_name)
                    user_profile.save()
                    return JsonResponse({"message": "Product added to favorites"}, status=200)
                else:
                    return JsonResponse({"message": "Product already in favorites"}, status=400)
            
            elif action == 'remove':
                if product_name in user_profile.favorites:
                    user_profile.favorites.remove(product_name)
                    user_profile.save()
                    return JsonResponse({"message": "Product removed from favorites"}, status=200)
                else:
                    return JsonResponse({"message": "Product not found in favorites"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found."}, status=404)
    else:
        print(serializer.errors)  # Add this to see validation errors
        return JsonResponse({"error": serializer.errors}, status=400)


@api_view(['POST'])
def update_cart(request):
    serializer = UpdateCartSerializer(data=request.data)
        
    if serializer.is_valid():
        username = serializer.validated_data['username']
        product_name = serializer.validated_data['product_name']
        action = serializer.validated_data['action']
        
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
        
            if action == 'add':
                if product_name not in user_profile.cart:
                    user_profile.cart.append(product_name)
                    user_profile.save()
                    return JsonResponse({"message": "Product added to cart"}, status=200)
                else:
                    return JsonResponse({"message": "Product already in cart"}, status=400)
            
            elif action == 'remove':
                if product_name in user_profile.cart:
                    user_profile.cart.remove(product_name)
                    user_profile.save()
                    return JsonResponse({"message": "Product removed from cart"}, status=200)
                else:
                    return JsonResponse({"message": "Product not found in cart"}, status=400)
        
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found."}, status=404)
    
    return JsonResponse({"error": serializer.errors}, status=400)
@api_view(['GET'])
@csrf_exempt
def get_favorites(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)
        
        # Assuming 'favorites' is a list of product names
        favorites = user_profile.favorites
        
        product_details = []
        for product_name in favorites:
            try:
                # Assuming product names are unique, use get() instead of filter()
                product = Product.objects.get(name=product_name)
                serializer = ProductSerializer(product)
                product_details.append(serializer.data)
            except Product.DoesNotExist:
                # Continue if the product doesn't exist
                continue
        
        if product_details:
            return JsonResponse(product_details, safe=False)
        else:
            return JsonResponse({"message": "No valid products found in favorites."}, status=404)
    
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    except UserProfile.DoesNotExist:
        return JsonResponse({"error": "User profile not found."}, status=404)
@api_view(['GET'])
@csrf_exempt
def get_cart(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)

        # Get the 'cart' column data
        cart = user_profile.cart
        product_details = []
        for product_name in cart:
            try:
                product = Product.objects.get(name=product_name)
                serializer = ProductSerializer(product)
                product_details.append(serializer.data)
            except Product.DoesNotExist:
                continue
        if product_details:
            return JsonResponse(product_details,safe=False)
        else:
            return JsonResponse({"message": "No valid products found in cart."}, status=404)
        
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found."}, status=404)
@api_view(['GET'])
@csrf_exempt
def get_orders(request, username):
    try:
        user = User.objects.get(username=username)
        user_profile = UserProfile.objects.get(user=user)

        # Get the 'cart' column data
        orders = user_profile.item_ordered
        product_details = []
        for product_name in orders:
            try:
                product = Product.objects.get(name=product_name)
                serializer = ProductSerializer(product)
                product_details.append(serializer.data)
            except Product.DoesNotExist:
                continue
        if product_details:
            return JsonResponse(product_details,safe=False)
        else:
            return JsonResponse({"message": "No valid products found in orders."}, status=404)
        
    except User.DoesNotExist:
        return Response({"error": "User not found."}, status=404)
    except UserProfile.DoesNotExist:
        return Response({"error": "User profile not found."}, status=404)

@api_view(['POST'])
def update_mul_orders(request):
    serializer = UpdateOrderSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        product_names = serializer.validated_data['product_names']  # List of product names
        action = serializer.validated_data['action']
        try:
            user = User.objects.get(username=username)
            user_profile = UserProfile.objects.get(user=user)
            
            updated_products = []
            errors = []

            for product_name in product_names:
                if action == 'add':
                    if product_name not in user_profile.item_ordered:
                        user_profile.item_ordered.append(product_name)
                        updated_products.append(product_name)
                    else:
                        errors.append(f"{product_name} already in orders")

                elif action == 'remove':
                    if product_name in user_profile.item_ordered:
                        user_profile.item_ordered.remove(product_name)
                        updated_products.append(product_name)
                    else:
                        errors.append(f"{product_name} not found in orders")

            user_profile.save()  # Save once after processing all products

            return JsonResponse({"message": "Order updated"}, status=200)
        
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found."}, status=404)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "User profile not found."}, status=404)
    else:
        print(serializer.errors)  # To debug validation errors
        return JsonResponse({"error": serializer.errors}, status=400)
