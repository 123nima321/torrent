from django.db import models


class Game(models.Model):
    PLATFORM_CHOICES = [
        ('PC', 'PC'),
        ('PS', 'PlayStation'),
        ('Xbox', 'Xbox'),
        ('Switch', 'Nintendo Switch'),
        ('Mobile', 'Mobile'),
    ]
    
    CATEGORY_CHOICES = [
        ('Action', 'Action'),
        ('RPG', 'RPG'),
        ('Strategy', 'Strategy'),
        ('Adventure', 'Adventure'),
        ('Sports', 'Sports'),
        ('Racing', 'Racing'),
        ('Puzzle', 'Puzzle'),
        ('Simulation', 'Simulation'),
        ('Horror', 'Horror'),
        ('MMO', 'MMO'),
    ]

    name = models.CharField(max_length=200, verbose_name="Название игры")
    image = models.ImageField(upload_to='games/', verbose_name="Изображение")
    description = models.TextField(verbose_name="Описание")
    memory = models.FloatField(verbose_name="Размер памяти (ГБ)")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, verbose_name="Платформа")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    class Meta:
        verbose_name = "Игра"
        verbose_name_plural = "Игры"
        ordering = ['-created_at']

    def __str__(self):
        return self.name
