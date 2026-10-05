# acrostic-poet

藏头诗 / 俳句生成小工具。输入若干汉字，生成以各字开头的诗句。内置规则语料库 + 模板拼接；可选 LLM。零第三方依赖。

## 功能

- 内置常见汉字起句库（春/花/月/山/水/风…）；
- 未知字用诗意后缀模板兜底；
- 俳句 5-7-5 三行模式；
- 配置 `OPENAI_API_KEY` 时调用 LLM 写诗；
- **无 key 自动降级为规则拼接**。

## 快速开始

```bash
python3 cli.py "山水清风"
# 山重水复疑无路
# 水村山郭酒旗风
# 清明时节雨纷纷
# 风萧萧兮易水寒
```

## 使用示例

```bash
# 俳句
python3 cli.py "花" --haiku

# 强制规则
python3 cli.py "思念" --no-llm
```

## 有 API Key 时启用 LLM

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai.com/v1"   # 可选
export OPENAI_MODEL="gpt-3.5-turbo"                 # 可选
python3 cli.py "前程似锦"
```

## 无 API Key 如何运行

不设置任何环境变量直接运行，自动使用内置语料库与模板拼接诗句，来源标注为 `rule`。

## 目录结构

```
acrostic-poet/
├── poet.py       # 起句库、藏头诗、俳句、可选 LLM
├── cli.py        # 命令行入口
├── tests/
│   └── test_poet.py
├── README.md
├── LICENSE
└── .gitignore
```

## 测试

```bash
python3 -m unittest discover -s tests
```

## 许可证

[MIT](./LICENSE)
