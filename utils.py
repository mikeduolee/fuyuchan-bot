
import pandas as pd
import random
import json
import os
from linebot import LineBotApi
from linebot.models import TextSendMessage

DATA_PATH = "fuyu_rune_readings_final_upgraded.csv"
USER_PATH = "user_ids.json"

# 預載符文資料
df = pd.read_csv(DATA_PATH)

# ✅ 單張符文抽取
def get_daily_rune():
    row = df.sample(1).iloc[0]
    return format_rune_message(row)

# ✅ 三符文占卜
def get_three_runes():
    samples = df.sample(3).reset_index(drop=True)
    labels = ["🌒 過去", "🌓 現在", "🌔 未來"]
    result = ""
    for i in range(3):
        result += f"{labels[i]}：\n" + format_rune_message(samples.iloc[i]) + "\n\n"
    return result.strip()

# ✅ 五符文占卜
def get_five_runes():
    samples = df.sample(5).reset_index(drop=True)
    positions = ["🌑 根本問題", "🌱 潛在能量", "🌬 阻礙因素", "🔥 助力或轉機", "🌈 結果與建議"]
    result = ""
    for i in range(5):
        row = samples.iloc[i]
        result += f"{positions[i]}：\n"
        result += f"符文：{row['符文名稱']}（{row['正逆位']}）\n"
        result += f"關鍵字：{row['關鍵字']}\n\n"
        result += f"{row['心靈指引']}\n{row['行動建議']}\n\n"
    return result.strip()

# ✅ 升級版每日練習（內含所有指引）
def get_learning_rune():
    row = df.sample(1).iloc[0]
    rune = row["符文名稱"]
    position = row["正逆位"]
    keyword = row["關鍵字"]
    intro = row["解釋語句"]
    guidance = row["心靈指引"]
    action = row["行動建議"]

    return (
        f"🧘‍♀️ 符語娘每日練習：\n\n"
        f"✨ 今日符文：{rune}（{position}）\n🔑 關鍵字：{keyword}\n\n"
        f"📖 指引語：{intro}\n\n"
        f"🌙 心靈引導：\n{guidance}\n\n"
        f"📌 行動建議：\n{action}"
    )

# ✅ 格式化符文訊息
def format_rune_message(row):
    return (
        "🔮 符語娘悄悄說：\n\n"
        f"今日符文是：{row['符文名稱']}（{row['正逆位']}）\n"
        f"關鍵字：{row['關鍵字']}\n\n"
        f"{row['心靈指引']}\n{row['行動建議']}"
    )

# ✅ 新增使用者
def add_user_if_new(user_id):
    users = load_all_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_PATH, "w") as f:
            json.dump(users, f)

# ✅ 載入所有使用者
def load_all_users():
    if not os.path.exists(USER_PATH):
        return []
    with open(USER_PATH, "r") as f:
        return json.load(f)

# ✅ 每日推播
def push_daily_practice_fuyu():
    line_bot_api = LineBotApi(os.getenv("CHANNEL_ACCESS_TOKEN"))
    users = load_all_users()

    if not users:
        print("⚠️ 無使用者可推播")
        return

    today_row = df.sample(1).iloc[0]
    rune = today_row["符文名稱"]
    position = today_row["正逆位"]
    keyword = today_row["關鍵字"]
    intro = today_row["解釋語句"]
    guidance = today_row["心靈指引"]
    action = today_row["行動建議"]

    message = (
        f"🧘‍♀️ 符語娘每日練習：\n\n"
        f"✨ 今日符文：{rune}（{position}）\n🔑 關鍵字：{keyword}\n\n"
        f"📖 指引語：{intro}\n\n"
        f"🌙 心靈引導：\n{guidance}\n\n"
        f"📌 行動建議：\n{action}"
    )

    for uid in users:
        try:
            line_bot_api.push_message(uid, TextSendMessage(text=message))
        except Exception as e:
            print(f"❌ 推播失敗：{uid}, 錯誤：{e}")
