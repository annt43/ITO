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
        action = None
        if intent == 'turn_on_device':
            action = 'on'
            dispatcher.utter_message(
                response='utter_device_on',
                custom={"action": action, "device_name": device, "value": value}
            )
        elif intent == 'turn_off_device':
            action = 'off'
            dispatcher.utter_message(
                response='utter_device_off',
                custom={"action": action, "device_name": device, "value": value}
            )
        else:
            action = 'set'
            dispatcher.utter_message(
                response='utter_set_value',
                custom={"action": action, "device_name": device, "value": value}
            )

        try:
            requests.post(url, json={"device": device, "action": action, "value": value})
        except:
            dispatcher.utter_message(text='Không gửi được lệnh IoT')
        return []

class ActionPlayMusic(Action):
    def name(self): return "action_play_music"

    def run(self, dispatcher, tracker, domain):
        value = tracker.get_slot('value')
        dispatcher.utter_message(
            response="utter_play_music",
            custom={"action": "play_music", "device_name": "YouTube", "value": value}
        )
        try:
            webbrowser.open("https://www.youtube.com/")
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
            dispatcher.utter_message(
                text=f"Đã {'tăng' if direction == 'increase' else 'giảm'} {device}",
                custom={"action": direction, "device_name": device, "value": None}
            )
        except:
            dispatcher.utter_message(text="Không gửi được lệnh điều chỉnh.")
        return []
