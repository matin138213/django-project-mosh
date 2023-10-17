from rest_framework.urls import path
from . import views
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet)
router.register('collection', views.CollectionViewSet)

products_routers = routers.NestedDefaultRouter(router, 'products', lookup='product')
products_routers.register('reviews', views.ReviewViewSet, basename='product_reviews')
urlpatterns = router.urls + products_routers.urls

# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>', views.ProductDetail.as_view()),
#     path('collection/', views.CollectionList.as_view(),name='collection_list'),
#     path('collection/<int:pk>', views.CollectionDetail.as_view(),name='collection_detail'),
# ]
