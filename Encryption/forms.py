from django import forms
# from django.forms import ModelForm
# from .models import EnCrypt


CRYPT_CHOICES = (
    ("encrypt", "Зашифровать"),
    ("decrypt", "Расшифровать"),
)

CRYPT_ALGO_CHOICES = (
    ("caesar", "Шифр Цезаря"),
    ("permutation", "Перестановочный шифр"),
    ("polybius", "Квадрат Полибия"),
    ("playfair", "Квадрат Плейфера"),
    ("gamming", "Гаммирование"),
    ("RSA", "Шифр RSA"),
    ("Diffie-Hellman", "Алгоритм Диффи-Хеллмана"),
)


class EnCryptForm(forms.Form):
    text = forms.CharField(required=False, widget=forms.Textarea(attrs={"class": "text",
                                                                        "placeholder": "Текст или файл"}))
    key = forms.CharField(widget=forms.Textarea(attrs={"class": "key",
                                                        "placeholder": "🔑"}))
    action = forms.ChoiceField(widget=forms.RadioSelect(attrs={"class": "action"}), choices=CRYPT_CHOICES)
    algorithm = forms.ChoiceField(widget=forms.Select(attrs={"class": "algorithm"}), choices=CRYPT_ALGO_CHOICES)
    file = forms.FileField(required=False)

    class Meta:
        # model = EnCrypt
        fields = ['text', 'key', 'file', 'algorithm', 'action']
