# Generated by Django 5.1.7 on 2025-04-27 22:19

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('users', '0011_alter_userprofile_available_credits'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='has_logged_in',
            field=models.BooleanField(default=False, help_text='Tracks if the user has logged in at least once.'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='purpose',
            field=models.CharField(blank=True, choices=[('pitch', 'Pitch'), ('present', 'Present'),
                                                        ('speak_storytelling', 'Speak/Storytelling'),
                                                        ('interview', 'Interview')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_intent',
            field=models.CharField(blank=True,
                                   choices=[('early', 'Early Career Professional'), ('mid', 'Mid-level Professionals'),
                                            ('sales', 'Sales Professionals'), ('c_suite', 'C-suites'),
                                            ('entrepreneur', 'Entrepreneurs'),
                                            ('athlete', 'Major League Sports Athlete'),
                                            ('executive', 'Major League Sports Executive')],
                                   help_text='Select your career/intention level at sign up.', max_length=50,
                                   null=True),
        ),
    ]
