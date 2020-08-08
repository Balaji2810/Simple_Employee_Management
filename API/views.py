import logging
import pytz
import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

#For NoSQL DB
from tinydb import TinyDB, Query

from constants import DB_PATH


def db_connection():
    return (TinyDB(DB_PATH),Query())

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")




@csrf_exempt
def add_member(request):
    try:
        db,query = db_connection()
        if request.method != "POST":
            return JsonResponse({'message': 'Bad Request'}, status = 400)
        data = {}
        id = request.POST.get("id")
        timezone = request.POST.get("tz")
        name = request.POST.get("real_name")


        if len(db.search(query.id == id)) != 0:
            return JsonResponse({"ok": False,'message': 'Bad Request, id already present in DB'}, status = 400)

        if id:
            data["id"] = id
        else:
            return JsonResponse({"ok": False,'message': 'Bad Request, id is missing'}, status = 400)

        if timezone:
            if timezone in pytz.all_timezones:
                data["tz"] = timezone
            else:
                return JsonResponse({"ok": False,'message': 'Bad Request, check the Time Zone'}, status = 400)

        if name:
            data["real_name"] = name

        db.insert(data)

        return JsonResponse({"ok": True,'message': 'Member Added'}, status = 200)

    except Exception as error:
        print(error)
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        db.close()




@csrf_exempt
def show_members(request):
    try:
        db,query = db_connection()
        if request.method != "GET":
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)

        members = []
        for member in db.all():
            members.append(member)

        return JsonResponse({"ok": True,'members': members}, status = 200)

    except Exception as error:
        print(error)
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        db.close()


@csrf_exempt
def show_member(request,id):
    try:
        db,query = db_connection()
        if request.method != "GET":
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)


        member = db.search(query.id == id)
        if len(member) == 0:
            return JsonResponse({"ok": False,'message': 'Bad Request, id not present in DB'}, status = 400)


        return JsonResponse({"ok": True,'members': member}, status = 200)

    except Exception as error:
        print(error)
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        db.close()

def time_validator(start,end):
    try:
        work_hours = abs(datetime.datetime.strptime(end,"%b %d %Y %I:%M%p") - datetime.datetime.strptime(start,"%b %d %Y %I:%M%p"))
        return work_hours.total_seconds() / 60
    except:
        return None

@csrf_exempt
def add_activity_period(request,id):
    try:
        db,query = db_connection()
        if request.method != "POST":
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)


        member = db.search(query.id == id)
        if len(member) == 0:
            return JsonResponse({"ok": False,'message': 'Bad Request, id not present in DB'}, status = 400)

        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        data = {}
        duration_in_minutes = time_validator(start_time,end_time)
        if duration_in_minutes:
            data["duration_in_minutes"] = duration_in_minutes
            data["start_time"] = start_time
            data["end_time"] = end_time

            if "activity_periods" not in member[0]:
                member[0]["activity_periods"] = []

            member[0]["activity_periods"].append(data)
            db.upsert(member[0],query.id == id)

        else:
            return JsonResponse({"ok": False,'message': 'Bad Request, Kindly Check the Start and End Time. (eg : Mar 1 2020 2:00PM)'}, status = 400)
        return JsonResponse({"ok": True, 'message':"Activity Period Added"}, status = 200)

    except Exception as error:
        print(error)
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        db.close()
