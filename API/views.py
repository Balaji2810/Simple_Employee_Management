import logging
import pytz
import datetime
import json
from urllib.parse import parse_qs

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt
from django.http.multipartparser import MultiPartParser


#For NoSQL DB
from tinydb import TinyDB, Query

from constants import DB_PATH


def db_connection():
    """
    Returns a connection object for the TinyBD
    """
    return (TinyDB(DB_PATH),Query())


def index(request):
    """
    Renders Simple API Doc.
    """
    return render(request,"doc.html",{"domain":request.META['HTTP_HOST']})

@csrf_exempt
def add_member(request):
    """
    Adds a new member to the DataBase:
    returns a success status if the data inserted to the database
    """
    try:
        logging.info("Add member called")
        #database Connection
        db,query = db_connection()
        #Checking the Request Method
        if request.method != "POST":
            logging.info("Add member BAD REQUEST")
            return JsonResponse({'message': 'Bad Request'}, status = 400)
        data = {}
        id = request.POST.get("id")
        timezone = request.POST.get("tz")
        name = request.POST.get("real_name")

        #Checking the ID in the Database
        if len(db.search(query.id == id)) != 0:
            logging.info("Add member ID already present")
            return JsonResponse({"ok": False,'message': 'Bad Request, id already present in DB'}, status = 400)

        #Checking for ID value
        if id and id != "":
            data["id"] = id
        else:
            logging.info("Add member ID missing")
            return JsonResponse({"ok": False,'message': 'Bad Request, id is missing'}, status = 400)

        #Validating the TimeZone
        if timezone:
            if timezone in pytz.all_timezones:
                data["tz"] = timezone
            else:
                logging.info("Add member TimeZone invalid")
                return JsonResponse({"ok": False,'message': 'Bad Request, check the Time Zone'}, status = 400)

        if name:
            data["real_name"] = name
        #Inserting into the DataBase
        db.insert(data)

        logging.info("Add member completed successfully")
        return JsonResponse({"ok": True,'message': 'Member Added'}, status = 200)

    except Exception as error:
        logging.error(str(error))
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        #Closing the Database Connection
        db.close()




@csrf_exempt
def show_members(request):
    """
    Fetchs All the Member Details form the DataBase:
    return a JSON which contains the Member Details
    """
    try:
        logging.info("Show members Called")
        #database Connection
        db,query = db_connection()
        #Checking the Request Method
        if request.method != "GET":
            logging.info("Show members BAD REQUEST")
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)

        members = []
        #Fetching all the Records fomr the DataBase
        for member in db.all():
            members.append(member)
        logging.info("Show members Completed successfully")
        return JsonResponse({"ok": True,'members': members}, status = 200)

    except Exception as error:
        logging.error(str(error))
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        #Closing the Database Connection
        db.close()


@csrf_exempt
def show_member(request,id):
    """
    Fetch the Unique Member Details form the DataBase based on the ID:
    return a JSON which contains the Member Details
    """
    try:
        logging.info("Show member Called")
        #database Connection
        db,query = db_connection()
        #Checking the Request Method
        if request.method != "GET":
            logging.info("Show member BAD REQUEST")
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)

        #Fetch the Specified Record from the DataBase
        member = db.search(query.id == id)
        if len(member) == 0:
            logging.info("Show member ID not in DB")
            return JsonResponse({"ok": False,'message': 'Bad Request, id not present in DB'}, status = 400)

        logging.info("Show member Completed successfully")
        return JsonResponse({"ok": True,'members': member}, status = 200)

    except Exception as error:
        logging.error(str(error))
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        #Closing the Database Connection
        db.close()

def time_validator(start,end):
    """
    This function validates the Time Format
    """
    try:
        work_hours = abs(datetime.datetime.strptime(end,"%b %d %Y %I:%M%p") - datetime.datetime.strptime(start,"%b %d %Y %I:%M%p"))
        return work_hours.total_seconds() / 60
    except:
        logging.info("Invalid Time Format")
        return None

@csrf_exempt
def add_activity_period(request,id):
    """
    This function ADDS ActivityPeriod to the specific Member based on the ID:
    returns a success status if the data inserted to the database
    """
    try:
        logging.info("Add Activity Period Called")
        #database Connection
        db,query = db_connection()
        #Checking the Request Method
        if request.method != "POST":
            logging.info("Add Activity Period BAD REQUEST")
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)

        #Checking the ID in the DataBase
        member = db.search(query.id == id)
        if len(member) == 0:
            logging.info("Add Activity Period ID not in DB")
            return JsonResponse({"ok": False,'message': 'Bad Request, id not present in DB'}, status = 400)

        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        data = {}
        #Calculating the Duration between start and end time.
        duration_in_minutes = time_validator(start_time,end_time)

        #Validate the Start and End Time
        if duration_in_minutes:
            data["duration_in_minutes"] = duration_in_minutes
            data["start_time"] = start_time
            data["end_time"] = end_time

            #If the activity_periods is not present for the Member
            if "activity_periods" not in member[0]:
                member[0]["activity_periods"] = []

            #Append the ActivityPeriod to the DataBase
            member[0]["activity_periods"].append(data)

            #Inserting The Activity Period in the DataBase
            db.upsert(member[0],query.id == id)

        else:
            logging.info("Add Activity Period Time invalid")
            return JsonResponse({"ok": False,'message': 'Bad Request, Kindly Check the Start and End Time. (eg : Mar 1 2020 2:00PM)'}, status = 400)
        logging.info("Add Activity Period completed successfully")
        return JsonResponse({"ok": True, 'message':"Activity Period Added"}, status = 200)

    except Exception as error:
        logging.error(str(error))
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        #Closing the Database Connection
        db.close()



@csrf_exempt
def update_member(request,id):
    """
    This function is to Update the Member Details based on the ID.
    returns a success status if the data update in the database
    """
    try:
        logging.info("Update Member Called")
        #database Connection
        db,query = db_connection()
        #Checking the Request Method
        if request.method != "PUT":
            logging.info("Update Member BAD REQUEST")
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)

        #Checking the ID in the DataBase
        if not db.contains(query.id == id):
            logging.info("Update Member ID not in DB")
            return JsonResponse({"ok": False,'message': 'Bad Request, id not present in DB'}, status = 400)

        #processing the PUT Request
        try:
            put = MultiPartParser(request.META, request, request.upload_handlers).parse()[0]
        except Exception as e:
            temp = parse_qs(str(request.body,"utf-8"))
            put = {}
            for item in temp:
                put[item] = temp[item][0]

        #Before changing the ID, Checks the DataBase to avoid Duplicate IDs.
        new_id = put.get("id")
        if new_id:
            if db.contains(query.id == new_id):
                logging.info("Update Member ID already present")
                return JsonResponse({"ok": False,'message': 'Bad Request, new id already present in DB'}, status = 400)
        data = {}

        #Validating the TimeZone
        timezone = put.get("tz")
        if timezone:
            if timezone not in pytz.all_timezones:
                logging.info("Update Member invalid TimeZone")
                return JsonResponse({"ok": False,'message': 'Bad Request, check the Time Zone'}, status = 400)

        #Change to the ActivityPeriod is avoided
        for item in put:
            if item == "activity_periods":
                continue
            data[item] = put.get(item)

        #Raise a WARNING if Data is empty
        if len(data)==0:
            logging.info("Update Member no data to update")
            return JsonResponse({"ok": False,'message': 'Bad Request, Nothing to change'}, status = 400)

        #Update the Changes in the Database
        db.upsert(data,query.id == id)
        logging.info("Update Member completed successfully")
        return JsonResponse({"ok": True, 'message':"Updated Member"}, status = 200)

    except Exception as error:
        logging.error(str(error))
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        #Closing the Database Connection
        db.close()

@csrf_exempt
def delete_member(request,id):
    """
    This function DELETEs a specific member form the DataBase based on the ID:
    returns a success status if the record is Removed
    """
    try:
        logging.info("Delete Member Called")
        #database Connection
        db,query = db_connection()
        #Checking the Request Method
        if request.method != "DELETE":
            logging.info("Delete Member BAD REQUEST")
            return JsonResponse({"ok": False,'message': 'Bad Request'}, status = 400)

        #Checking the DataBase for ID
        if not db.contains(query.id == id):
            logging.info("Delete Member ID not in DB")
            return JsonResponse({"ok": False,'message': 'Bad Request, id not present in DB'}, status = 400)

        #Removinf the Specified ID from the DataBase
        db.remove(query.id == id)
        logging.info("Delete Member Completed successfully")
        return JsonResponse({"ok": True, 'message':"Member Deleted"}, status = 200)

    except Exception as error:
        logging.error(str(error))
        return JsonResponse({"ok": False,'message': 'Server Error'}, status = 500)
    finally:
        #Closing the Database Connection
        db.close()
