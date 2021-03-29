from django.urls import path
from .views import AssinaturaList, AssinaturaDetail, AssinaturaCreate, AssinaturaUpdate, CustomDeleteView, CustomLoginView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),

    path('', AssinaturaList.as_view(), name='assinaturas'),
    path('assinatura/<int:pk>/', AssinaturaDetail.as_view(), name='assinatura'),
    path('criar-assinatura/', AssinaturaCreate.as_view(), name='assinatura-create'),
    path('atualizar-assinatura/<int:pk>/', AssinaturaUpdate.as_view(), name='assinatura-update'),
    path('deletar-assinatura/<int:pk>/', CustomDeleteView.as_view(), name='assinatura-delete'),
]
