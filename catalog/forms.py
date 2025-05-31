from django import forms
from .models import Product
from django.core.exceptions import ValidationError

FORBIDDEN_WORDS = [
    'казино', 'криптовалюта', 'крипта',
    'биржа', 'дешево', 'бесплатно',
    'обман', 'полиция', 'радар'
]

def validate_image(image):
    if isinstance(image, str):
        raise ValidationError("Ошибка: ожидается объект файла, а не строка.")
    # Проверка формата
    if not (image.name.endswith('.png') or image.name.endswith('.jpg') or image.name.endswith('.jpeg')):
        raise ValidationError("Файл должен быть в формате JPEG или PNG.")
    # Проверка размера
    if image.size > 5 * 1024 * 1024:  # 5 МБ
        raise ValidationError("Файл слишком большой (максимум 5MB).")

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'image', 'category', 'price']

    def clean_name(self):
        name = self.cleaned_data.get('name')
        if any(word in name.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Имя продукта содержит запрещенные слова.")
        return name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if any(word in description.lower() for word in FORBIDDEN_WORDS):
            raise forms.ValidationError("Описание продукта содержит запрещенные слова.")
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price < 0:
            raise forms.ValidationError("Цена продукта не может быть отрицательной.")
        return price

    def clean_image(self):
        image = self.cleaned_data.get('image')
        # Если изображение не загружено, просто пропустим валидацию
        if not image or image == '':
            return image  # Вернем image, который может быть None или пустой строкой

        validate_image(image)  # Проверка формата и размера, если изображение загружено
        return image