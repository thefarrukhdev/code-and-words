import sys
import time
import subprocess
import os

def clear_screen():
    os.system('clear')

def type_text(text, delay=0.08, newline_delay=1.0, start_time_ref=None):
    if start_time_ref is None:
        start_time_ref = time.time()
        
    duration = len(text) * delay
    
    # Calculate natural typing weights
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
        target = start_time_ref + (cumulative_weight / total_weight) * duration
        now = time.time()
        if target > now:
            time.sleep(target - now)
            
        sys.stdout.write(char)
        sys.stdout.flush()
        cumulative_weight += weights[i]
        
    target_nl = start_time_ref + duration + newline_delay
    now = time.time()
    if target_nl > now:
        time.sleep(target_nl - now)
    print()
    return target_nl

lyrics = [
    ("Umr o'tyapti, umr o'tyapti...", 0.093, 1.500),
    ("Ba'zan boy berilib bebaho onlar,", 0.062, 0.500),
    ("Bekor o'tgan damga ko'ngil ezilar.", 0.068, 0.700),
    ("", 0.000, 4.500),
    ("Essiz, essiz bolalikni qoldirib ortda,", 0.066, 0.600),
    ("Umr o'tmoqdadir daryo misoli.", 0.059, 0.600),
    ("Qoldirib, qoldirmay iz bu hayotda", 0.064, 0.300),
    ("Umr o'tmoqdadir, umr o'tmoqda.", 0.067, 0.000),
    ("", 0.000, 0.300),
    ("Qarang...", 0.100, 0.500),
    ("Keksalik mo'ralab eshik qoqmoqda,", 0.076, 1.500),
    ("Bolalik qaytadan qaytarilmoqda.", 0.081, 0.500),
    ("Bizdan erta kunga nelar qolmoqda?", 0.076, 0.500),
    ("Umr o'tmoqdadir...", 0.083, 0.500),
    ("Daryo misoli.", 0.154, 1.000)
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
    
    # Absolute path to mp3
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mp3_path = os.path.join(script_dir, "umr-o'tmoqda.mp3")

    try:
        player = subprocess.Popen(['mpv', '--no-video', mp3_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        try:
            player = subprocess.Popen(['ffplay', '-nodisp', '-autoexit', mp3_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except FileNotFoundError:
            print("Error: Neither mpv nor ffplay found. Install one of them to play audio.")
            return

    time.sleep(0.3)
    
    start_time_ref = time.time()

    for line, char_delay, nl_delay in lyrics:
        sys.stdout.write(" " * 10)
        start_time_ref = type_text(line, char_delay, nl_delay, start_time_ref)

    print("\n\n          ... umr o'tmoqda ...")
    time.sleep(1.5)
    print("\n                         [ farrukh.dev ]\n")

    player.wait()

if __name__ == "__main__":
    main()
