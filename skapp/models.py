from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import validate_unicode_slug
from django.utils.timezone import now


def validate_gt(value):
    if value < 1000:
        raise ValidationError(
            ("%(value)s is not greater than 1000"),
            params={"value": value},
        )


class Sk(models.Model):
    sk_id = models.IntegerField(primary_key=True, validators=[validate_gt])
    summary = models.TextField(blank=False)
    keytakeaways = models.TextField(blank=False)
    filename = models.CharField(max_length=100, blank=False)
    inputfile = models.FileField(upload_to='input_files/', null=True)
    datetime = models.DateTimeField(auto_now_add=True)
    # publish = models.BooleanField(default=False)


    def save(self, *args, **kwargs):
        if self.sk_id is None:

            last_id = Sk.objects.aggregate(models.Max('sk_id'))['sk_id__max']
            self.sk_id = (last_id or 999) + 1 

            validate_gt(self.sk_id)

        super(Sk, self).save(*args, **kwargs)