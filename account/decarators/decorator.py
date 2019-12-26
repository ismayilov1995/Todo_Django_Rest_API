from django.shortcuts import HttpResponseRedirect, reverse

def anonymous_required(func):
    def wrap(request, *arg, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("mainPage"))
        return func(request, *arg, **kwargs)

    return wrap
