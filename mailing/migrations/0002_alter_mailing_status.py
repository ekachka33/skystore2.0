

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'Создана'), ('started', 'Запущена'), ('completed', 'Завершена'), ('paused', 'Приостановлена')], default='created', max_length=10, verbose_name='Статус рассылки'),
        ),
    ]
