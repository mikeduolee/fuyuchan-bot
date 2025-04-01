import random
import pandas as pd

USER_CSV_PATH = "user_data.csv"

# 加入無逆位符文處理
def enforce_valid_rune_orientation(rune_name, position):
    no_reversed_runes = ["Gebo", "Isa", "Sowilo", "Jera", "Eihwaz", "Ingwaz"]
    base_name = rune_name.split("（")[0]  # 去除附註

    if base_name in no_reversed_runes:
        return "正位", True  # 強制轉為正位
    else:
        return position, False

# 讀取資料庫（以升級清理後版本為例）
def load_rune_data():
    df = pd.read_csv("fuyu_rune_readings_final_upgraded.csv")
    return df

# 單抽符文
def get_daily_rune():
    df = load_rune_data()
    rune = df.sample().iloc[0]
    rune_name = rune["符文名稱"]
    position = "正位" if random.random() > 0.5 else "逆位"
    position, no_reverse = enforce_valid_rune_orientation(rune_name, position)

    result = df[(df["符文名稱"] == rune_name) & (df["正逆位"] == position)]
    if result.empty:
        result = df[df["符文名稱"] == rune_name]  # 取正位資料

    row = result.iloc[0]
    text = f"🔮 {rune_name} {position if position else ''}\n\n"
    text += f"{row['解釋語句']}\n\n✨ {row['心靈指引']}\n📜 {row['行動建議']}"
    
    if no_reverse:
        text += "\n\n⚠️ 此符文無正逆位之分，已以正位解讀。"
    
    return text

# 搜尋符文內容：可接受中文或英文查詢
def search_rune(keyword):
    keyword = keyword.strip()

    if keyword == "":
        all_runes = [
            "Fehu ᚠ", "Uruz ᚢ", "Thurisaz ᚦ", "Ansuz ᚨ", "Raido ᚱ", "Kenaz ᚲ", "Gebo ᚷ", "Wunjo ᚹ",
            "Hagalaz ᚺ", "Nauthiz ᚾ", "Isa ᛁ", "Jera ᛃ", "Eihwaz ᛇ", "Perthro ᛈ", "Algiz ᛉ", "Sowilo ᛋ",
            "Tiwaz ᛏ", "Berkano ᛒ", "Ehwaz ᛖ", "Mannaz ᛗ", "Laguz ᛚ", "Ingwaz ᛜ", "Dagaz ᛞ", "Othala ᛟ"
        ]
        rune_list = "｜".join(all_runes)
        return (
            "📜 可查詢的符文如下：
"
            f"{rune_list}

"
            "請輸入：查符文 + 名稱，例如「查符文 Gebo」"
        )

    df = load_rune_data()
    results = df[df["符文名稱"].str.contains(keyword, case=False, na=False)]

    if results.empty:
        return f"🔍 沒有找到與「{keyword}」相關的符文喔～試著檢查拼字或換個詞搜尋吧。"

    reply = f"🔎 搜尋結果：{keyword}

"
    for _, row in results.iterrows():
        pos = row["正逆位"] if pd.notna(row["正逆位"]) and row["正逆位"] else "（無正逆位）"
        image_base = row["符文名稱"].split("（")[0].strip()
        image_url = f"https://mikeduolee.github.io/fuyu-rune-assets/{image_base}.png"

        reply += f"🖼️ 圖片：{image_url}
"
        reply += f"🌿 {row['符文名稱']} {pos}
"
        reply += f"{row['解釋語句']}
✨ {row['心靈指引']}
📜 {row['行動建議']}

"

    return reply.strip()

    keyword = keyword.strip()

    if keyword == "":
        all_runes = [
            "Fehu ᚠ ", "Uruz ᚢ ", "Thurisaz ᚦ ", "Ansuz ᚨ ", "Raido ᚱ ", "Kenaz ᚲ ", "Gebo ᚷ ", "Wunjo ᚹ ",
            "Hagalaz ᚺ ", "Nauthiz ᚾ ", "Isa ᛁ ", "Jera ᛃ ", "Eihwaz ᛇ ", "Perthro ᛈ ", "Algiz ᛉ ", "Sowilo ᛋ ",
            "Tiwaz ᛏ ", "Berkano ᛒ ", "Ehwaz ᛖ ", "Mannaz ᛗ ", "Laguz ᛚ ", "Ingwaz ᛜ ", "Dagaz ᛞ ", "Othala ᛟ "
        ]
        rune_list = "｜".join(all_runes)
        return (
            "📜 可查詢的符文如下：\n"
            f"{rune_list}\n\n"
            "請輸入：查符文 + 名稱，例如「查符文 Gebo」"
        )

    df = load_rune_data()
    results = df[df["符文名稱"].str.contains(keyword, case=False, na=False)]

    if results.empty:
        return f"🔍 沒有找到與「{keyword}」相關的符文喔～試著檢查拼字或換個詞搜尋吧。"

    reply = f"🔎 搜尋結果：{keyword}\n\n"
    for _, row in results.iterrows():
        pos = row["正逆位"] if pd.notna(row["正逆位"]) and row["正逆位"] else "（無正逆位）"
        reply += f"🌿 {row['符文名稱']} {pos}\n"
        reply += f"{row['解釋語句']}\n✨ {row['心靈指引']}\n📜 {row['行動建議']}\n\n"

    return reply.strip()

def get_three_runes():
    df = load_rune_data()
    selected = df.sample(3).reset_index(drop=True)
    reply = "📜 三符文占卜結果：\n\n"
    for i, row in selected.iterrows():
        pos = row["正逆位"] if pd.notna(row["正逆位"]) and row["正逆位"] else "（無正逆位）"
        reply += f"🪄 第 {i+1} 枚：{row['符文名稱']} {pos}\n"
        reply += f"{row['解釋語句']}\n✨ {row['心靈指引']}\n📜 {row['行動建議']}\n\n"
    return reply.strip()

def get_five_runes():
    df = load_rune_data()
    selected = df.sample(5).reset_index(drop=True)
    reply = "🌟 五符文占卜結果：\n\n"
    for i, row in selected.iterrows():
        pos = row["正逆位"] if pd.notna(row["正逆位"]) and row["正逆位"] else "（無正逆位）"
        reply += f"🪄 第 {i+1} 枚：{row['符文名稱']} {pos}\n"
        reply += f"{row['解釋語句']}\n✨ {row['心靈指引']}\n📜 {row['行動建議']}\n\n"
    return reply.strip()

def get_learning_rune():
    df = load_rune_data()
    row = df.sample(1).iloc[0]
    pos = row["正逆位"] if pd.notna(row["正逆位"]) and row["正逆位"] else "（無正逆位）"
    reply = (
        "🧘‍♀️ 每日符文學習\n\n"
        f"📖 今日符文：{row['符文名稱']} {pos}\n"
        f"🔍 關鍵詞：{row['關鍵字']}\n"
        f"{row['解釋語句']}\n\n"
        f"✨ 心靈指引：{row['心靈指引']}\n"
        f"📜 行動建議：{row['行動建議']}\n"
    )
    return reply.strip()
    
def add_user_if_new(user_id):
    try:
        df = pd.read_csv(USER_CSV_PATH)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["user_id"])

    if user_id not in df["user_id"].values:
        df = pd.concat([df, pd.DataFrame([{"user_id": user_id}])], ignore_index=True)
        df.to_csv(USER_CSV_PATH, index=False)
