from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


def sign_up(request):
    if request.method == 'POST':
        # Store the data from the POST request
        form = UserCreationForm(request.POST)

        # If the form is valid (eg. user's username is unique)
        if form.is_valid():
            # Save the user into the database
            user = form.save()
            login(request, user)

            return redirect('/dashboard/test/')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/sign_up.html', {'form': form})


@login_required
def profile(request):
    return render(request, '/redditsearch/dashboard.html')
