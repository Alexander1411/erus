from django.db import models
from django.core.validators import RegexValidator

class Contact(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+7 \(([1-9]\d{2})\) \d{3}-\d{2}-\d{2}$',
        message="Номер телефона должен быть в формате: '+7 (XXX) XXX-XX-XX', где первая цифра кода от 1 до 9"
    )

    last_name = models.CharField('Фамилия', max_length=100, help_text='Введите фамилию')
    first_name = models.CharField('Имя', max_length=100, help_text='Введите имя')
    patronymic = models.CharField('Отчество', max_length=100, help_text='Введите отчество')
    email = models.EmailField('Email', help_text='Введите email адрес')
    phone = models.CharField(
        'Телефон',
        max_length=20,
        validators=[phone_regex],
        help_text='Введите номер телефона в формате +7 (XXX) XXX-XX-XX. Примеры: +7 (495) 123-45-67 (Москва), +7 (812) 123-45-67 (СПб), +7 (900) 123-45-67 (мобильный)'
    )
    subject = models.CharField('Тема', max_length=200, blank=True, help_text='Укажите тему сообщения')
    pain_duration = models.CharField('Продолжительность боли', max_length=50, blank=True)
    pain_locations = models.JSONField('Локализация боли', blank=True, null=True)
    pain_level = models.CharField('Уровень боли', max_length=10, blank=True)
    message = models.TextField('Сообщение', blank=True)
    patient_type = models.CharField(
        'Тип пациента', 
        max_length=20, 
        choices=[('self-paying', 'Платное лечение'), ('oms', 'ОМС')], 
        default='self-paying'
    )
    consent = models.BooleanField(
        'Согласие на обработку данных',
        default=False,
        help_text='Я согласен на обработку моих персональных данных'
    )
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)

    class Meta:
        verbose_name = 'Контактная форма'
        verbose_name_plural = 'Контактные формы'
        ordering = ['-created_at']

    def __str__(self):
        subject_text = self.subject if self.subject else 'Заявка'
        return f'{self.last_name} {self.first_name} - {subject_text}'

class ContactSubmission(models.Model):
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    patronymic = models.CharField(max_length=50, verbose_name='Отчество')
    contact_email = models.EmailField(verbose_name='Email')
    mobile = models.CharField(max_length=20, verbose_name='Телефон')
    pain_locations = models.JSONField(blank=True, null=True, verbose_name='Локализация боли')
    pain_duration = models.CharField(max_length=20, blank=True, null=True, verbose_name='Продолжительность боли')
    pain_level = models.CharField(max_length=10, blank=True, null=True, verbose_name='Уровень боли (1-10)')
    message = models.TextField(blank=True, null=True, verbose_name='Дополнительная информация')
    patient_type = models.CharField(
        verbose_name='Тип пациента', 
        max_length=20, 
        choices=[('self-paying', 'Платное лечение'), ('oms', 'ОМС')], 
        default='self-paying'
    )
    consent = models.BooleanField(default=False, verbose_name='Согласие на обработку данных')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Контактная заявка'
        verbose_name_plural = 'Контактные заявки'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.last_name} {self.first_name} - {self.created_at}' 