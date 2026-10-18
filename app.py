#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""📖 中文默書預備 — 10 個詞語默寫訓練"""
import re
import random
import unicodedata
import streamlit as st

st.set_page_config(page_title="📖 中文默書預備", page_icon="📖", layout="wide")

WORDS = [
    ("難以忘懷", "非常難忘記，一直記得", "那次旅行的美好回憶，令我難以忘懷。"),
    ("彬彬有禮", "舉止文雅、很有禮貌", "這個彬彬有禮的孩子見到長輩會主動問好。"),
    ("攔住", "擋住、阻止前進", "警察攔住了違反交通規則的司機。"),
    ("鞠躬", "彎腰行禮致敬", "表演結束後，演員向觀眾鞠躬致謝。"),
    ("狼狽", "困窘、難堪的樣子", "被大雨淋得全身濕透，他的樣子十分狼狽。"),
    ("愣住", "因吃驚而呆住", "聽到這個意外的消息，他當場愣住了。"),
    ("沾滿", "沾上、佈滿", "他工作了一整天，雙手沾滿了泥土。"),
    ("誇張", "言過其實，超過實際情況", "他說話總是誇張，不可盡信。"),
    ("僅有", "只有、僅僅有", "這是他僅有的一點積蓄。"),
    ("鼓勵", "激勵、勸勉他人", "老師鼓勵我們努力學習，不要放棄。"),
]

def _norm(s):
    """正規化：全形→半形、刪空白同標點括號，用嚟寬鬆比對默寫"""
    s = unicodedata.normalize("NFKC", s or "")
    return re.sub(r"[\s「」『』\"'“”’（）()]+", "", s)

def mask_example(word, example):
    """把詞語喺例句中挖空成＿＿＿＿（默寫提示用）"""
    return example.replace(word, "＿＿＿＿")

# ===== Sidebar =====
with st.sidebar:
    st.header("⚙️ 設定")
    mode = st.radio("模式", ["📖 詞語溫習", "✍️ 默寫測驗"], key="d_mode")
    if mode.startswith("✍️"):
        order = st.radio("出題順序", ["隨機", "按表順序"], key="d_order_mode")
        st.caption("默寫：睇解釋＋例句（詞語挖空），憑記憶默寫詞語。")

st.title("📖 中文默書預備")
st.caption("10 個詞語 — 先溫習，再默寫，即場批改。")

# ===== 溫習模式 =====
if mode.startswith("📖"):
    st.subheader("📖 詞語溫習（10 個）")
    for w, m, ex in WORDS:
        with st.expander(f"**{w}** — {m}"):
            st.markdown(f"📝 例句：{ex}")
    st.info("👈 溫習完，去左邊 sidebar 揀「✍️ 默寫測驗」開始默寫。")

# ===== 默寫模式 =====
else:
    if "d_checked" not in st.session_state:
        st.session_state.d_checked = False
    if "d_order" not in st.session_state:
        st.session_state.d_order = list(range(len(WORDS)))

    if st.button("🎲 開始默寫", type="primary", use_container_width=True):
        idx = list(range(len(WORDS)))
        if st.session_state.get("d_order_mode", "隨機") == "隨機":
            random.shuffle(idx)
        st.session_state.d_order = idx
        st.session_state.d_checked = False
        for k in list(st.session_state.keys()):
            if re.fullmatch(r"d_a\d+", str(k)):
                del st.session_state[k]
        st.rerun()

    st.divider()

    if st.session_state.d_checked:
        correct = 0
        for i, wi in enumerate(st.session_state.d_order):
            w, m, ex = WORDS[wi]
            user = st.session_state.get(f"d_a{i}", "")
            ok = _norm(user) == _norm(w)
            if ok:
                correct += 1
                st.success(f"**✅ 第 {i + 1} 題**　你默寫咗「{user}」— 啱！")
            else:
                shown = user if user else "（未默寫）"
                st.error(f"**❌ 第 {i + 1} 題**　你默寫咗：「{shown}」　正確：**{w}**")
            st.markdown(f"💡 {m}　|　📝 {ex}")
            st.markdown("---")
        st.metric("🏆 得分", f"{correct} / {len(WORDS)}")
        if st.button("🔄 再默一次", use_container_width=True):
            idx = list(range(len(WORDS)))
            if st.session_state.get("d_order_mode", "隨機") == "隨機":
                random.shuffle(idx)
            st.session_state.d_order = idx
            st.session_state.d_checked = False
            for k in list(st.session_state.keys()):
                if re.fullmatch(r"d_a\d+", str(k)):
                    del st.session_state[k]
            st.rerun()
    else:
        for i, wi in enumerate(st.session_state.d_order):
            w, m, ex = WORDS[wi]
            st.markdown(f"**{i + 1}.** {m}")
            st.markdown(f"📝 例句：{mask_example(w, ex)}")
            st.text_input("默寫詞語", key=f"d_a{i}", label_visibility="collapsed",
                          placeholder="憑記憶默寫詞語…")
        if st.button("✅ 檢查答案", type="primary", use_container_width=True):
            st.session_state.d_checked = True
            st.rerun()
