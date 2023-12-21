from django.db import models
from django.core import validators
from item.constants import MAX_LENGTH_ITEM, MIN_VALUE_PRICE, MAX_VALUE_PRICE


class Item(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=MAX_LENGTH_ITEM,
        unique=True,
    )
    description = models.TextField(
        verbose_name='Описание',
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        validators=[
            validators.MinValueValidator(
                limit_value=MIN_VALUE_PRICE,
                message='Значение должно быть больше 1.',
            ),
            validators.MaxValueValidator(
                limit_value=MAX_VALUE_PRICE,
                message='Значение должно быть меньше 2147483647.',
                )
        ]
    )

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'
        ordering = ('name',)
        constraints = [
            models.UniqueConstraint(
                fields=('name', 'description'),
                name='unique_name_description'
            )
        ]

    def __str__(self) -> str:
        return self.name
