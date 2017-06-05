# Create your views here.

import redis

from django.contrib.sites.models import Site

from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, get_backends
try:
    from django.contrib.sites.models import get_current_site
except ImportError:
    from django.contrib.sites.shortcuts import get_current_site
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User

from django.conf import settings

from .utils import generate_random_string, salted_hash
from .qr import make_qr_code

AUTH_QR_CODE_EXPIRATION_TIME = getattr(
    settings,
    "AUTH_QR_CODE_EXPIRATION_TIME",
    300
)

AUTH_QR_CODE_REDIRECT_URL = getattr(
    settings,
    "AUTH_QR_CODE_REDIRECT_URL",
    "/"
)

AUTH_QR_CODE_REDIS_KWARGS = getattr(
    settings,
    "AUTH_QR_CODE_REDIS_KWARGS",
    {}
)

def uses_redis(func):
    def wrapper(*args, **kwargs):
        kwargs["r"] = redis.StrictRedis(**AUTH_QR_CODE_REDIS_KWARGS)
        return func(*args, **kwargs)

    return wrapper

@login_required
@uses_redis
def qr_code_page(request, r=None):
    auth_code = generate_random_string(50)
    auth_code = auth_code.strip()
    auth_code_hash = salted_hash(auth_code)
    auth_code_hash = auth_code_hash.strip()

    key = "".join(["qrauth_", auth_code_hash])
    r.setex(
        key,
        AUTH_QR_CODE_EXPIRATION_TIME,
        request.user.id
    )

    return render(request, "qrauth/page.html",
                              {"auth_code": auth_code})

@login_required
@uses_redis
def qr_code_picture(request, auth_code, r=None):
    auth_code = auth_code.strip()
    auth_code_hash = salted_hash(auth_code)
    auth_code_hash = auth_code_hash.strip()

    key = "".join(["qrauth_", auth_code_hash])
    user_id = r.get(key)

    if (user_id == None) or (int(user_id.decode(), 10) != request.user.id):
        raise Http404("No such auth code")

    #current_site = get_current_site(request)
    #current_site = Site.objects.get_current()
    current_site = request.get_host()
    print("Current site 25", request.get_host())
    scheme = request.is_secure() and "https" or "http"

    login_link = "".join([
        scheme,
        "://",
        current_site,
        reverse("qr_code_login", args=(auth_code_hash,)),
    ])

    img = make_qr_code(login_link)
    response = HttpResponse(content_type="image/png")
    img.save(response, "PNG")
    return response

@uses_redis
def login_view(request, auth_code_hash, r=None):
    redis_key = "".join(["qrauth_", auth_code_hash])

    user_id = r.get(redis_key)

    if user_id == None:
        return HttpResponseRedirect(reverse("invalid_auth_code"))

    r.delete(redis_key)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return HttpResponseRedirect(reverse("invalid_auth_code"))

    # In lieu of a call to authenticate()
    backend = get_backends()[0]
    user.backend = "%s.%s" % (backend.__module__, backend.__class__.__name__)
    login(request, user)

    return HttpResponseRedirect(AUTH_QR_CODE_REDIRECT_URL)
