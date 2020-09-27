from django.db import models
from twilio.rest import Client

# Create your models here.

class Score(models.Model):
    result = models.PositiveIntegerField()

    def __str__(self):
        return str(self.result)

    def save(self, *args, **kwargs):
        if self.result < 70:
            account_sid = 'AC546670f460126b5f8f3e38abd463318f'
            auth_token = 'f0508a7e323e5db606deb914b9a42ae7'
            client = Client(account_sid, auth_token)

            message = client.messages \
                .create(
                body=f"The current result is bad - {self.result}",
                from_='+12056569196',
                to='+91 8850422367'
            )

            print(message.sid)
        return super().save(*args, **kwargs)

