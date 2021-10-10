from datetime import datetime
from os import name
from uuid import uuid1

from google.cloud import storage

from const import GROUPS
from typing import List
from classes import Lecture

from icalendar import Calendar, Event, vGeo

def generate_and_upload(lectures: List[Lecture], coordinates) -> None:
    groups = GROUPS

    for group in groups.keys():
        cal = Calendar()

        # Some of this is not needed but some implementations
        # somehow need it
        cal.add('prodid', '-//Kalendarz//ISI//achook.dev//EN')
        cal.add('version', '2.0')
        cal.add('calscale', 'GREGORIAN')
        cal.add('method', 'PUBLISH')
        cal.add('X-WR-TIMEZONE', 'utc')
        cal.add('X-WR-CALNAME', 'Zajęcia')

        # I have no idea what is happening from where up until
        # line 45 but somehow it works and splits the whole timetable into groups
        # TODO: Make it readable
        for lecture in lectures:
            if 'apart_from' in groups[group]:
                if lecture.subject in groups[group]['apart_from'].keys():
                    if lecture.lecture_type == groups[group]['apart_from'][lecture.subject][0]:
                        if lecture.group != groups[group]['apart_from'][lecture.subject][1]:
                            continue
                    else:
                        if lecture.group not in groups[group]['groups']:
                            continue
                else:
                    if lecture.group not in groups[group]['groups']:
                        continue
            else:
                if lecture.group not in groups[group]['groups']:
                    continue

            # Some of this is not needed but some implementations
            # somehow need it (Apple mostly)
            event = Event()

            event.add('summary', lecture.subject)
            event.add('dtstart', lecture.start)
            event.add('dtend', lecture.end)
            event.add('dtstamp', datetime.now())
            event.add('created', datetime.now())
            event.add('last-modified', datetime.now())
            event.add('sequence', 0)
            event.add('status', 'confirmed')
            event.add('transp', 'opaque')

            uid = uuid1().hex
            event.add('uid', uid)

            # Make the description (not ugly)
            desc = ''
            if lecture.lecture_type is not None:
                desc += 'Typ: ' + lecture.lecture_type + '\n'
            if lecture.lecturer is not None:
                desc += 'Prowadzący: ' + lecture.lecturer + '\n'
            if lecture.building is not None:
                desc += 'Budynek: ' + lecture.building + '\n'

                lat = coordinates[lecture.building]['lat']
                lng = coordinates[lecture.building]['lng']

                geo = vGeo((lat, lng))
                event['geo'] = geo

                event.add('location', f'AGH {lecture.building}, Kraków')

            if lecture.room is not None:
                desc += 'Sala: ' + lecture.room
            
            
            event.add('description', desc)
            cal.add_component(event)

        # Upload to Google Cloud
        file = cal.to_ical()
        storage_client = storage.Client()
        bucket = storage_client.bucket('isi-ical')
        blob = bucket.blob(f'cal-{group}.ics')

        # Do not allow caching, otherwise updating doesn't work on Apple
        blob.cache_control = 'no-store; max-age=0'
        blob.upload_from_string(file, content_type='text/calendar')
