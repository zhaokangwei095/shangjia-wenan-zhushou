#!/usr/bin/env python3
"""商家文案助手 · 违禁词体检脚本。

扫描文案文本，标出绝对化用语、收益承诺等高风险表述并给出替换建议。
用法：python3 banned_words_check.py 文案.txt
     echo "全网最低价，最好用的面膜" | python3 banned_words_check.py -
"""
import re
import sys

RULES = [
    ("绝对化用语", r"全网最低|全国第一|中国第一|全球第一|世界级|国家级|顶级|顶尖|唯一|独一无二|史无前例|百分之百|100%有效|最好|最佳|第一名",
     "删除绝对化表述，改为可核验的事实：具体价格、活动期限、工艺或数据来源"),
    ("功效承诺", r"立竿见影|药到病除|治愈|根治|美白祛斑|7天换肤|包治",
     "改为合规的功效范围内表述（清洁/保湿等），食品和日化不得宣称治疗或超备案功效"),
    ("收益承诺", r"稳赚不赔|保本保收益|躺赚|零风险|收益率\d",
     "金融类收益承诺直接删除，不得改写保留"),
    ("虚假紧迫感", r"最后一件|仅剩\d+秒|马上售罄|清仓最后一天",
     "改为真实的活动信息：活动价金额 + 明确截止日期，无期限则删除"),
]


def scan(text: str):
    hits = []
    for category, pattern, advice in RULES:
        for m in re.finditer(pattern, text):
            line_no = text[: m.start()].count("\n") + 1
            hits.append((line_no, category, m.group(0), advice))
    return hits


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    text = sys.stdin.read() if sys.argv[1] == "-" else open(sys.argv[1], encoding="utf-8").read()
    hits = scan(text)
    if not hits:
        print("✅ 未命中清单中的高风险词。注意：本脚本只覆盖常见词表，交付前仍需人工逐句自检。")
        return 0
    print(f"⚠️ 命中 {len(hits)} 处高风险表述：")
    for line_no, cat, word, advice in hits:
        print(f"- 第{line_no}行 [{cat}] 「{word}」→ {advice}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
