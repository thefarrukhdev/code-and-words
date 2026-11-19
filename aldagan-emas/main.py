#!/usr/bin/env python3
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
        elif char in ["'", "’", "‘"]:
            weights.append(1.2)
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
    (0.00, "Aldagan emas,", 0.85),
    (1.00, "aldalgan bo'lish ancha yaxshiroq.", 2.30),
    (2.40, "Aldalgan insonni niyati pok bo'ladi,", 4.30),
    (4.40, "Qalbi toza bo'ladi,", 5.15),
    (5.20, "Uni bir muammosi yo'qki,", 6.40),
    (6.50, "Aldagan inson bo'lsa,", 7.60),
    (7.70, "Qilgan tanlovi va vijdoni oldida,", 9.60),
    (9.80, "Yuzma-yuz qoladi va", 11.00),
    (11.20, "O'ziga o'zi javob berish bo'p qoladi.", 12.60),
    (12.80, "Inson birovlarni aldashi judayam oson,", 15.00),
    (15.20, "Lekin o'zini o'zi aldashi bu bir muammo.", 17.30),
    (17.50, "O'zini o'zi hech qachon aldolmaydi,", 18.80),
    (18.90, "Va o'zini vijdoniga beradigan javoblari,", 21.10),
    (21.20, "Judayam og'ir bo'ladi.", 22.30),
    (22.40, "Buning ustida biz diqqatli bo'lishimiz kerak,", 24.60),
    (24.70, "Aldangan inson bo'lib yashavurishimiz,", 26.60),
    (26.70, "Ancha yaxshiroq deb o'ylab qolaman ba'zida.", 28.20),
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
    mp3_path = os.path.join(script_dir, "audio.mp3")

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

    for i, (start_t, text, end_t) in enumerate(lyrics):
        now = time.time() - t_zero
        if start_t > now:
            time.sleep(start_t - now)

        # Semantik bloklar oralig'iga bo'sh qator tashlash
        if i in [2, 5, 9, 14]:
            print()

        line_start_ref = t_zero + start_t
        duration = end_t - start_t

        sys.stdout.write(" " * 10)
        type_text(text, duration, line_start_ref)

    # Musiqa avjiga chiqqanda chiqadigan mualliflik imzosi
    signature_target = t_zero + 28.5
    now = time.time()
    if signature_target > now:
        time.sleep(signature_target - now)

    print("\n\n                         <the.farrukh.dev/>\n")

    player.wait()

if __name__ == "__main__":
    main()
