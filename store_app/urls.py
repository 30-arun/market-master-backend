from .views import *
from django.urls import path
from rest_framework.routers import DefaultRouter

app_name = 'store_app'


urlpatterns = [
    path('templates/', AllTemplateView.as_view(), name='templates'),
    path('templates/<int:template_id>/', GetTemplateView.as_view(), name='templates-id'),
    path('user-template/<int:user_id>/', UserTemplateView.as_view(), name='user-template'),
    path('user-template-detail/<int:user_id>/<int:user_template_id>/', UserTemplateDetailView.as_view(), name='user-template-detail'),
    path('post-user-template/', PostUserTemplateView.as_view(), name='post-user-template'),
    path('editor-template/<int:user_id>/<int:temp_id>/', EditorUserTemplateDetailView.as_view(), name='editor-template'),
    path('qrcode-history/', QrcodeView.as_view(), name='qrcode-history'),
    path('get-started/', GetStartedViewSet.as_view(), name='get-started'),    
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact-replied/', ContactRepliedView.as_view(), name='contact-replied'),
    path('appointment/', AppointmentView.as_view(), name='appointment'),  
    path('booking/', BookingView.as_view(), name='booking'),
    path('available-time/', AvailableTimeView.as_view(), name='available-time'),
    path('domain/<int:pk>/', DomainView.as_view(), name='domain-detail'),
    path('slug/<slug:slug>/', SlugAPIView.as_view(), name='slug_by_slug'),
    path('slug_id/<slug:slug>/', SlugIdAPIView.as_view(), name='slug_by_id'),

]
