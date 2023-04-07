from django.shortcuts import render
from .forms import EnCryptForm
from .cryptoalgorithms import Crypt, GenerateKey
from django.utils.encoding import filepath_to_uri
from django.http import JsonResponse


def generate_rsa(request):
    values = GenerateKey.generate_rsa_keys_pem()
    return JsonResponse({"values": values})


def generate_diffie_hellman(request):
    value = GenerateKey.generate_diffie_hellman()
    return JsonResponse({"value": str(value)})


def encryption(request):
    if request.method == 'GET':
        return render(request, 'encryption/home.html', {'form': EnCryptForm()})
    elif request.method == 'POST':
        form = EnCryptForm(request.POST, request.FILES)
        if form.is_valid():
            text = form.cleaned_data.get("text")
            key = form.cleaned_data.get("key")
            action = form.cleaned_data.get("action")
            algorithm = form.cleaned_data.get("algorithm")
            if request.FILES:
                file = request.FILES['file']
            else:
                file = None
            result = Crypt(text, key, file, algorithm, action)
            uploaded_file_url = filepath_to_uri(result.file_result.name)
            return render(request, 'encryption/home.html', {'form': form,
                                                            'result': result.text_result,
                                                            'result_file': uploaded_file_url})
        else:
            return render(request, 'encryption/home.html', {'form': EnCryptForm()})
