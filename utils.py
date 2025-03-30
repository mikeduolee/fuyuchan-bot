
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
