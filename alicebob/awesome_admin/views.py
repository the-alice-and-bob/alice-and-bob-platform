# -------------------------------------------------------------------------
#
# Custom admin views
#
# -------------------------------------------------------------------------
from academy.models import Student


# -------------------------------------------------------------------------
# Students
# -------------------------------------------------------------------------

def students_leads(request):
    """
    Callback for the leads in the sidebar.
    """
    students = Student.objects.filter(is_lead=True)
    return {
        "title": "Leads",
        "icon": "fa fa-users",
        "url": "/academy/students/leads/",
        "count": students.count(),
        "color": "info"
    }
