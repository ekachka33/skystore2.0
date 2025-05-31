# mailing/management/commands/send_mailing.py

from django.core.management.base import BaseCommand, CommandError
from django.shortcuts import get_object_or_404
from mailing.models import Mailing # Импортируем модель рассылки
from mailing.services import send_single_mailing # Импортируем нашу сервисную функцию отправки
from django.utils import timezone

class Command(BaseCommand):
    help = 'Sends a specific mailing by its ID.'

    def add_arguments(self, parser):

        parser.add_argument('mailing_id', type=int, help='The ID of the mailing to send.')

    def handle(self, *args, **options):
        mailing_id = options['mailing_id']
        self.stdout.write(self.style.SUCCESS(f'Attempting to send mailing with ID: {mailing_id}'))

        try:
            mailing = get_object_or_404(Mailing, pk=mailing_id)
        except Exception as e:
            raise CommandError(f'Mailing with ID "{mailing_id}" does not exist. Error: {e}')

        if mailing.status == Mailing.STATUS_COMPLETED:
            raise CommandError(f'Mailing with ID "{mailing_id}" is already completed and cannot be sent.')

        if timezone.now() >= mailing.end_time:
            raise CommandError(f'Mailing with ID "{mailing_id}" cannot be sent, as its end time has already passed.')

        successful_sends, failed_sends = send_single_mailing(mailing)

        self.stdout.write(self.style.SUCCESS(f'Mailing ID {mailing_id} finished processing.'))
        self.stdout.write(self.style.SUCCESS(f'Successfully sent to: {successful_sends} recipients.'))
        if failed_sends > 0:
            self.stdout.write(self.style.WARNING(f'Failed to send to: {failed_sends} recipients.'))
        self.stdout.write(self.style.SUCCESS('Check mailing attempts in Django admin for details.'))