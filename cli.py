"""命令行：python3 cli.py "藏头短语" """
import argparse
import json
import sys

from poet import generate


def main(argv=None):
    p = argparse.ArgumentParser(description="acrostic-poet 藏头诗/俳句生成")
    p.add_argument("phrase", nargs="?", help="藏头汉字，如：春暖花开")
    p.add_argument("--haiku", action="store_true", help="生成俳句")
    p.add_argument("--no-llm", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    phrase = args.phrase or sys.stdin.read().strip()
    if not phrase:
        print("错误：未提供藏头汉字", file=sys.stderr)
        return 2

    kind = "haiku" if args.haiku else "acrostic"
    result = generate(phrase, use_llm=not args.no_llm, kind=kind)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"（{result['kind']}，来源：{result['source']}）")
        for line in result["lines"]:
            print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
