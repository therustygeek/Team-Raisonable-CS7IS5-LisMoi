from django.shortcuts import render

from django.views import View
from django.http import HttpResponse

from DAO import get_Mood , get_user_preferences
  
def mood_of_user(request):
    mood = get_Mood(1)
    return render(request,'dbtest/dbtest.html',{'mood':mood})
    
def pref_of_user(request):
    pref = get_user_preferences(1)
    return render(request,'dbtest/dbtest.html',{'pref':pref})

# More Testing Required  