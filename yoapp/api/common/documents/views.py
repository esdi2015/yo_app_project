from django.shortcuts import redirect, render


def terms_template_view(request):

    return render(request, 'documents/terms.html')