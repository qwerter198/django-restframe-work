# Django-rest-framework

此範例建立一個簡單的django框架並使用rest framework套件來時做Restful API

建立類別與商品的Restful API

1. 參考先前的[django-example](https://github.com/qwerter198/django-example) 建立Django專案(djangorestframework)與Django應用程式(product)
2. 安裝rest framework套件
    
    ```bash
    pip install djangorestframework
    ```
    
3. 在設定文件(product/setting.py)中添加rest_framework
    
    ```python
    INSTALLED_APPS = [
        # ...
        'product',
        'rest_framework',
    ]
    ```
    
4. 在設定文件(product/setting.py)新增設置API權限允許任何人訪問，並啟用了基於Session的身份驗證
    
    ```python
    REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.AllowAny',
        ],
        'DEFAULT_AUTHENTICATION_CLASSES': [
            'rest_framework.authentication.SessionAuthentication',
        ],
    }
    ```
    
5. 創建模型model(product/models.py)
    
    ```python
    from django.db import models
    import uuid
    
    from django.db import models
    
    class Category(models.Model):
        category_id = models.UUIDField(
            primary_key=True, default=uuid.uuid4, editable=False)
        category_name = models.CharField(max_length=255, unique=True)
    
        def __str__(self):
            return self.category_name
    
    class Product(models.Model):
        product_id = models.UUIDField(
            primary_key=True, default=uuid.uuid4, editable=False)
        product_name = models.CharField(max_length=255)
        description = models.TextField()
        price = models.DecimalField(max_digits=10, decimal_places=2)
        category = models.ForeignKey(
            Category, on_delete=models.CASCADE, related_name='products')
    
        def __str__(self):
            return self.product_name
    ```
    
6. 新增序列化器Serializer(product/serializers.py)
序列化器用於將模型數據轉換為JSON格式，或者將JSON數據轉換為模型實例
    
    ```python
    from rest_framework import serializers
    
    from .models import Category, Product
    
    class CategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = Category
            fields = '__all__'
    
    class ProductSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__'
    ```
    
7. 創建視圖View(product/views.py)
    
    ```python
    from rest_framework import viewsets
    from .models import Category, Product
    from .serializers import CategorySerializer, ProductSerializer
    from django.http import JsonResponse
    from rest_framework import generics
    from django.shortcuts import get_object_or_404
    
    class CategoryViewSet(viewsets.ModelViewSet):
        queryset = Category.objects.all()
        serializer_class = CategorySerializer
    
    class ProductViewSet(viewsets.ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
    
    class ProductsByCategoryView(generics.ListAPIView):
        serializer_class = ProductSerializer
    
        def get_queryset(self):
            category_id = self.kwargs['category_id']
            category = get_object_or_404(Category, category_id=category_id)
            return Product.objects.filter(category=category)
    ```
    
8. 設置url(djangorestframework/urls.py)
    
    ```python
    from django.contrib import admin
    from django.urls import path, include
    
    from rest_framework.routers import DefaultRouter
    from product import views
    
    router = DefaultRouter()
    router.register(r'categories', views.CategoryViewSet)
    router.register(r'products', views.ProductViewSet)
    
    urlpatterns = [
        path('categories/<uuid:category_id>/products/', views.ProductsByCategoryView.as_view(), name='produc
    ```
    
9. 更新資料庫
    
    ```python
    python manage.py makemigrations product
    python manage.py migrate
    ```
    
10. 啟動web服務
    
    ```python
    python manage.py runserver
    ```
    

### 執行成功後即可測試類別與商品API

- 類別
    - GET:
        
        ```bash
        curl --location 'http://127.0.0.1:8000/categories/'
        ```
        
        ```bash
        curl --location 'http://127.0.0.1:8000/categories/{{category_id}}'
        ```
        
    - POST:
        
        ```bash
        curl --location 'http://127.0.0.1:8000/categories/' \
        --header 'Content-Type: application/json' \
        --data '{
            "category_name": "餅乾"
        }'
        ```
        
    - PUT:
        
        ```bash
        curl --location --request PUT 'http://127.0.0.1:8000/categories/{{category_id}}/' \
        --header 'Content-Type: application/json' \
        --data '{
            "category_name": "餅乾1"
        }'
        ```
        
    - DELETE:
        
        ```bash
        curl --location --request DELETE '[http://127.0.0.1:8000/categories/](http://127.0.0.1:8000/categories/5c5a0d30-4a10-4803-a29d-10768c98a6d3/){{category_id}}[/](http://127.0.0.1:8000/categories/5c5a0d30-4a10-4803-a29d-10768c98a6d3/)'
        ```
        
- 商品
    - GET:
        
        ```bash
        curl --location 'http://127.0.0.1:8000/products/'
        ```
        
        ```bash
        curl --location 'http://127.0.0.1:8000/products/{{product_id}}'
        ```
        
    - POST:
        
        ```bash
        curl --location 'http://127.0.0.1:8000/products/' \
        --header 'Content-Type: application/json' \
        --data '{
            "product_name": "可樂果",
            "description":"好吃的可樂果",
            "price": 35,
            "category": "{{category_id}}"
        }'
        ```
        
    - PUT:
        
        ```bash
        curl --location --request PUT 'http://127.0.0.1:8000/products/{{product_id}}/' \
        --header 'Content-Type: application/json' \
        --data '{
            "product_name": "養樂多1",
            "description": "好喝的養樂多1",
            "price": "14.00",
            "category": "{{category_id}}"
        }'
        ```
        
    - DELETE:
        
        ```bash
        curl --location --request DELETE 'http://127.0.0.1:8000/products/{{product_id}}/'
        ```
        
- 取得指定類別的商品
    - GET
        
        ```bash
        curl --location 'http://127.0.0.1:8000/categories/{{category_id}}/products/'
        ```
