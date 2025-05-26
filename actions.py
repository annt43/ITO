from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

class ActionControlDevice(Action):
    def name(self): return "action_control_device"
    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent']['name']
        dev = tracker.get_slot('device') or 'thiết bị'
        room = tracker.get_slot('room') or 'nơi nào đó'
        val = tracker.get_slot('value')
        url = 'http://localhost:5000/control'
        if intent=='turn_on_device':
            payload={'device':dev,'room':room,'action':'on'}
            dispatcher.utter_message(response='utter_device_on')
        elif intent=='turn_off_device':
            payload={'device':dev,'room':room,'action':'off'}
            dispatcher.utter_message(response='utter_device_off')
        else:
            payload={'device':dev,'room':room,'value':val}
            dispatcher.utter_message(response='utter_set_value')
        try:
            requests.post(url,json=payload)
        except:
            dispatcher.utter_message(text='Không gửi được lệnh IoT')
        return []
    
class ActionPlayMusic(Action):
    def name(self): return "action_play_music"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_play_music")
        # Mở một video YouTube bằng trình duyệt mặc định
        try:
            webbrowser.open("https://www.youtube.com/watch?v=ZbZSe6N_BXs")  # Happy - Pharrell Williams
        except:
            dispatcher.utter_message(text="Không thể mở trình duyệt để phát nhạc.")
        return []