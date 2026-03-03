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
sidebar_upload = st.sidebar.file_uploader("CSVファイルをアップロード", type="csv", key="sidebar_upload")

# サイドバーまたはメイン画面のどちらからでもアップロード可能にする
uploaded_file = sidebar_upload

if not uploaded_file:
    st.markdown("### 📂 CSVファイルのアップロード")
    st.info("サイドバー、またはここからCSVファイルをアップロードしてください。")
    main_upload = st.file_uploader("CSVファイルをドラッグ＆ドロップ", type="csv", key="main_upload")
    uploaded_file = main_upload

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        for col in ALL_OPTIONS:
            if col not in df.columns: df[col] = 0
        df = df.fillna(0)
        
        st.sidebar.success(f"データ数: {len(df)}件")
        
        st.sidebar.header("2. 探索条件")
        
        # --- モジュールタイプによる絞り込みの追加 ---
        module_type_col = "モジュールタイプ"
        has_module_type = module_type_col in df.columns
        selected_module_types = []
        
        if has_module_type:
            # np.nan等の無効な値を除外。空白を除去してサニタイズ
            df[module_type_col] = df[module_type_col].astype(str).str.strip()
            available_types = [t for t in df[module_type_col].unique().tolist() if t != '0' and t != 'nan' and t != 'None']
            
            # デフォルトを「防御」に設定。もし「防御」が存在しない場合はあるものを全て選択状態にする
            default_types = ["防御"] if "防御" in available_types else available_types
            
            selected_module_types = st.sidebar.multiselect(
                "【絞り込み】使用するモジュールタイプ",
                options=available_types,
                default=default_types
            )
            st.sidebar.markdown("---")
        
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

        display_limit = st.sidebar.selectbox(
            "表示件数",
            options=[20, 50, 100],
            index=0
        )

        # レベル計算ヘルパー（ループ外へ移動して高速化）
        def calc_level(val):
            if val >= 20: return 6
            if val >= 16: return 5
            if val >= 12: return 4
            if val >= 8:  return 3
            if val >= 4:  return 2
            if val >= 1:  return 1
            return 0

        if st.sidebar.button("🚀 計算開始", type="primary"):
            st.markdown("---")
            st.header("計算結果")
            
            # --- プログレス（待機）表示の追加 ---
            with st.spinner('組み合わせを空間探索中... (モジュール数が多いと時間がかかります)'):
                filtered_df = df.copy()
                
                # モジュールタイプでフィルタリング
                if has_module_type and selected_module_types:
                    filtered_df = filtered_df[filtered_df[module_type_col].isin(selected_module_types)]
                
                if exclude_options:
                    mask = (filtered_df[exclude_options] > 0).any(axis=1)
                    filtered_df = filtered_df[~mask]
                
                targets = list(set(must_options + priority_options))
                if targets:
                    filtered_df = filtered_df[filtered_df[targets].sum(axis=1) > 0]
                
                modules = filtered_df.to_dict('records')
                
                if len(modules) < 4:
                    st.error(f"有効なモジュールが選ばれていないか、4つ未満です（現在: {len(modules)}個）。条件を緩めてください。")
                else:
                    results = []
                    
                    # 高速化のためのインデックスとタプル展開
                    must_indices = [ALL_OPTIONS.index(opt) for opt in must_options]
                    priority_indices = [ALL_OPTIONS.index(opt) for opt in priority_options]
                    all_len = len(ALL_OPTIONS)
                    
                    # 全モジュールをタプルに変換（辞書アクセスを排除）
                    mod_tuples = [tuple(m.get(k, 0) for k in ALL_OPTIONS) for m in modules]
                    
                    # 組み合わせの生成と評価をタプル・インデックスベースで実行
                    for combo_indices in combinations(range(len(modules)), 4):
                        m1 = mod_tuples[combo_indices[0]]
                        m2 = mod_tuples[combo_indices[1]]
                        m3 = mod_tuples[combo_indices[2]]
                        m4 = mod_tuples[combo_indices[3]]
                        
                        # 必須レベルの早期チェック（閾値20未満があればスキップ）
                        is_valid = True
                        for idx in must_indices:
                            if m1[idx] + m2[idx] + m3[idx] + m4[idx] < 20:
                                is_valid = False
                                break
                        if not is_valid:
                            continue
                        
                        # 個別ステータス合計
                        stats_vals = [m1[i] + m2[i] + m3[i] + m4[i] for i in range(all_len)]
                        
                        priority_level_sum = sum(calc_level(stats_vals[i]) for i in priority_indices)
                        total_level_sum = sum(calc_level(v) for v in stats_vals)
                        
                        extra_max = [
                            ALL_OPTIONS[i] for i, v in enumerate(stats_vals)
                            if v >= 20 and i not in must_indices and i not in priority_indices
                        ]
                        
                        # 辞書に戻して互換性を維持
                        stats_dict = {ALL_OPTIONS[i]: stats_vals[i] for i in range(all_len)}
                        
                        results.append({
                            'combo': [modules[i] for i in combo_indices],
                            'stats': stats_dict,
                            'score': sum(stats_vals[i] for i in priority_indices),
                            'total_value': sum(stats_vals),
                            'priority_level_sum': priority_level_sum,
                            'total_level_sum': total_level_sum,
                            'nonzero_count': sum(1 for v in stats_vals if v > 0),
                            'extra_max': extra_max
                        })
                
                if not results:
                    st.warning("条件を満たす組み合わせがありませんでした。")
                else:
                    # ソート順: 全項目のレベル合計（リンク効果） > 優先項目のレベル合計 > 隠れLv.6数
                    results.sort(key=lambda x: (x['total_level_sum'], x['priority_level_sum'], len(x['extra_max'])), reverse=True)
                    
                    st.success(f"{len(results)} 通りの組み合わせが見つかりました")
                    
                    for rank, res in enumerate(results[:display_limit], 1):
                        
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
