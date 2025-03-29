import pandas as pd
import random
import json
import os

DATA_PATH = "fuyu_rune_readings.csv"
USER_PATH = "user_ids.json"

df = pd.read_csv(DATA_PATH)

def get_daily_rune():
    row = df.sample(1).iloc[0]
    return format_rune_message(row)

def get_three_runes():
    samples = df.sample(3).reset_index(drop=True)
    labels = ["🌒 過去", "🌓 現在", "🌔 未來"]
    result = ""
    for i in range(3):
        result += f"{labels[i]}：\n" + format_rune_message(samples.iloc[i]) + "\n\n"
    return result.strip()

def get_learning_rune():
    row = df.sample(1).iloc[0]
    return f"📘 每日練習\n\n符文：{row['符文名稱']}（{row['正逆位']}）\n關鍵字：{row['關鍵字']}\n\n{row['解釋語句']}"

def format_rune_message(row):
    return (
        "🔮 符語娘悄悄說：\n\n"
        f"今日符文是：{row['符文名稱']}（{row['正逆位']}）\n"
        f"關鍵字：{row['關鍵字']}\n\n"
        f"{row['心靈指引']}\n{row['行動建議']}"
    )

def add_user_if_new(user_id):
    users = load_all_users()
    if user_id not in users:
        users.append(user_id)
        with open(USER_PATH, "w") as f:
            json.dump(users, f)

def load_all_users():
    if not os.path.exists(USER_PATH):
        return []
    with open(USER_PATH, "r") as f:
        return json.load(f)
