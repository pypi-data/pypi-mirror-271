# views.py
from numbers import Number
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.communication.app_tasks.notification_task import send_notification_task
from apps.communication.app_tasks.sms_task import check_verify_token_task, send_sms_notification_task, send_verify_token_task
from ....app_tasks.email_task import send_email_notification_task
from ....app_models.models import emailNotification,mobileNotification,smsNotification,STATUS_CHOICES ,SMS_TYPE_CHOICES
from apps.communication.app_models.interfaces.main_interface import db_add

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email_view(request):
    subject = request.data.get('subject')
    message = request.data.get('message')
    recipient_list = request.data.get('recipient_list', []) 
    return send_email(subject,message,recipient_list)

def send_email(subject,message,recipient_list):
    if subject and message and recipient_list:
        email_list= ",".join(recipient_list);
        email_record = db_add(emailNotification,recipient_emails=email_list,subject=subject,content=message,status= STATUS_CHOICES.CHOICE_PENDING)
        send_email_notification_task.delay(subject, message, recipient_list,email_record.id) # type: ignore
        return Response({'message': 'Email sent asynchronously'}, status=status.HTTP_200_OK)
    else:
        return Response({'message': 'subject and message and recipient_list are required'}, status=status.HTTP_400_BAD_REQUEST)

#=====================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_sms_view(request):
    recipient_number = request.data.get('recipient_number')
    message = request.data.get('message')
    return send_sms_view(message, recipient_number)

def send_sms(message,recipient_number):
    if recipient_number and message:
        sms_record = db_add(smsNotification, recipient_phone=recipient_number,type=SMS_TYPE_CHOICES.CHOICE_SMS, status=STATUS_CHOICES.CHOICE_PENDING)
        success, message_sid = send_sms_notification_task.delay(recipient_number, message,sms_record.id)
        if success:
            return Response({'message': 'SMS sent successfully', 'message_sid': message_sid}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to send SMS', 'error_message': message_sid}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Recipient number and message are required'}, status=status.HTTP_400_BAD_REQUEST)

#=====================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def send_notification_view(request):
    token = request.data.get('token')
    title = request.data.get('title')
    body = request.data.get('body')
    image_url = request.data.get('image_url') or None
    data = request.data.get('data') or None
    return send_notification(token, title, body,image_url,data)

def send_notification(token, title, body,image_url=None,data=None):
    if body and title and token:
        mobile_record = db_add(mobileNotification, recipient_fcmtoken=token,title=title,message_text=body,image_url=image_url,json_data=data, status=STATUS_CHOICES.CHOICE_PENDING)
        response = send_notification_task.delay(token, title, body,mobile_record.id,image_url,data)
        if response:
            return Response({'message': 'Notification sent successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to send Notification'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Recipient token and title and body are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#=====================================================================    

@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def send_verify_view(request):
    recipient_number = request.data.get('recipient_number')
    service_id = request.data.get('service_id') or settings.TWILIO_VERIFY_SID
    return send_verify(recipient_number, service_id)

def send_verify(recipient_number, service_id=settings.TWILIO_VERIFY_SID):
    if recipient_number and service_id:
        sms_record = db_add(smsNotification, recipient_phone=recipient_number,type=SMS_TYPE_CHOICES.CHOICE_VERIFY, status=STATUS_CHOICES.CHOICE_PENDING)
        success, message_sid = send_verify_token_task(recipient_number,sms_record.id,service_id)
        if success:
            return Response({'message': 'verify sent successfully', 'message_sid': message_sid}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to send verify', 'error_message': message_sid}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Recipient recipient_number and service_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#=====================================================================   
 
@api_view(['POST'])
@permission_classes([IsAuthenticated])    
def check_verify_view(request):
    recipient_number = request.data.get('recipient_number')
    code = request.data.get('code')
    service_id = request.data.get('service_id') or settings.TWILIO_VERIFY_SID
    return check_verify(recipient_number,code, service_id)

def check_verify(recipient_number,code, service_id=settings.TWILIO_VERIFY_SID):
    if recipient_number and code and service_id:
        success, message_status = check_verify_token_task(recipient_number,code,service_id)
        if success:
            return Response({'message': 'verify sent successfully', 'message_status': message_status}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Failed to send verify', 'message_status': message_status}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'message': 'Recipient recipient_number and code and service_id are required'}, status=status.HTTP_400_BAD_REQUEST)
    
#=====================================================================  

