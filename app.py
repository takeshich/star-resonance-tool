import streamlit as st
import pandas as pd
from itertools import combinations

# --- 設定 ---
st.set_page_config(page_title="モジュール計算機 v8.3", layout="wide")

ALL_OPTIONS = [
    "魔法耐性", "物理耐性", 
    "極・HP凝縮", "極・絶境守護", "極・HP変動", "極・HP吸収",
    "筋力強化", "敏捷強化", "知力強化",
    "特攻ダメージ強化", "精鋭打撃", "特攻回復強化", "マスタリー回復強化",
    "集中・詠唱", "集中・攻撃速度", "集中・会心", "集中・幸運",
    "極・ダメージ増強", "極・適応力", "極・応急処置", "極・幸運会心"
]

LEVEL_THRESHOLDS = [1, 4, 8, 12, 16, 20]

def get_level_label(value):
    """数値からLv表記を返す"""
    level = 0
    for i, thresh in enumerate(LEVEL_THRESHOLDS):
        if value >= thresh: level = i + 1
        else: break
    return f"Lv.{level}" if level > 0 else "-"

def highlight_rows(row):
    """行ごとのスタイル適用"""
    gold_style = 'background-color: #FFD700; color: black; font-weight: bold'
    header_style = 'background-color: #333333; color: white; font-weight: bold'
    default_style = ''

    if row["ID"] in ["到達レベル", "合計値"]:
        return [header_style] * len(row)
    
    # 数値データの個数をカウント
    numeric_values = pd.to_numeric(row.drop("ID"), errors='coerce').fillna(0)
    count = (numeric_values > 0).sum()
    
    if count >= 3:
        return [gold_style] * len(row)
    return [default_style] * len(row)

# --- メイン画面 ---
st.title("🛡️ モジュール組み合わせ計算機")

st.sidebar.header("1. データ読み込み")
uploaded_file = st.sidebar.file_uploader("CSVファイルをアップロード", type="csv")

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        for col in ALL_OPTIONS:
            if col not in df.columns: df[col] = 0
        df = df.fillna(0)
        
        st.sidebar.success(f"データ数: {len(df)}件")
        
        st.sidebar.header("2. 探索条件")
        
        default_must = [c for c in ["魔法耐性", "物理耐性"] if c in df.columns]
        must_options = st.sidebar.multiselect(
            "【必須】Lv.6 (値20以上) にする項目",
            options=ALL_OPTIONS,
            default=default_must
        )
        
        priority_options = st.sidebar.multiselect(
            "【優先】値を伸ばしたい項目",
            options=[c for c in ALL_OPTIONS if c not in must_options]
        )
        
        exclude_options = st.sidebar.multiselect(
            "【除外】計算に含めない項目",
            options=ALL_OPTIONS
        )

        if st.sidebar.button("🚀 計算開始", type="primary"):
            st.markdown("---")
            st.header("計算結果")
            
            filtered_df = df.copy()
            if exclude_options:
                mask = (filtered_df[exclude_options] > 0).any(axis=1)
                filtered_df = filtered_df[~mask]
            
            targets = list(set(must_options + priority_options))
            if targets:
                filtered_df = filtered_df[filtered_df[targets].sum(axis=1) > 0]
            
            modules = filtered_df.to_dict('records')
            
            if len(modules) < 4:
                st.error("有効なモジュールが4つ未満です。")
            else:
                results = []
                
                for combo in combinations(modules, 4):
                    stats = {k: 0 for k in ALL_OPTIONS}
                    for m in combo:
                        for k in ALL_OPTIONS:
                            stats[k] += m.get(k, 0)
                    
                    if any(stats[opt] < 20 for opt in must_options):
                        continue
                    
                    score = sum(stats[opt] for opt in priority_options)
                    total_value = sum(stats.values())
                    
                    # 隠れLv.6
                    extra_max = [
                        k for k, v in stats.items() 
                        if v >= 20 and k not in must_options and k not in priority_options
                    ]
                    
                    results.append({
                        'combo': combo,
                        'stats': stats,
                        'score': score,
                        'total_value': total_value,
                        'extra_max': extra_max
                    })
                
                if not results:
                    st.warning("条件を満たす組み合わせがありませんでした。")
                else:
                    results.sort(key=lambda x: (len(x['extra_max']), x['score'], x['total_value']), reverse=True)
                    
                    st.success(f"{len(results)} 通りの組み合わせが見つかりました")
                    
                    for rank, res in enumerate(results[:20], 1):
                        
                        # --- タイトルを番号のみに変更 ---
                        st.subheader(f"{rank}")
                        # -----------------------------

                        display_cols = must_options + priority_options + \
                            [k for k in ALL_OPTIONS if res['stats'][k] > 0 and k not in must_options + priority_options]
                        display_cols = sorted(list(set(display_cols)), key=lambda x: (x not in must_options, x not in priority_options))

                        table_rows = []
                        
                        row_lv = {"ID": "到達レベル"}
                        row_sum = {"ID": "合計値"}
                        for col in display_cols:
                            row_lv[col] = get_level_label(res['stats'][col])
                            row_sum[col] = res['stats'][col]
                        table_rows.append(row_lv)
                        table_rows.append(row_sum)
                        
                        for m in res['combo']:
                            row_mod = {"ID": m.get('ID', 'NoID')}
                            for col in display_cols:
                                row_mod[col] = m.get(col, 0)
                            table_rows.append(row_mod)
                        
                        df_res = pd.DataFrame(table_rows)
                        cols_order = ["ID"] + [c for c in display_cols]
                        df_res = df_res[cols_order]

                        st.dataframe(
                            df_res.style.apply(highlight_rows, axis=1),
                            use_container_width=True,
                            hide_index=True
                        )
                        st.markdown("---")

    except Exception as e:
        st.error(f"エラー: {e}")

else:
    st.info("👈 左側のサイドバーからCSVファイルをアップロードしてください。")
