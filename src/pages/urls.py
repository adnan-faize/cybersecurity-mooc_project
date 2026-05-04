from django.urls import path
from views import (
    add_note,
    api_get_record,
    dashboard,
    export_data,
    home,
    login_view,
    logout_view,
    register_view,
    search_records,
    update_patient_info,
    view_patient_data,
)

urlpatterns = [
    path("", home, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard, name="dashboard"),
    path("patient/<str:patient_id>/", view_patient_data, name="patient_data"),
    path("search/", search_records, name="search_records"),
    path("add-note/", add_note, name="add_note"),
    path("update-info/", update_patient_info, name="update_info"),
    path("export/", export_data, name="export_data"),
    path("api/record/<int:record_id>/", api_get_record, name="api_get_record"),
]
