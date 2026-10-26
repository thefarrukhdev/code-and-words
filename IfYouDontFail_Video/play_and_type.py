import sys
import time
import subprocess
import os

# ANSI escape codes for styling
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
WHITE_BOLD = "\033[1;97m"

def clear_screen():
    os.system('clear')

def type_text(text, duration, line_start_ref, prefix="", style=""):
    """
    Types text over a specified duration with natural character pauses,
    anchored to line_start_ref to avoid timing drift.
    Prefix and styling are applied without interfering with typing rhythm.
    """
    sys.stdout.write(prefix)
    if style:
        sys.stdout.write(style)
    sys.stdout.flush()

    weights = []
    prev_char = ''
    for char in text:
        if char in [',', ';', ':']:
            weights.append(4.0)
        elif char in ['.', '?', '!']:
            weights.append(2.0 if prev_char == '.' else 6.0)
        elif char in ['"', "'", '“', '”']:
            weights.append(1.5)
        elif char == ' ':
            weights.append(1.5)
        else:
            weights.append(1.0)
        prev_char = char

    total_weight = sum(weights) if weights else 1.0
    cumulative_weight = 0

    for i, char in enumerate(text):
        target = line_start_ref + (cumulative_weight / total_weight) * duration
        now = time.time()
        if target > now:
            time.sleep(target - now)

        sys.stdout.write(char)
        sys.stdout.flush()
        cumulative_weight += weights[i]

    target_end = line_start_ref + duration
    now = time.time()
    if target_end > now:
        time.sleep(target_end - now)

    if style:
        sys.stdout.write(RESET)
        sys.stdout.flush()

    print()

# Timeline synchronized with the audio: (start_sec, text, end_sec, is_quote)
lyrics = [
    (0.10, "If you don't fail,", 1.80, False),
    (2.35, "you're not even trying.", 3.70, False),
    (5.85, "I'll say it again.", 6.70, False),
    (6.95, "If you don't fail,", 8.25, False),
    (8.45, "you're not even trying.", 9.30, False),
    (9.45, "My wife told me this great expression:", 10.95, False),
    (11.30, "“To get something you never had,", 13.30, True),
    (13.50, " you have to do something you never did.”", 16.05, True),
]

def main():
    delay_seconds = 0
    if len(sys.argv) > 1:
        try:
            delay_seconds = int(sys.argv[1])
        except ValueError:
            pass

    if delay_seconds > 0:
        clear_screen()
        for i in range(delay_seconds, 0, -1):
            sys.stdout.write(f"\r[ Kamera uchun tayyorgarlik: {i} soniya qoldi... ]")
            sys.stdout.flush()
            time.sleep(1)

    clear_screen()
    print("\n" * 5)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(script_dir, "if-you-dont-fail.mp3")

    if not os.path.exists(mp3_path):
        print(f"Xatolik: Audio fayl topilmadi: {mp3_path}")
        return

    try:
        player = subprocess.Popen(['mpv', '--no-video', mp3_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        try:
            player = subprocess.Popen(['ffplay', '-nodisp', '-autoexit', mp3_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print("Error: mpv yoki ffplay topilmadi. Audio tinglash uchun birortasini o'rnating.")
            return

    # Audio boshlanishi uchun qisqa kutish
    time.sleep(0.3)
    t_zero = time.time()

    base_indent = " " * 10

    for i, (start_t, text, end_t, is_quote) in enumerate(lyrics):
        now = time.time() - t_zero
        if start_t > now:
            time.sleep(start_t - now)

        # Semantik bloklar oralig'iga bo'sh qator tashlash
        if i in [2, 3, 5, 6]:
            print()

        line_start_ref = t_zero + start_t
        duration = end_t - start_t

        if is_quote:
            prefix = base_indent + f"{CYAN}│{RESET}  "
            style = WHITE_BOLD
        else:
            prefix = base_indent
            style = ""

        type_text(text, duration, line_start_ref, prefix=prefix, style=style)

    # Musiqa avjiga chiqqanda chiqadigan mualliflik imzosi
    signature_target = t_zero + 16.35
    now = time.time()
    if signature_target > now:
        time.sleep(signature_target - now)

    print(f"\n\n                         {DIM}<farrukh.dev/>{RESET}\n")

    player.wait()

if __name__ == "__main__":
    main()
