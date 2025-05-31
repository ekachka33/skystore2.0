# catalog/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product # Импортируем модель Product
from mailing.models import Mailing, Client # <--- ОБЯЗАТЕЛЬНО ИМПОРТИРУЙ Mailing И Client


class Command(BaseCommand):
    help = 'Creates default user groups and assigns permissions.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating default groups...'))

        # --- Создание/проверка группы "Модератор продуктов" (и менеджер рассылок) ---
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Модератор продуктов" created.'))
        else:
            self.stdout.write(self.style.SUCCESS('Group "Модератор продуктов" already exists.'))

        # Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)

        # Назначаем разрешения для модератора продуктов
        # can_unpublish_product
        try:
            can_unpublish_product_perm = Permission.objects.get(
                content_type=product_content_type,
                codename='can_unpublish_product'
            )
            moderator_group.permissions.add(can_unpublish_product_perm)
            self.stdout.write(self.style.SUCCESS('Permission "can_unpublish_product" assigned to "Модератор продуктов".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "can_unpublish_product" not found. Make sure you ran makemigrations/migrate for catalog app.'))

        # delete_product
        try:
            delete_product_perm = Permission.objects.get(
                content_type=product_content_type,
                codename='delete_product'
            )
            moderator_group.permissions.add(delete_product_perm)
            self.stdout.write(self.style.SUCCESS('Permission "delete_product" assigned to "Модератор продуктов".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "delete_product" not found. Make sure you ran makemigrations/migrate for catalog app.'))


        # --- НАЗНАЧЕНИЕ РАЗРЕШЕНИЙ ДЛЯ УПРАВЛЕНИЯ РАССЫЛКАМИ (МОДЕРАТОРАМ/МЕНЕДЖЕРАМ) ---
        mailing_content_type = ContentType.objects.get_for_model(Mailing)
        client_content_type = ContentType.objects.get_for_model(Client) # Необходимо для Client

        # can_view_all_mailings (просмотр всех рассылок и клиентов)
        try:
            can_view_all_mailings_perm = Permission.objects.get(
                content_type=mailing_content_type,
                codename='can_view_all_mailings'
            )
            moderator_group.permissions.add(can_view_all_mailings_perm)
            self.stdout.write(self.style.SUCCESS('Permission "can_view_all_mailings" assigned to "Модератор продуктов".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "can_view_all_mailings" not found. Make sure you ran makemigrations/migrate for mailing app.'))

        # can_deactivate_mailings (отключение/включение рассылок)
        try:
            can_deactivate_mailings_perm = Permission.objects.get(
                content_type=mailing_content_type,
                codename='can_deactivate_mailings'
            )
            moderator_group.permissions.add(can_deactivate_mailings_perm)
            self.stdout.write(self.style.SUCCESS('Permission "can_deactivate_mailings" assigned to "Модератор продуктов".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "can_deactivate_mailings" not found. Make sure you ran makemigrations/migrate for mailing app.'))

        # --- Дополнительные права для Модератора продуктов, если нужны ---
        # Например, если модератор продуктов должен видеть всех клиентов:
        try:
            view_client_perm = Permission.objects.get(
                content_type=client_content_type,
                codename='view_client' # Стандартное разрешение Django на просмотр
            )
            moderator_group.permissions.add(view_client_perm)
            self.stdout.write(self.style.SUCCESS('Permission "view_client" assigned to "Модератор продуктов".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "view_client" not found. Make sure you ran makemigrations/migrate for mailing app.'))


        # --- Создание/проверка группы "Контент-менеджер" ---
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Контент-менеджер" created.'))
        else:
            self.stdout.write(self.style.SUCCESS('Group "Контент-менеджер" already exists.'))

        # Получаем стандартные разрешения Django
        # add_product
        try:
            add_product_perm = Permission.objects.get(
                content_type=product_content_type,
                codename='add_product'
            )
            content_manager_group.permissions.add(add_product_perm)
            self.stdout.write(self.style.SUCCESS('Permission "add_product" assigned to "Контент-менеджер".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "add_product" not found. Make sure you ran makemigrations/migrate for catalog app.'))

        # change_product (для редактирования своих продуктов)
        try:
            change_product_perm = Permission.objects.get(
                content_type=product_content_type,
                codename='change_product'
            )
            content_manager_group.permissions.add(change_product_perm)
            self.stdout.write(self.style.SUCCESS('Permission "change_product" assigned to "Контент-менеджер".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "change_product" not found. Make sure you ran makemigrations/migrate for catalog app.'))


        self.stdout.write(self.style.SUCCESS('Default groups creation finished.'))