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
        elif char in ['.', '?', '!', ':']:
            weights.append(2.0 if prev_char == '.' else 6.0)
        elif char in ['"', "'", "’", "‘"]:
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
    (0.15, "Go'zalligiga qarang bu hadisi qudsiyda.", 1.95),
    (2.68, "Alloh taolo aytadi:", 4.10),
    (4.25, "\"Bandam, sen Men uchun Men xohlaganday bo'lgin,", 9.16),
    (9.64, "Men ham sen uchun sen xohlaganday bo'laman.", 12.80),
    (12.88, "Senga nima foydali ekanini Menga gapirma.", 15.70),
    (16.32, "Sen ham xohlaysan, Men ham xohlayman.", 19.55),
    (19.60, "Agar sen Men xohlagan ishda Menga taslim bo'lsang,", 24.50),
    (24.56, "sen istagan ishingda Men senga kifoya qilaman\".", 27.60),
    (27.70, "\"Men aytganday qilib bo'l deyapti,", 29.50),
    (29.60, "qolgan ishini Mening zimmamga yuklab qo'y deyapti.", 32.10),
    (32.25, "Tushunarlimi?", 33.30),
    (33.40, "\"Tavakkal qildik, bo'lmadi u\" desa,", 35.30),
    (35.40, "sen Alloh xohlaganday bo'lmading shu ishda.", 37.35),
    (37.40, "Tavakkaldan oldin sababini ham qilish kerak.", 39.50),
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
        if i in [2, 8, 11]:
            print()

        line_start_ref = t_zero + start_t
        duration = end_t - start_t

        sys.stdout.write(" " * 10)
        type_text(text, duration, line_start_ref)

    # Yakuniy mualliflik imzosi
    signature_target = t_zero + 39.6
    now = time.time()
    if signature_target > now:
        time.sleep(signature_target - now)

    print("\n\n                         <the.farrukh.dev/>\n")

    player.wait()

if __name__ == "__main__":
    main()
