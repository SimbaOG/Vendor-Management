from apscheduler.schedulers.background import BackgroundScheduler

# Create a global background scheduler to handle tasks like performing logging of historical
# aggregations and updating po with related actions

global_scheduler = BackgroundScheduler()
global_scheduler.start()
