# mailing/services.py

from django.core.cache import cache
from django.core.mail import send_mail
from django.conf import settings
from .models import Mailing, MailingAttempt, Client
from django.utils import timezone


from catalog.models import Product, Category

def get_products_by_category(category_pk):
    """
    Сервисная функция, возвращающая список продуктов по указанной категории.
    Использует низкоуровневое кеширование.
    """

    if not category_pk:

        return Product.objects.all()

    cache_key = f'products_by_category_{category_pk}'
    products = cache.get(cache_key)

    if products is None:
        try:
            category = Category.objects.get(pk=category_pk)
            products = Product.objects.filter(category=category)
            cache.set(cache_key, products, 300)
            print(f"DEBUG: Products for category {category_pk} fetched from DB and cached.")
        except Category.DoesNotExist:
            products = Product.objects.none()
            print(f"DEBUG: Category {category_pk} not found. Returning empty queryset.")
    else:
        print(f"DEBUG: Products for category {category_pk} fetched from cache.")

    return products



def send_single_mailing(mailing_object):
    """
    Отправляет рассылку для указанного объекта Mailing и логирует попытки.
    Добавлена детальная диагностика.
    """
    total_recipients = mailing_object.recipients.count()
    successful_sends = 0
    failed_sends = 0

    print(f"\n--- DEBUG: Starting send for Mailing ID: {mailing_object.pk} ---")
    print(f"DEBUG: Mailing status before send: {mailing_object.status}")
    print(f"DEBUG: Message Subject: {mailing_object.message.subject}")
    print(f"DEBUG: From Email: {settings.EMAIL_HOST_USER}")



    for recipient in mailing_object.recipients.all():
        try:
            recipient_email = recipient.email
            print(f"DEBUG: Attempting to send to: {recipient_email}")


            num_sent = send_mail(
                subject=mailing_object.message.subject,
                message=mailing_object.message.body,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[recipient_email],
                fail_silently=False,
            )


            if num_sent == 1:
                MailingAttempt.objects.create(
                    mailing=mailing_object,
                    status=MailingAttempt.STATUS_SUCCESS,
                    server_response='Email sent successfully.'
                )
                successful_sends += 1
                print(f"DEBUG: Successfully sent email to {recipient_email}. Num sent: {num_sent}")
            else:

                MailingAttempt.objects.create(
                    mailing=mailing_object,
                    status=MailingAttempt.STATUS_FAILED,
                    server_response='Email did not send, but no exception was raised (num_sent was 0). This is unexpected with fail_silently=False.'
                )
                failed_sends += 1
                print(f"DEBUG: send_mail returned 0 for {recipient_email}.")

        except Exception as e:

            MailingAttempt.objects.create(
                mailing=mailing_object,
                status=MailingAttempt.STATUS_FAILED,
                server_response=f"Error sending to {recipient_email}: {str(e)}"
            )
            failed_sends += 1
            print(f"DEBUG: Failed to send email to {recipient_email}: {e}")

    print(
        f"--- DEBUG: Mailing ID {mailing_object.pk} completed. Total sent: {successful_sends}, Total failed: {failed_sends} ---")
    print("-" * 50)



    return successful_sends, failed_sends