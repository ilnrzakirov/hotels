from django.db import models

class Profile(models.Model):
    extr_id = models.PositiveIntegerField(
        verbose_name='User ID'
    )
    name = models.TextField(
        verbose_name='User name'
    )
    city = models.TextField(
        verbose_name='Location',
        default='None',
    )
    def __str__(self):
        return  f'{self.extr_id} {self.name}'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'

class Message(models.Model):
    profile = models.ForeignKey(
        to = 'hotelapp.Profile',
        verbose_name='Profile',
        on_delete=models.PROTECT,
    )
    text = models.TextField(
        verbose_name='Text',
    )
    created_at = models.DateTimeField(
        verbose_name='Time of receipt',
        auto_now_add=True
    )

    def __str__(self):
        return f'Message {self.pk} от {self.profile}'

    class Meta:
        verbose_name = 'Message',
        verbose_name_plural = 'Messages'