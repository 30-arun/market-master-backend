from django.conf import settings
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import *
from rest_framework.views import APIView
from .models import *
from .serializers import *
import stripe
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from rest_framework.exceptions import NotFound

stripe.api_key = settings.STRIPE_SECRET_KEY
User = get_user_model()

    
class AllTemplateView(APIView):
    
    def get(self, request, format=None):
        templates = Templates.objects.all()
        serializer = TemplateSerializer(templates, many=True)
        return Response(serializer.data)
    
class GetTemplateView(APIView):
    	
	def get(self, request, template_id, format=None):
		templates = Templates.objects.filter(id=template_id).first()
		serializer = TemplateSerializer(templates)
		return Response(serializer.data, status=status.HTTP_200_OK)

class UserTemplateView(APIView):
    	
	def get(self, request, user_id, format=None):
		templates = UserTemplate.objects.filter(user_id=user_id)
		serializer = UserTemplateSerializer(templates, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)


class UserTemplateDetailView(APIView):
	def get(self, request, user_id, user_template_id, format=None):
		templates = Templates.objects.filter(user_templates__user=user_id, user_templates__id=user_template_id).first()
		serializer = TemplateSerializer(templates)
		return Response(serializer.data, status=status.HTTP_200_OK)

	def put(self, request, user_id, user_template_id, format=None):
		try:
			user_template = UserTemplate.objects.get(pk=user_id, user=user_template_id)
		except UserTemplate.DoesNotExist:
			return Response({"error": "UserTemplate not found"}, status=status.HTTP_404_NOT_FOUND)

		template = user_template.template
		serializer = TemplateSerializer(template, data=request.data, partial=True)
		
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, user_id, user_template_id, format=None):
		template = UserTemplate.objects.filter(user=user_id, id=user_template_id)
		template.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class PostUserTemplateView(APIView):
	def post(self, request, format=None):
		serializer = PostUserTemplateSerializer(data=request.data)
		# if user and template already added then do not create new, instead return error
		# if UserTemplate.objects.filter(user=request.data['user'], template=request.data['template']).exists():
		# 	return Response({"error": "UserTemplate already exists"}, status=status.HTTP_400_BAD_REQUEST)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.exceptions import PermissionDenied


class EditorUserTemplateDetailView(APIView):
    
    def get_object(self, temp_id, user_id):
        try:
            return UserTemplate.objects.get(pk=temp_id, user_id=user_id)
        except UserTemplate.DoesNotExist:
            raise Http404

    def get(self, request, user_id, temp_id, format=None):
        user_template = self.get_object(temp_id, user_id)
        serializer = EditorUserTemplateSerializer(user_template)
        return Response(serializer.data)

    def put(self, request, user_id, temp_id, format=None):
        user_template = self.get_object(temp_id, user_id)
        serializer = EditorUserTemplateSerializer(user_template, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QrcodeView(APIView):
    
	def get(self, request, format=None):
		user_id = request.GET.get('user_id')
		qrcodes = QrCodeHistory.objects.filter(user_id=user_id)
		serializer = QrcodeSerializer(qrcodes, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = QrcodeSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		user_id = request.GET.get('user_id')
		qrcode_id = request.GET.get('qrcode_id')
		qrcodes = QrCodeHistory.objects.filter(user_id=user_id, id=qrcode_id)
		qrcodes.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class GetStartedViewSet(APIView):
    def get(self, request, format=None):
        user_id = request.GET.get('user_id')
        get_started_objects = GetStarted.objects.filter(user_id=user_id)
        serializer = GetStartedSerializer(get_started_objects, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = GetStartedSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ContactView(APIView):
    	
	def get(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		contacts = Contact.objects.filter(user_template_id=user_template_id)
		serializer = ContactSerializer(contacts, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = ContactSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		contact_id = request.GET.get('contact_id')
		contacts = Contact.objects.filter(user_template_id=user_template_id, id=contact_id)
		contacts.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class AppointmentView(APIView):
    		
	def get(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		appointments = Appointment.objects.filter(user_template_id=user_template_id)
		serializer = AppointmentSerializer(appointments, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = AppointmentSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		appointment_id = request.GET.get('appointment_id')
		appointments = Appointment.objects.filter(user_template_id=user_template_id, id=appointment_id)
		appointments.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class BookingView(APIView):
    	
	def get(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		bookings = Booking.objects.filter(user_template_id=user_template_id)
		serializer = BookingSerializer(bookings, many=True)
		return Response(serializer.data)
	
	def post(self, request, format=None):
		serializer = BookingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	
	def delete(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		booking_id = request.GET.get('booking_id')
		bookings = Booking.objects.filter(user_template_id=user_template_id, id=booking_id)
		bookings.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class AvailableTimeView(APIView):
	def get(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		available_times = AvailableTime.objects.filter(user_template_id=user_template_id)
		serializer = AvailableTimeSerializer(available_times, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = AvailableTimeSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, format=None):
		user_template_id = request.GET.get('template_id')
		available_time_id = request.GET.get('available_time_id')
		available_times = AvailableTime.objects.filter(user_template_id=user_template_id, id=available_time_id)
		available_times.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

class ContactRepliedView(APIView):
    def post(self, request, format=None):
        contact_id = request.data.get('contact_id')
        replied_message = request.data.get('replied_message')
        if not contact_id or not replied_message:
            return Response({"error": "Missing contact_id or replied_message."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            contact = Contact.objects.get(id=contact_id)
        except Contact.DoesNotExist:
            raise NotFound(detail="Contact not found.")
        self.send_replied_email(contact, replied_message)
        contact.replied = True
        contact.replied_message = replied_message
        contact.save()
        return Response({"message": "Replied status updated and email sent."}, status=status.HTTP_200_OK)
    
    def send_replied_email(self, contact, replied_message):
        subject = 'Market Master Contact Replied'
        message = replied_message
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [contact.email]
        send_mail(subject, message, from_email, recipient_list)