# Crie um arquivo, por exemplo, "middleware.py" no seu projeto
import re
from django.conf import settings
from django.shortcuts import redirect

class LoginRequiredMiddleware:
    """
    Middleware que exige que o usuário esteja autenticado para acessar
    todas as URLs, exceto aquelas explicitamente definidas como públicas.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        # Defina os caminhos que não exigem autenticação
        self.public_paths = [
            re.compile(settings.LOGIN_URL.lstrip('/')),
            re.compile(r'^static/'),  # por exemplo, arquivos estáticos
            # Adicione outras URLs públicas conforme necessário
        ]

    def __call__(self, request):
        # Se o usuário não estiver autenticado, verifique se a URL é pública
        if not request.user.is_authenticated:
            path = request.path_info.lstrip('/')
            if not any(pattern.match(path) for pattern in self.public_paths):
                return redirect(settings.LOGIN_URL)
        response = self.get_response(request)
        return response
