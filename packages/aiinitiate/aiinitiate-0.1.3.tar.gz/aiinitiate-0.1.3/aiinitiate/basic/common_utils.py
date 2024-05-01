import subprocess
import os
import typer


def install_common_utils():
    try:
        subprocess.run(["sudo", "apt-get", "update"])
        typer.echo("start install curl")
        subprocess.run(["sudo", "apt-get", "install", "curl", "-y"])
        typer.echo("curl install success")

        typer.echo("start install git")
        subprocess.run(["sudo", "apt-get", "install", "git", "-y"])
        typer.echo("git install success")

        typer.echo("start install htop")
        subprocess.run(["sudo", "apt-get", "install", "htop", "-y"])
        typer.echo("htop install success")

        typer.echo("start install rsync")
        subprocess.run(["sudo", "apt-get", "install", "rsync", "-y"])
        typer.echo("rsync install success")

        typer.echo("start install vim")
        subprocess.run(["sudo", "apt-get", "install", "vim", "-y"])
        typer.echo("vim install success")
    except Exception as e:
        print(f"Failed to install: {e}")


def _install_zsh():
    subprocess.run(["sudo", "apt-get", "install", "zsh", "-y"])
    # 设置 Zsh 为默认 Shell
    subprocess.run(["chsh", "-s", "/bin/zsh"])
    # 安装 Oh My Zsh
    subprocess.run(
        ["sh", "-c", "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"])
    # 配置 Powerlevel10k 主题
    subprocess.run(["git", "clone", "https://github.com/romkatv/powerlevel10k.git",
                    "~/.oh-my-zsh/custom/themes/powerlevel10k"])
    # 更新 Zsh 配置文件 .zshrc
    with open(os.path.expanduser("~/.zshrc"), "a") as f:
        f.write("\n# Set Zsh theme to Powerlevel10k\n")
        f.write("ZSH_THEME=\"powerlevel10k/powerlevel10k\"\n")
