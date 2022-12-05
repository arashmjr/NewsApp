from django.urls import include, path

accounts_url_patterns = []


V_0_0_0_urlpatterns = [
    path("accounts/", include(accounts_url_patterns)),
]

urlpatterns = [
    path("V0.0.0/", include(V_0_0_0_urlpatterns)),
]
