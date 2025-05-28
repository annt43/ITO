from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Danh sách thiết bị hợp lệ
VALID_DEVICES = {'quạt', 'đèn', 'máy lạnh'}
VALID_ACTIONS = {'on', 'off', 'set', None}
VALID_ADJUSTS = {'increase', 'decrease', None}

@app.route('/control', methods=['POST'])
def control():
    data = request.json or {}

    timestamp = datetime.datetime.now().isoformat()
    device = data.get('device', 'Không rõ')
    room = data.get('room', 'Không rõ')
    action = data.get('action')
    value = data.get('value')
    adjust = data.get('adjust')

    errors = []

    # Kiểm tra device hợp lệ
    if device not in VALID_DEVICES:
        errors.append(f"Thiết bị không hợp lệ: {device}")

    # Kiểm tra action (nếu có)
    if action not in VALID_ACTIONS:
        errors.append(f"Action không hợp lệ: {action}")

    # Kiểm tra adjust (nếu có)
    if adjust not in VALID_ADJUSTS:
        errors.append(f"Điều chỉnh không hợp lệ: {adjust}")

    # Trả lỗi nếu có
    if errors:
        print("\n❌ Lệnh bị từ chối:")
        for err in errors:
            print(" -", err)
        return jsonify({
            "status": "ERROR",
            "timestamp": timestamp,
            "errors": errors
        }), 400

    # In log hợp lệ
    print("\n========== 📥 IoT Command Received ==========")
    print(f"[Time]     {timestamp}")
    print(f"[Device]   {device}")
    print(f"[Room]     {room}")
    if action: print(f"[Action]   {action}")
    if adjust: print(f"[Adjust]   {adjust}")
    if value: print(f"[Value]    {value}")
    print("=============================================")

    return jsonify({
        "status": "OK",
        "timestamp": timestamp,
        "device": device,
        "room": room,
        "action": action,
        "adjust": adjust,
        "value": value
    })

if __name__ == '__main__':
    app.run(port=5000)
