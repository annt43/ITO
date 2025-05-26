from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Danh sách thiết bị và action hợp lệ
VALID_DEVICES = {'quạt', 'đèn', 'máy lạnh'}
VALID_ACTIONS = {'on', 'off', 'set', None}

@app.route('/control', methods=['POST'])
def control():
    data = request.json or {}

    timestamp = datetime.datetime.now().isoformat()
    device = data.get('device', 'Không rõ')
    room = data.get('room', 'Không rõ')
    action = data.get('action')
    value = data.get('value')

    errors = []

    # Kiểm tra device hợp lệ
    if device not in VALID_DEVICES:
        errors.append(f"Thiết bị không hợp lệ: {device}")

    # Không kiểm tra room nữa

    # Kiểm tra action hợp lệ
    if action not in VALID_ACTIONS:
        errors.append(f"Action không hợp lệ: {action}")

    if errors:
        print("\n❌ Lệnh bị từ chối:")
        for err in errors:
            print(" -", err)
        return jsonify({
            "status": "ERROR",
            "timestamp": timestamp,
            "errors": errors
        }), 400

    # In log
    print("\n========== 📥 IoT Command Received ==========")
    print(f"[Time]    {timestamp}")
    print(f"[Device]  {device}")
    print(f"[Room]    {room}")
    if action: print(f"[Action]  {action}")
    if value: print(f"[Value]   {value}")
    print("=============================================")

    return jsonify({
        "status": "OK",
        "timestamp": timestamp,
        "device": device,
        "room": room,
        "action": action,
        "value": value
    })

if __name__ == '__main__':
    app.run(port=5000)
