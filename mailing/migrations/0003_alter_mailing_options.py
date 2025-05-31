

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_mailing_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mailing',
            options={'ordering': ['-first_send_time'], 'permissions': [('can_view_all_mailings', 'Can view all mailings (for managers)'), ('can_deactivate_mailings', 'Can deactivate/pause mailings (for managers)')], 'verbose_name': 'Рассылка', 'verbose_name_plural': 'Рассылки'},
        ),
    ]
