import json
import requests
import urllib2


_ACCESS_TOKEN = '4f5adfd8-aa81-48ff-835e-fdc4a73fd7b8'
_BASE_URL = 'https://api.welkinhealth.com/v1'


class BaseRequests(object):
    def __init__(self, resource):
        self.resource = resource
        self.req_url = '{base_url}/{resource}'.format(
            base_url=_BASE_URL,
            resource=self.resource)
        self.headers = {'Authorization': 'Bearer ' + _ACCESS_TOKEN,
                        'content-type': 'application/json'}

    def get_all(self):
        r = requests.get(self.req_url, headers=self.headers)
        return r.json()['data']

    def get_from_req_url(self, req_url):
        r = requests.get(req_url, headers=self.headers)
        return r.json()['data']


class CareplanRequests(BaseRequests):
    def __init__(self, resource):
        super(CareplanRequests, self).__init__(resource)
        
    def get_careplans_for_patient(self, pt_id):
        careplans = [careplan for careplan in self.get_all()
                     if careplan['user_id'] == pt_id]
        return careplans


class PatientRequests(BaseRequests):
    def __init__(self, resource):
        super(PatientRequests, self).__init__(resource)

    def get_patient(self, pt_id):
        req_url = '{base_url}/{resource}/{pt_id}/'.format(
            pt_id=pt_id,
            base_url=_BASE_URL,
            resource=self.resource)
        return self.get_from_req_url(req_url)


class MessageRequests(BaseRequests):
    def __init__(self, resource):
        super(MessageRequests, self).__init__(resource)

    def get_message(self, message_id):
        req_url = '/'.join([self.req_url, message_id])
        return self.get_from_req_url(req_url)

    def create_message(self, direction, pt_id, coach_id, conversation_id, body):
        params = {
            'direction': direction,
            'user_id': pt_id,
            'worker_id': coach_id,
            'conversation_id': conversation_id,
            'contents': body,
        }
        r = requests.post(self.req_url,
                          headers=self.headers,
                          params=params)
        return r


class CalendarEventRequests(BaseRequests):
    def __init__(self, resource):
        super(CalendarEventRequests, self).__init__(resource)

    def get_all_calendar_events(self):
        return self.get_all()

    # TODO (Franklin): This does not currently work
    # appt_type = (home_visit, outreach_call)
    # modality = (call, visit)
    def create_visit_for_patient(self, pt_id, calendar_id, appt_type,
                                 modality, start_time, end_time):
        params = {
            'calendar_id': calendar_id,
            'modality': modality,
            'appointment_type': appt_type,
            'user_id': pt_id,
            'start_time': start_time,
            'end_time': end_time
        }
        r = requests.post(self.req_url,
                          headers=self.headers,
                          params=params)
        return r.__dict__
            

def test_requests():
    pt_id = '90ba8652-8e41-4194-a602-6090e48565e5'
    calendar_id = '27ba1be0-8bf7-452c-9f50-46795491e6fa'

    # print 'Testing careplans'
    # careplan_requests = CareplanRequests('careplans')
    # print careplan_requests.get_all()

    # print 'Testing patients'
    # patient_requests = PatientRequests('patients')
    # print patient_requests.get_patient(pt_id)
    # print careplan_requests.get_careplans_for_patient(pt_id)

    print 'Testing calendar events'
    calendar_requests = CalendarEventRequests('calendar_events')
    print calendar_requests.create_visit_for_patient(pt_id,
                                                     calendar_id=calendar_id,
                                                     appt_type='home_visit',
                                                     modality='visit',
                                                     start_time='2018-03-07T13:00:00+00:00',
                                                     end_time='2018-03-07T14:00:00+00:00')

    # print 'Testing messages'
    # message_requests = MessageRequests('messages')
    # print message_requests.get_all()
    # print message_requests.create_message(direction='inbound',
    #                                       pt_id='787eae26-65a1-457c-8939-c8fbdfe8d6f2',
    #                                       coach_id='da41e701-df37-446a-b034-a4638ca6ebd9',
    #                                       conversation_id='e5063e70-ac5b-4062-a501-66fea72db868',
    #                                       body='Test creation of msg from API')
        


if __name__ == '__main__':
    test_requests()
