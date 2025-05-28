from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

# Cho phép các thiết bị có chứa từ khóa này
VALID_KEYWORDS = {'quạt', 'đèn', 'máy lạnh'}

def is_valid_device(device_name: str) -> bool:
    if not device_name:
        return False
    device_name = device_name.lower()
    return any(keyword in device_name for keyword in VALID_KEYWORDS)

@app.route('/control', methods=['POST'])
def control():
    data = request.json or {}

    timestamp = datetime.datetime.now().isoformat()
    device = data.get('device', '').strip()
    action = data.get('action')
    value = data.get('value')
    adjust = data.get('adjust')

    errors = []

    # Kiểm tra thiết bị
    if not is_valid_device(device):
        errors.append(f"Thiết bị không hợp lệ: {device}")

    # Kiểm tra action/adjust hợp lệ nếu có
    if action and action not in {"on", "off", "set"}:
        errors.append(f"Action không hợp lệ: {action}")
    if adjust and adjust not in {"increase", "decrease"}:
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
    print("\n========== 📥 Lệnh IoT nhận được ==========")
    print(f"[Time]     {timestamp}")
    print(f"[Device]   {device}")
    if action:
        print(f"[Action]   {action}")
    if adjust:
        print(f"[Adjust]   {adjust}")
    if value:
        print(f"[Value]    {value}")
    print("============================================")

    return jsonify({
        "status": "OK",
        "timestamp": timestamp,
        "device": device,
        "action": action,
        "adjust": adjust,
        "value": value
    })

if __name__ == '__main__':
    app.run(port=5000)
