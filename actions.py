from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests
import webbrowser

class ActionControlDevice(Action):
    def name(self): return "action_control_device"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent']['name']
        device = tracker.get_slot('device')
        value = tracker.get_slot('value')
        if not device:
            dispatcher.utter_message(text="Tôi chưa rõ thiết bị bạn muốn điều khiển.")
            return []

        url = 'http://localhost:5000/control'
        if intent == 'turn_on_device':
            payload = {'device': device, 'action': 'on'}
            dispatcher.utter_message(response='utter_device_on')
        elif intent == 'turn_off_device':
            payload = {'device': device, 'action': 'off'}
            dispatcher.utter_message(response='utter_device_off')
        else:
            payload = {'device': device, 'value': value}
            dispatcher.utter_message(response='utter_set_value')

        try:
            requests.post(url, json=payload)
        except:
            dispatcher.utter_message(text='Không gửi được lệnh IoT')
        return []

class ActionPlayMusic(Action):
    def name(self): return "action_play_music"

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(response="utter_play_music")
        try:
            webbrowser.open("https://www.youtube.com/watch?v=ZbZSe6N_BXs")
        except:
            dispatcher.utter_message(text="Không thể mở trình duyệt để phát nhạc.")
        return []

class ActionAdjustSetting(Action):
    def name(self): return "action_adjust_setting"

    def run(self, dispatcher, tracker, domain):
        intent = tracker.latest_message['intent']['name']
        device = tracker.get_slot("device")
        if not device:
            dispatcher.utter_message(text="Tôi chưa rõ thiết bị cần điều chỉnh.")
            return []

        direction = "increase" if intent == "increase_setting" else "decrease"
        payload = {
            "device": device,
            "adjust": direction
        }

        try:
            requests.post("http://localhost:5000/control", json=payload)
            msg = f"Đã {'tăng' if direction == 'increase' else 'giảm'} {device}"
            dispatcher.utter_message(text=msg)
        except:
            dispatcher.utter_message(text="Không gửi được lệnh điều chỉnh.")
        return []
