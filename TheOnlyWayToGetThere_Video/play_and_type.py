import sys
import time
import subprocess
import os

def clear_screen():
    os.system('clear')

def type_text(text, duration, line_start_ref):
    """
    Types text over a specified duration with natural character pauses,
    anchored to line_start_ref to avoid timing drift.
    """
    weights = []
    prev_char = ''
    for char in text:
        if char in [',', ';']:
            weights.append(4.0)
        elif char in ['.', '?', '!']:
            weights.append(2.0 if prev_char == '.' else 6.0)
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
    print()

# Timeline synchronized with the audio: (start_sec, text, end_sec)
lyrics = [
    (3.10, "So today...", 4.60),
    (4.90, "Don't think about it.", 6.40),
    (6.75, "Don't talk about it.", 8.10),
    (8.45, "Don't wish for it.", 10.30),
    (10.75, "Go for it.", 12.00),
    (12.60, "Dive.", 13.40),
    (13.75, "Move.", 14.60),
    (14.85, "Start.", 15.70),
    (15.95, "Act.", 16.50),
    (16.90, "Trust me.", 17.85),
    (18.20, "It's the only way to get there.", 20.25),
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
    mp3_path = os.path.join(script_dir, "the-only-way-to-get-there.mp3")

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

    for start_t, text, end_t in lyrics:
        now = time.time() - t_zero
        if start_t > now:
            time.sleep(start_t - now)

        line_start_ref = t_zero + start_t
        duration = end_t - start_t

        sys.stdout.write(" " * 10)
        type_text(text, duration, line_start_ref)

    # Musiqa avjiga chiqqanda chiqadigan mualliflik imzosi
    time.sleep(1.0)
    print("\n\n                         <farrukh.dev/>\n")

    player.wait()

if __name__ == "__main__":
    main()
