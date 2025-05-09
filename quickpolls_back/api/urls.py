from django.urls import path
from .views import RegisterView
from rest_framework_simplejwt.views import ( TokenObtainPairView, TokenRefreshView, )

urlpatterns = [
    # EndPoints para respectivamente: registrar um novo usuário, obter um token JWT e atualizar o token JWT.
    path('register/', RegisterView.as_view(), name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # EndPoints usuários
    path('polls/', PollListCreateView.as_view(), name='create_list_polls'), #criar e listar polls
    path('polls/<int:pk>/', PollRetrieveUpdateDeleteView.as_view(), name='list_put_delete_polls'), # atualizar e deletar polls por ID
    path('polls/<int:pk>/vote/', VoteListCreateView.as_view(), name='list_create_vote'), # votar em polls por ID
    path('polls/options/', OptionListCreateView.as_view(), name='list_create_poll_options'),
    path('polls/options/<int:pk>/', OptionRetrieveUpdateDestroyView.as_view(), name='list_update_destroy_poll_options'),

    path('polls/flag/', FlagCreateView.as_view(), name='create_flag_to_polls')

    # EndPoints administradores
    path('admin/polls/<int:pk>/', AdminPollRetrieveUpdateDeleteView.as_view(), name='admin_polls_actions'),
    path('admin/flags/', )
    path('admin/polls/<int:pk>/flagged/')


]
