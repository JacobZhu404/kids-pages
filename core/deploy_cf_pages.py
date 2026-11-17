"""
kids-pages Cloudflare Pages 部署模块

将 public/ 目录下的静态文件（数学/算法互动教程，专为孩子共享）部署到 Cloudflare Pages。
URL 永久固定：https://kids-pages.pages.dev/<文件名>.html

部署方式：wrangler CLI（API Token 认证），沿用 ad-newsletter 的成熟封装。
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Optional


# 项目根目录（core 的上一级）
PROJECT_ROOT = Path(__file__).parent.parent
PUBLIC_DIR = PROJECT_ROOT / "public"
WRANGLER_TOML = PROJECT_ROOT / "wrangler.toml"
CF_CONFIG = PROJECT_ROOT / "cloudflare_config.json"
CF_PROJECT_NAME = "kids-pages"

def _env(name: str) -> str:
    """读取环境变量，去掉首尾空白，返回空字符串表示未设置。"""
    return os.environ.get(name, "").strip()


# 公司环境常驻失效代理，wrangler 走代理会报 TLS/连接错误，部署前必须剔除。
PROXY_KEYS = (
    "http_proxy", "https_proxy", "all_proxy",
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
)


def clean_env(base: Optional[dict] = None) -> dict:
    """返回剥离代理变量的环境副本。"""
    env = dict(base if base is not None else os.environ)
    for key in PROXY_KEYS:
        env.pop(key, None)
    env.pop("NO_PROXY", None)
    env.pop("no_proxy", None)
    return env


def find_wrangler() -> Optional[list]:
    """
    定位 wrangler，返回可直接执行的命令前缀。

    顺序：PATH 上的 wrangler → 常见全局路径 → npx 缓存里的 wrangler.js（用 node 跑）。
    npx 现拉常因缓存残留报 ENOTEMPTY，所以优先复用已缓存包。
    """
    home = Path.home()
    direct = [shutil.which("wrangler")]
    direct += [
        str(home / ".workbuddy/binaries/node/versions/22.22.2/bin/wrangler"),
        "/usr/local/bin/wrangler",
        "/opt/homebrew/bin/wrangler",
    ]
    direct += [str(p) for p in sorted(
        home.glob(".workbuddy/binaries/node/versions/*/bin/wrangler"), reverse=True
    )]
    for candidate in direct:
        if candidate and os.path.exists(candidate) and os.access(candidate, os.X_OK):
            return [candidate]

    node = shutil.which("node")
    if not node:
        for p in sorted(home.glob(".workbuddy/binaries/node/versions/*/bin/node"), reverse=True):
            if os.access(p, os.X_OK):
                node = str(p)
                break
    if node:
        scripts = sorted(
            home.glob(".npm/_npx/*/node_modules/wrangler/bin/wrangler.js"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )
        if scripts:
            return [node, str(scripts[0])]
    return None


def load_cf_config() -> dict:
    """加载 Cloudflare 配置"""
    if CF_CONFIG.exists():
        with open(CF_CONFIG, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def deploy_to_cf() -> bool:
    """
    将 public/ 整个目录部署到 Cloudflare Pages。

    Returns:
        成功返回 True，失败返回 False
    """
    cfg = load_cf_config()
    # 凭证来源优先级：环境变量 > cloudflare_config.json。
    # 绝不能把 Token 硬编码进代码（GitHub secret scanning 会拦截）。
    api_token = _env("CLOUDFLARE_API_TOKEN") or cfg.get("api_token", "")
    account_id = _env("CLOUDFLARE_ACCOUNT_ID") or cfg.get("account_id", "")

    if not api_token or not account_id:
        print("   ⚠️ Cloudflare 配置不完整，跳过 CF Pages 部署")
        return False

    # 确保 wrangler.toml 存在
    if not WRANGLER_TOML.exists():
        WRANGLER_TOML.write_text(
            f'name = "{CF_PROJECT_NAME}"\n'
            f'compatibility_date = "2026-08-09"\n'
            f'pages_build_output_dir = "public"\n',
            encoding="utf-8",
        )

    # Fail fast before sending any files if generated pages/assets are inconsistent.
    smoke = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "core/deploy_smoke_test.py")],
        cwd=str(PROJECT_ROOT), capture_output=True, text=True, timeout=90,
    )
    if smoke.returncode != 0:
        print(f"   ⚠️ 部署前冒烟测试未通过:\n{smoke.stdout}{smoke.stderr}")
        return False
    print(f"   🔎 {smoke.stdout.strip()}")

    # 部署整个 public 目录
    try:
        env = clean_env()
        env["CLOUDFLARE_API_TOKEN"] = api_token
        env["CLOUDFLARE_ACCOUNT_ID"] = account_id

        base_args = [
            "pages", "deploy",
            str(PUBLIC_DIR),
            "--project-name", CF_PROJECT_NAME,
            "--branch", "main",
            "--commit-dirty=true",
        ]
        wrangler_cmd = find_wrangler()
        if wrangler_cmd is None:
            print("   ⚠️ 未找到 wrangler（PATH / 全局安装 / npx 缓存均无）")
            return False
        cmd = [*wrangler_cmd, *base_args]
        print(f"   🔧 调用 wrangler: {' '.join(wrangler_cmd)}（已清除代理变量）")

        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=180,
            env=env,
            stdin=subprocess.DEVNULL,
        )

        if result.returncode != 0:
            print(f"   ⚠️ CF Pages 部署失败: {result.stderr.strip()[-300:]}")
            return False

        url = f"https://{CF_PROJECT_NAME}.pages.dev/"
        print(f"   ✅ CF Pages 部署成功: {url}")
        return True

    except subprocess.TimeoutExpired:
        print("   ⚠️ CF Pages 部署超时")
        return False
    except FileNotFoundError:
        print("   ⚠️ wrangler CLI 未安装，跳过 CF Pages 部署")
        return False
    except Exception as e:
        print(f"   ⚠️ CF Pages 部署异常: {e}")
        return False


if __name__ == "__main__":
    ok = deploy_to_cf()
    sys.exit(0 if ok else 1)
