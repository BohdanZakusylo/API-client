from django.http import HttpResponse, HttpRequest


def set_access_token(response: HttpResponse, token: str):
    response.set_cookie("access_token", token, httponly=True)


def set_refresh_token(response: HttpResponse, token: str):
    response.set_cookie("refresh_token", token, httponly=True)


def get_tokens(request: HttpRequest) -> tuple:
    access_token = request.COOKIES.get("access_token")
    refresh_token = request.COOKIES.get("refresh_token")
    return access_token, refresh_token
