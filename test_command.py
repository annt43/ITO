import asyncio
from rasa_service import analyze_text_with_rasa, extract_device_command 

async def test():
    user_input = input("Nhập câu điều khiển: ")
    result = await analyze_text_with_rasa(user_input)
    print("Phản hồi từ Rasa:", result)

    if result["status"] == "success":
        command = extract_device_command(result)
        print("Lệnh trích xuất được:", command)
    else:
        print("Lỗi:", result["message"])

asyncio.run(test())
