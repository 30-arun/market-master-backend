
from rest_framework import serializers
from .models import *

class TemplateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Templates
        fields = "__all__"
        read_only_fields = ['id', 'image', 'title', 'description']
        
# ======================================================================================

class UserTemplateSerializer(serializers.ModelSerializer):
    template = TemplateSerializer()


    class Meta:
        model = UserTemplate
        fields = ['id', 'user', 'image', 'template', "title", "description", 'created_at', 'updated_at', 'time_since_updated', "ecommerce"]
        read_only_fields = ['id', 'created_at', 'updated_at', 'time_since_updated']
        
        
class PostUserTemplateSerializer(serializers.ModelSerializer):
	template = serializers.PrimaryKeyRelatedField(queryset=Templates.objects.all())

	class Meta:
		model = UserTemplate
		fields = ['id', 'user', 'template', 'created_at', 'updated_at', 'time_since_updated']
		read_only_fields = ['id', 'created_at', 'updated_at', 'time_since_updated']

class EditorUserTemplateSerializer(serializers.ModelSerializer):
    time_since_updated = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserTemplate
        fields =  "__all__"
        read_only_fields = ['id', 'user', 'template', 'created_at', 'updated_at']
        
    def get_time_since_updated(self, obj):
        return obj.time_since_updated()
    
  
  
#   ['id', 'user', 'template', 'html_content', 'css_cotent', 'js_content']
class QrcodeSerializer(serializers.ModelSerializer):
	class Meta:
		model = QrCodeHistory
		fields = ['id', 'user', 'name', 'url', 'time_since_updated']
		read_only_fields = ['id', 'time_since_updated', 'created_at']


class GetStartedSerializer(serializers.ModelSerializer):
    class Meta:
        model = GetStarted
        fields = '__all__'
        
        
class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
class AppointmentSerializer(serializers.ModelSerializer):
    time_since_updated = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Appointment
        fields = '__all__'
        
    def get_time_since_updated(self, obj):
        return obj.time_since_updated()


class BookingSerializer(serializers.ModelSerializer):
    time_since_updated = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Booking
        fields = '__all__'
        
    def get_time_since_updated(self, obj):
        return obj.time_since_updated()
        
class AvailableTimeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = AvailableTime
        fields = '__all__'