"""acrostic-poet — 藏头诗 / 俳句生成。

输入若干汉字，生成以各字开头的诗句（藏头诗）。内置规则语料库 + 模板拼接；
可选 LLM（OPENAI_API_KEY）润色。零第三方依赖。
"""
from __future__ import annotations

import json
import os
import urllib.request
import re

# 内置起字 -> 候选诗句片段（七言为主）
CHAR_LINES: dict[str, list[str]] = {
    "春": ["春风又绿江南岸", "春江水暖鸭先知", "春城无处不飞花"],
    "花": ["花褪残红青杏小", "花开花落两由之", "花重锦官城"],
    "月": ["月是故乡明", "月落乌啼霜满天", "月光如水照缁衣"],
    "山": ["山重水复疑无路", "山外青山楼外楼", "山色空蒙雨亦奇"],
    "水": ["水光潋滟晴方好", "水村山郭酒旗风", "水波轻漾送归舟"],
    "风": ["风萧萧兮易水寒", "春风得意马蹄疾", "风吹草低见牛羊"],
    "云": ["云深不知处", "云想衣裳花想容", "云开见月明"],
    "天": ["天涯共此时", "天下谁人不识君", "天高云淡望断南飞雁"],
    "海": ["海内存知己", "海上明月共潮生", "海阔凭鱼跃"],
    "一": ["一江春水向东流", "一览众山小", "一片冰心在玉壶"],
    "清": ["清风徐来水波兴", "清泉石上流", "清明时节雨纷纷"],
    "明": ["明月几时有", "明河共影湖心亭", "明日隔山岳"],
    "思": ["思君不见下渝州", "思悠悠恨悠悠", "思接千载意飞扬"],
    "归": ["归雁洛阳边", "归去也无风雨也无晴", "归梦绕家山"],
    "长": ["长风破浪会有时", "长河落日圆", "长安一片月"],
    "路": ["路漫漫其修远兮", "路上行人欲断魂", "路转溪桥忽见"],
    "白": ["白云生处有人家", "白首方悔读书迟", "白水暮东流"],
    "光": ["光彩照人归", "光景不待人", "光映寒窗读书声"],
}

# 未知字的兜底后缀（模板拼接）
_FALLBACK_SUFFIX = ["光满庭", "意悠悠", "入笔端", "映碧天", "思万千", "寄远帆"]


def _acrostic_line(ch: str, variant: int = 0) -> str:
    if ch in CHAR_LINES:
        lines = CHAR_LINES[ch]
        return lines[variant % len(lines)]
    return ch + _FALLBACK_SUFFIX[variant % len(_FALLBACK_SUFFIX)]


def make_acrostic(phrase: str, variant: int = 0) -> list[str]:
    """取 phrase 中的汉字逐字生成藏头诗。"""
    chars = re.findall(r"[\u4e00-\u9fff]", phrase)
    if not chars:
        return []
    return [_acrostic_line(ch, variant + i) for i, ch in enumerate(chars)]


def make_haiku(theme: str) -> list[str]:
    """俳句：5-7-5 节奏的三行（按汉字计数近似）。"""
    lines = [
        _acrostic_line((theme or "风")[0], 0)[:5] or "风过小桥西",
        _acrostic_line((theme or "花")[0], 1)[:7] or "花落人独立微雨",
        _acrostic_line((theme or "月")[0], 2)[:5] or "月落鸟啼霜",
    ]
    return lines


def acrostic_with_llm(phrase: str) -> list[str] | None:
    """有 key 时用 LLM 写藏头诗；无 key/失败返回 None。"""
    key = os.environ.get("OPENAI_API_KEY")
    if not key:
        return None
    base = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
    model = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo")
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": "你擅长写藏头诗。"},
            {"role": "user",
             "content": f"以「{phrase}」每字为句首，写一首五言/七言藏头诗，每行一句，共{len(phrase)}句，只输出诗句。"},
        ],
        "max_tokens": 200,
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base}/chat/completions", data=payload,
        headers={"Authorization": f"Bearer {key}",
                 "Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        content = data["choices"][0]["message"]["content"]
        return [ln.strip() for ln in content.splitlines() if ln.strip()]
    except Exception:
        return None


def generate(phrase: str, use_llm: bool = True, kind: str = "acrostic") -> dict:
    if kind == "haiku":
        return {"kind": "haiku", "source": "rule", "lines": make_haiku(phrase)}
    if use_llm:
        lines = acrostic_with_llm(phrase)
        if lines:
            return {"kind": "acrostic", "source": "llm", "lines": lines}
    return {"kind": "acrostic", "source": "rule", "lines": make_acrostic(phrase)}
