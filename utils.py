
import random
import pandas as pd

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
    df = pd.read_csv("fuyu_rune_readings_final_upgraded_cleaned_final_noted.csv")
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
    if not keyword.strip():
        all_runes = [
            "Fehu", "Uruz", "Thurisaz", "Ansuz", "Raidho", "Kenaz", "Gebo", "Wunjo",
            "Hagalaz", "Nauthiz", "Isa", "Jera", "Eihwaz", "Perthro", "Algiz", "Sowilo",
            "Tiwaz", "Berkano", "Ehwaz", "Mannaz", "Laguz", "Ingwaz", "Dagaz", "Othala"
        ]
        rune_list = "｜".join(all_runes)
        return f"📜 可查詢的符文有：\n{rune_list}\n\n請輸入：查符文 + 名稱，例如「查符文 Gebo」，也可加上 正位 或 逆位 喔～"

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
