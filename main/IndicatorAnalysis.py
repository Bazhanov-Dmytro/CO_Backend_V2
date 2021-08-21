import random


class Analyser:
    def __init__(self, bpm=None, pressure=None, temp=None):
        self.parameters['heartbeat']['value'] = bpm
        self.parameters['pressure']['value'] = pressure
        self.parameters['temperature']['value'] = temp
        self.danger_level = 0
        self.recommendation = []

    advices = {
        'common': [
            '-Drink more water.',
            '-Try to avoid smoking for sometime if you do smoke.',
            '-Take additional work breaks.',
            '-Limit your alcohol and coffee intakes.',
            '-Get enough sleep'
        ],
        'heartbeat': [
            '-Go for a walk if you have an opportunity.',
            '-Breath in and out slow and deep for a couple of minutes.',
        ],
        'pressure': [
            '-Eat vegetable, fruit or drink a glass of milk or yogurt, nuts or beans would be okay too.',
            '-Cut back you sugar consuming.',
        ],
        'temperature': [
            '-Apply something cold like ice to the body key points such as the wrists, neck, chest, and temples.',
            '-Move less, take a break while temperature is high.',
        ],
    }

    def create_advice(self):
        params = self.parameters
        used_common = []
        for param in params:
            if params[param]['status'] != 'Normal':
                self.recommendation.append(self.advices[param][random.randint(0, 1)])

                while True:
                    random_advice = random.randint(0, 4)

                    if random_advice not in used_common:
                        used_common.append(random_advice)
                        self.recommendation.append(self.advices['common'][random_advice])
                        break

                self.danger_level += 1

    parameters = {
        'heartbeat': {
            'value': None,
            'status': None,
        },
        'pressure': {
            'value': None,
            'status': None,
        },
        'temperature': {
            'value': None,
            'status': None,
        },
    }

    def check_values(self):
        params = self.parameters
        for param in params:
            if params[param]['value'] is None:
                return False
        return True

    def analise_heartbeat(self):
        try:
            heartbeat = int(self.parameters['heartbeat']['value'])
        except ValueError or TypeError:
            raise Exception('Heartbeat value must be an integer.')

        if heartbeat < 45:
            self.parameters['heartbeat']['status'] = 'Low'
        elif heartbeat > 95:
            self.parameters['heartbeat']['status'] = 'High'
        else:
            self.parameters['heartbeat']['status'] = 'Normal'

    def analise_pressure(self):
        try:
            lp = int(self.parameters['pressure']['value'][1])
            hp = int(self.parameters['pressure']['value'][0])
        except ValueError or TypeError:
            raise Exception('Pressure values must be an integers.')

        if lp < 65 or hp < 105:
            self.parameters['pressure']['status'] = 'Low'
        elif lp > 95 or hp > 135:
            self.parameters['pressure']['status'] = 'High'
        else:
            self.parameters['pressure']['status'] = 'Normal'

    def analise_temperature(self):
        try:
            temp = float(self.parameters['temperature']['value'])
        except ValueError or TypeError:
            raise Exception('Temperature must be provided as float or integer.')

        if temp < 36:
            self.parameters['temperature']['status'] = 'Low'
        elif temp > 37:
            self.parameters['temperature']['status'] = 'High'
        else:
            self.parameters['temperature']['status'] = 'Normal'

    def execute_full_analysis(self):
        if self.check_values():
            self.analise_heartbeat()
            self.analise_pressure()
            self.analise_temperature()

            self.create_advice()
            return self.parameters['heartbeat']['status'] + self.parameters['pressure']['status'] + self.parameters['temperature']['status'], "\n".join(self.recommendation), self.danger_level
        else:
            raise ValueError('Not all parameters were provided.')

