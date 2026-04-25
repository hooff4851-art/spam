rom flask import Flask, render_template, request, jsonify
import requests
import threading
import time

app = Flask(__name__)
bombing_active = False

def bomb_task(url, user_id):
    global bombing_active
    count = 1
    print(f"--- 偵錯資訊 ---")
    print(f"網址: {url}")
    print(f"ID: {user_id}")
    print(f"---------------")
    
    while bombing_active:
        # 這裡用標註格式 <@ID>
        payload = {"content": f"<@{user_id}> 網頁版轟炸中 {count}"}
        try:
            res = requests.post(url, json=payload, timeout=5)
            print(f"第 {count} 次發送 - 狀態: {res.status_code}")
            if res.status_code == 429:
                time.sleep(1)
            else:
                time.sleep(0.3)
                count += 1
        except Exception as e:
            print(f"錯誤: {e}")
            break

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    global bombing_active
    if not bombing_active:
        bombing_active = True
        data = request.json
        # 啟動轟炸執行緒
        t = threading.Thread(target=bomb_task, args=(data['url'].strip(), data['id'].strip()))
        t.start()
        return jsonify({"status": "Started"})
    return jsonify({"status": "Already Running"})

@app.route('/stop', methods=['POST'])
def stop():
    global bombing_active
    bombing_active = False
    return jsonify({"status": "Stopped"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
