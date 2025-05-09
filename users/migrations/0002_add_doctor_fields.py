from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='consultation_fee',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=10),
        ),
        migrations.AddField(
            model_name='doctor',
            name='rating',
            field=models.DecimalField(decimal_places=2, default=0.00, max_digits=3),
        ),
        migrations.AddField(
            model_name='doctor',
            name='total_ratings',
            field=models.IntegerField(default=0),
        ),
    ] 