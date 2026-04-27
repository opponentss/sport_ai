from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Checkin
from .forms import CheckinForm


@login_required
def checkin_list(request):
    checkins = Checkin.objects.filter(user=request.user).select_related('exercise_type').order_by('-created_at')
    total_calories = sum(c.calories_burned for c in checkins if c.calories_burned)
    return render(request, 'checkin/checkin_list.html', {
        'checkins': checkins,
        'total_calories': total_calories,
    })


@login_required
def checkin_create(request):
    if request.method == 'POST':
        form = CheckinForm(request.POST)
        if form.is_valid():
            checkin = form.save(commit=False)
            checkin.user = request.user
            if checkin.exercise_type and not checkin.calories_burned:
                checkin.calories_burned = int(checkin.duration * checkin.exercise_type.calories_per_minute)
            if not checkin.activity and checkin.exercise_type:
                checkin.activity = checkin.exercise_type.name
            checkin.save()
            return redirect('checkin_list')
    else:
        form = CheckinForm()
    return render(request, 'checkin/checkin_form.html', {'form': form})


@login_required
def checkin_update(request, pk):
    checkin = get_object_or_404(Checkin, pk=pk, user=request.user)
    if request.method == 'POST':
        form = CheckinForm(request.POST, instance=checkin)
        if form.is_valid():
            checkin = form.save(commit=False)
            if checkin.exercise_type and not checkin.calories_burned:
                checkin.calories_burned = int(checkin.duration * checkin.exercise_type.calories_per_minute)
            checkin.save()
            return redirect('checkin_list')
    else:
        form = CheckinForm(instance=checkin)
    return render(request, 'checkin/checkin_form.html', {'form': form})


@login_required
def checkin_delete(request, pk):
    checkin = get_object_or_404(Checkin, pk=pk, user=request.user)
    if request.method == 'POST':
        checkin.delete()
        return redirect('checkin_list')
    return render(request, 'checkin/checkin_confirm_delete.html', {'checkin': checkin})
