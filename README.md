# Code and Words

> A collection of poetic terminal scripts, CLI art, and visual stories built with code.

This repository serves as a personal diary and a creative canvas, blending programming with storytelling. Each folder contains a unique project designed to run in the terminal, exploring how code can be used to express thoughts, poetry, and philosophy.

## Projects

* **`umr-otmoqda`** — A beautifully timed terminal typing effect synchronized with audio, illustrating the fleeting nature of time like a flowing river.
* **`only-way`** — A motivational terminal typing experience precisely synchronized to voice and rhythm, capturing the mindset of relentless action ("It's the only way to get there").
* **`tashlab-ketgan-joy`** — A poignant, emotionally resonant terminal poem synchronized with voice and music, reflecting on longing, struggle, and steadfast loyalty ("Tashlab ketgan joydaman").
* **`boglanib-qolma`** — A deeply reflective terminal poem synchronized with voice and soulful melody, about detachment, human nature, and resilience ("Bog'lanib qolma hech inson zotiga").
* **`aldagan-emas`** — A thought-provoking terminal reflection synchronized with voice, pondering honesty, conscience, and inner peace ("Aldagan emas, aldalgan bo'lish ancha yaxshiroq").
* **`sen-ham-xohlaysan`** — A spiritual and deeply moving Hadith Qudsi recital by Abdulloh domla, reflecting on surrender to the Divine will, trust, and peace ("Sen ham xohlaysan, Men ham xohlayman").
* **`if-you-dont-fail`** — An electrifying terminal typing performance synchronized to Denzel Washington's legendary words on risk, failure, and growth ("If you don't fail, you're not even trying").

## Prerequisites

The scripts use Python 3 and rely on a lightweight CLI audio player (either `mpv` or `ffplay` from `ffmpeg`):

```bash
# Ubuntu / Debian
sudo apt install mpv

# Arch Linux
sudo pacman -S mpv

# macOS
brew install mpv
```

## How to Run

Navigate into any project folder and execute `main.py`:

```bash
cd if-you-dont-fail
python3 main.py
```

To give yourself prep time before screen recording starts, pass a countdown delay in seconds:

```bash
python3 main.py 5
```

---
Created by `<the.farrukh.dev/>`
