from django.urls import path
from .views import RegisterView, 
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )

urlpatterns = [
    # EndPoints para respectivamente: registrar um novo usuário, obter um token JWT e atualizar o token JWT.
    path('register/', RegisterView.as_view(), name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('polls/', ) #criar e listar polls
    path('polls/<int:pk>/',) # atualizar e deletar polls por ID
    path('polls/<int:pk>/vote/',) # votar em polls por ID
    

]
