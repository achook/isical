
from scrapper import get_timetable
from generator import generate_and_upload
from geo import get_coordinates

from os import environ

# Function to run from GCP
def make_ics(event, context):
    timetable = get_timetable(environ['START_DATE'],environ['END_DATE'])
    coords = get_coordinates(timetable.buildings)
    generate_and_upload(timetable.lectures, coords)

    return True

#make_ics(None, None)