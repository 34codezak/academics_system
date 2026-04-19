from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.students.models import Student
#from apps.grading.models import Submission
#from apps.notifications.models import Notification

@login_required
def dashboard_view(request):
    context = {
        'total_students': Student.objects.count(),
        'active_courses': 12,  # Replace with actual query
 #       'pending_grades': Submission.objects.filter(graded=False).count(),
  #      'unread_count': Notification.objects.filter(user=request.user, read=False).count(),
  #      'notifications': Notification.objects.filter(user=request.user).order_by('-created_at'),
 #       'pending_submissions': Submission.objects.filter(graded=False).select_related('student', 'assignment', 'course').order_by('submitted_at'),
    }
    return render(request, 'dashboard/dashboard.html', context)