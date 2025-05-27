# catalog/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from catalog.models import Product # Импортируем модель Product

class Command(BaseCommand):
    help = 'Creates default user groups and assigns permissions.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creating default groups...'))

        # Группа "Модератор продуктов"
        moderator_group, created = Group.objects.get_or_create(name='Модератор продуктов')
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Модератор продуктов" created.'))
        else:
            self.stdout.write(self.style.WARNING('Group "Модератор продуктов" already exists.'))

        # Получаем ContentType для модели Product
        product_content_type = ContentType.objects.get_for_model(Product)

        # Получаем разрешение на отмену публикации продукта (can_unpublish_product)
        try:
            can_unpublish_product_perm = Permission.objects.get(
                content_type=product_content_type,
                codename='can_unpublish_product'
            )
            moderator_group.permissions.add(can_unpublish_product_perm)
            self.stdout.write(self.style.SUCCESS('Permission "can_unpublish_product" assigned to "Модератор продуктов".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "can_unpublish_product" not found. Make sure you ran makemigrations/migrate for catalog app.'))

        # Получаем разрешение на удаление любого продукта (standard Django permission: delete_product)
        try:
            delete_product_perm = Permission.objects.get(
                content_type=product_content_type,
                codename='delete_product'
            )
            moderator_group.permissions.add(delete_product_perm)
            self.stdout.write(self.style.SUCCESS('Permission "delete_product" assigned to "Модератор продуктов".'))
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('Permission "delete_product" not found. Make sure you ran makemigrations/migrate for catalog app.'))


        # Группа "Контент-менеджер" (для дополнительного задания, но мы ее тоже создаем)
        content_manager_group, created = Group.objects.get_or_create(name='Контент-менеджер')
        if created:
            self.stdout.write(self.style.SUCCESS('Group "Контент-менеджер" created.'))
        else:
            self.stdout.write(self.style.WARNING('Group "Контент-менеджер" already exists.'))

        self.stdout.write(self.style.SUCCESS('Default groups creation finished.'))