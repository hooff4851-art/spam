from flask import Flask, render_template, request, jsonify
import requests
import threading
import time
import os

app = Flask(__name__)

# 儲存任務狀態
tasks = {}

def spam_task(webhook_url, user_id):
    content = f"<@{user_id}> 🚯 該起床囉！"
    while tasks.get(webhook_url):
        try:
            requests.post(webhook_url, json={"content": content})
        except:
            pass
        time.sleep(0.5)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    data = request.json
    url = data.get('url')
    user_id = data.get('id')
    if url and url not in tasks:
        tasks[url] = True
        threading.Thread(target=spam_task, args=(url, user_id), daemon=True).start()
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    data = request.json
    url = data.get('url')
    if url in tasks:
        tasks[url] = False
        del tasks[url]
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
