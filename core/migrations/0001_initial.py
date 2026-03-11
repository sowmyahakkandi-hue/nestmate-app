from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in format: '+999999999'. Up to 15 digits.", regex='^\\+?1?\\d{9,15}$')])),
                ('course', models.CharField(choices=[('undergraduate', 'Undergraduate'), ('postgraduate', 'Postgraduate'), ('phd', 'PhD'), ('exchange', 'Exchange Student')], default='undergraduate', max_length=20)),
                ('college', models.CharField(max_length=100)),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='auth.user')),
            ],
        ),
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=1000)),
                ('property_type', models.CharField(choices=[('room', 'Single Room'), ('shared', 'Shared Room'), ('studio', 'Studio Apartment'), ('apartment', 'Full Apartment')], default='room', max_length=20)),
                ('address', models.CharField(max_length=300)),
                ('city', models.CharField(max_length=100)),
                ('rent_per_month', models.DecimalField(decimal_places=2, max_digits=8, validators=[django.core.validators.MinValueValidator(0.01)])),
                ('available_from', models.DateField()),
                ('bedrooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('bathrooms', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(10)])),
                ('max_occupants', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(20)])),
                ('pets_allowed', models.BooleanField(default=False)),
                ('smoking_allowed', models.BooleanField(default=False)),
                ('wifi_included', models.BooleanField(default=False)),
                ('bills_included', models.BooleanField(default=False)),
                ('status', models.CharField(choices=[('available', 'Available'), ('pending', 'Pending'), ('taken', 'Taken')], default='available', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='listings', to='auth.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='RoommateRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=500)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('withdrawn', 'Withdrawn')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests', to='core.listing')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_requests', to='auth.user')),
            ],
            options={'ordering': ['-created_at'], 'unique_together': {('listing', 'sender')}},
        ),
    ]
