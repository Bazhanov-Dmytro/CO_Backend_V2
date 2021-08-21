import random, time, decimal
from .models import Indicators
from celery import shared_task

indicator_objects = Indicators.objects.all()
inds = {
    'heartbeat_rate': {
        "max": 150,
        "min": 25,
    },
    'higher_pressure': {
        "max": 220,
        "min": 60,
    },
    'lower_pressure': {
        "max": 170,
        "min": 30,
    },
    'temperature': {
        "max": 39.5,
        "min": 34,
    }}

@shared_task
def generate_course():
    value = random.randint(1, 10)
    if value < 3:
        return -1
    elif value > 8:
        return 1

    return 0

@shared_task
def generate_data():
    for indicatorInstance in indicator_objects:
        course = generate_course()

        change_pulse_or_pressure = random.randint(1, 3)
        change_temperature = decimal.Decimal(random.randrange(5, 10) / 25)

        if course == 1:
            if indicatorInstance.heartbeat_rate < inds["heartbeat_rate"]["max"]:
                indicatorInstance.heartbeat_rate += change_pulse_or_pressure

            if indicatorInstance.higher_pressure < inds["higher_pressure"]["max"]:
                indicatorInstance.higher_pressure += change_pulse_or_pressure

            if indicatorInstance.lower_pressure < inds["lower_pressure"]["max"]:
                indicatorInstance.lower_pressure += change_pulse_or_pressure

            if indicatorInstance.temperature < inds["temperature"]["max"]:
                indicatorInstance.temperature += change_temperature
        elif course == -1:
            if indicatorInstance.heartbeat_rate >= inds["heartbeat_rate"]["min"]:
                indicatorInstance.heartbeat_rate -= change_pulse_or_pressure

            if indicatorInstance.higher_pressure >= inds["higher_pressure"]["min"]:
                indicatorInstance.higher_pressure -= change_pulse_or_pressure

            if indicatorInstance.lower_pressure >= inds["lower_pressure"]["min"]:
                indicatorInstance.lower_pressure -= change_pulse_or_pressure

            if indicatorInstance.temperature >= inds["temperature"]["min"]:
                indicatorInstance.temperature -= change_temperature

        indicatorInstance.save()
    return indicator_objects
