# Check if the user logged in is a Staff member.
# Used to display add book and author choices in base.html when logged in.
def staff_status(request):
    return {
        'is_staff': request.user.is_staff
    }
