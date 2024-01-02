# from workers import celery
import time
from datetime import timedelta
import csv, os
from database import exportdetails
from utils import send_message
from celery.schedules import crontab
from celery import shared_task

import flask_excel as excel
from weasyprint import HTML
from celery import shared_task
from monthly_report import generate_monthly_report
@shared_task()
def send_welcome_msg(data):
    print(time.time())
    time.sleep(10)
    print(time.time())
    return "Test"

webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'

@shared_task(ignore_result=False)
def generate_csv():
    time.sleep(10)
    for file in os.listdir('./instance'):
        if file.endswith(".csv"):
            os.remove(f'./instance/{file}')
    with open(f'./instance/name.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "stock_left", "rate", "units sold"])
        result = exportdetails()
        for row in result:
            name, stock_left, rate_per_unit, total_quantity = row
            print(
                f"Product Name: {name},Stock Left {stock_left}, Rate per Unit: {rate_per_unit}, Total Quantity: {total_quantity}")

            writer.writerow(row)  # to send file to user as download

    # Message content to send
    message = 'CSV sent after generating. Click here to download: http://127.0.0.1:5003/download_csv'
    send_message(webhook_url, message)
    return "./instance/name.csv"

# @celery.on_after_finalize.connect
# def setup_periodic_tasks(sender, **kwargs):
#     sender.add_periodic_task(crontab(hour=17,minute=6), engagment.s(), name='Monthly Report')
#     sender.add_periodic_task(timedelta(seconds=30), engagment.s(), name="Secondly report")
#     # sender.add_periodic_task(crontab(minute=0, hour=0), daily_reminder.s(), name='daily reminders')

@shared_task()
def engagment():
    webhook_url = 'https://chat.googleapis.com/v1/spaces/AAAABN4yDm8/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=bdFYUNx6xyL2btWwQDrHKIflDVhQBJ66rSs-vcREwjA'

    message="This is a daily reminder message"
    send_message(webhook_url, message)

@shared_task
def bla():
    return generate_csv()
    


from celery import shared_task
import flask_excel as excel
from mail_service import send_email
from models import User, Role
from jinja2 import Template
from celery import shared_task

@shared_task(ignore_result=False)
def create_resource_csv():
    print("inside")
    from app import db  # Check if the import location is correct
    
    stud_res = User.query.all()
    data = [(i.email, i.fname) for i in stud_res]
    print(data)
    csv_output = excel.make_response_from_array(data, "csv", file_name="test.csv")
    print(csv_output)
    print("our")
    return csv_output



@shared_task(ignore_result=True)
def monthly_report():
    subject='Monthly report'
    users = User.query.filter(User.roles.any(Role.name == 'user')).all()
    for user in users:
        report_file = generate_monthly_report(user.id)
        print(f"Report generated: {report_file}")
        temp_html = f'report.html'
        pdf_file = f'report.pdf'
        if os.path.exists(pdf_file):
            os.remove(pdf_file)

        HTML(temp_html).write_pdf(pdf_file)
        # with open(f'report_{user.id}.html', 'r') as f:
        send_email(user.email, subject,message="Monthly report",attachement_file=pdf_file,content="pdf")
    print(users)
    return "OK"

