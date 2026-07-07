import time
import sys
import os

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

HIGHLIGHT_COLOR = "\033[95m"
MAIN_COLOR = "\033[97m"

INACTIVE_LYRIC_COLOR = "\033[38;5;239m"

INFO_COLOR = "\033[36m"

CURSOR_POS = lambda row, col: f"\033[{row};{col}H"
CLEAR_SCREEN = "\033[H\033[J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

TEXT_WIDTH = 60
TEXT_HEIGHT = 15
terminal_width = 80
terminal_height = 24

def update_terminal_size():

    global terminal_width, terminal_height
    try:
        current_term_width, current_term_height = os.get_terminal_size()
        terminal_width = max(80, current_term_width)
        terminal_height = max(20, current_term_height)

    except OSError:
        pass

def split_and_wrap_text(text, max_width):

    parts_by_newline = text.split('\n')
    wrapped_lines = []

    for part in parts_by_newline:
        words = part.split()
        current_line = []
        current_line_length = 0

        for word in words:
            if current_line_length + len(word) + (1 if current_line else 0) <= max_width:
                current_line.append(word)
                current_line_length += len(word) + (1 if current_line else 0)

            else:
                wrapped_lines.append(" ".join(current_line))
                current_line = [word]
                current_line_length = len(word)

        if current_line:
            wrapped_lines.append(" ".join(current_line))

    return wrapped_lines

def display_content(current_line_index, lyrics_data, content_info):

    start_col = 2
    start_row = 1
    LYRIC_WRAP_WIDTH = TEXT_WIDTH
    current_display_row = 0

    sys.stdout.write(CLEAR_SCREEN)

    for title_part_line in content_info["title_lines"]:
        title_wrapped = split_and_wrap_text(title_part_line, LYRIC_WRAP_WIDTH)

        for line in title_wrapped:
            if current_display_row < TEXT_HEIGHT:
                sys.stdout.write(CURSOR_POS(start_row + current_display_row, start_col))
                sys.stdout.write(f"{BOLD}{INFO_COLOR}{line}{RESET}")
                current_display_row += 1

    for info_part_line in content_info["artist_lines"]:
        info_wrapped = split_and_wrap_text(info_part_line, LYRIC_WRAP_WIDTH)

        for line in info_wrapped:
            if current_display_row < TEXT_HEIGHT:
                sys.stdout.write(CURSOR_POS(start_row + current_display_row, start_col))
                sys.stdout.write(f"{BOLD}{INFO_COLOR}{line}{RESET}")
                current_display_row += 1

    if current_display_row < TEXT_HEIGHT:
        current_display_row += 1

    start_lyric_index = current_line_index
    lines_to_show = TEXT_HEIGHT - current_display_row
    end_lyric_index = start_lyric_index + lines_to_show

    for i in range(start_lyric_index, end_lyric_index):
        if i >= 0 and i < len(lyrics_data):
            line_data = lyrics_data[i]
            line_text_to_wrap = line_data["original"]

            wrapped_lines = split_and_wrap_text(line_text_to_wrap, LYRIC_WRAP_WIDTH)
            is_highlighted = line_data.get("highlight", False)

            for line_part in wrapped_lines:
                if i == current_line_index:
                    color = BOLD + (HIGHLIGHT_COLOR if is_highlighted else MAIN_COLOR)

                else:
                    color = INACTIVE_LYRIC_COLOR

                if current_display_row < TEXT_HEIGHT:
                    sys.stdout.write(CURSOR_POS(start_row + current_display_row, start_col))
                    sys.stdout.write(f"{color}{line_part}{RESET}")

                current_display_row += 1

            # linha em branco de espaçamento entre versos
            current_display_row += 1

        else: current_display_row += 1

    sys.stdout.flush()

def cleanup_screen():
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.write(SHOW_CURSOR)
    sys.stdout.flush()


CONTENT_INFO = {
    "title_lines": [
        "Self Aware"
    ],
    "artist_lines": [
        "Temper City"
    ]
}

LYRICS_DATA = [
    # Letra sincronizada gerada de self_aware.lrc (tempos em segundos)
    {"time": 13.7, "original": "(Oh)"},
    {"time": 15.06, "original": "No smoke with no fire"},
    {"time": 17.52, "original": "No silence if there's no sound"},
    {"time": 20.67, "original": "One way or another"},
    {"time": 22.93, "original": "You're going to put me out"},
    {"time": 26.78, "original": "Drinks flowing like water"},
    {"time": 29.61, "original": "Too drunk to turn off the light"},
    {"time": 32.84, "original": "Stay under the covers"},
    {"time": 35.42, "original": "Who knows how we'll end the night"},
    {"time": 38.31, "original": "Just don't hang your hopes on me"},
    {"time": 41.66, "original": "I wanna feel something"},
    {"time": 44.36, "original": "God, you look so pretty"},
    {"time": 46.55, "original": "When you tell me that you love me"},
    {"time": 50.41, "original": "I wish that I could lie"},
    {"time": 53.77, "original": "But my mind gets in the way"},
    {"time": 56.72, "original": "I know you think that I'm"},
    {"time": 59.79, "original": "Always way too self-aware", "highlight": True},
    {"time": 62.43, "original": "Oh, we could never be together"},
    {"time": 65.52, "original": "But it's nice to play pretend"},
    {"time": 68.67, "original": "I wish that I could lie"},
    {"time": 71.6, "original": "But I'm way too self-aware", "highlight": True},
    {"time": 74.4, "original": "Mood swings like the weather"},
    {"time": 76.11, "original": "Body's under pressure"},
    {"time": 77.72, "original": "Oh, I love the way you're using your imagination"},
    {"time": 80.62, "original": "Laws of attraction"},
    {"time": 82.1, "original": "Put 'em into practice"},
    {"time": 85.79, "original": "Just don't hang your hopes on me"},
    {"time": 89.16, "original": "I wanna feel something"},
    {"time": 91.76, "original": "God, you look so pretty"},
    {"time": 93.94, "original": "When you tell me that you love me"},
    {"time": 98.31, "original": "I wish that I could lie"},
    {"time": 101.47, "original": "But my mind gets in the way"},
    {"time": 104.31, "original": "I know you think that I'm"},
    {"time": 107.12, "original": "Always way too self-aware", "highlight": True},
    {"time": 109.94, "original": "Oh, we could never be together"},
    {"time": 113.34, "original": "But it's nice to play pretend"},
    {"time": 116.21, "original": "I wish that I could lie"},
    {"time": 119.25, "original": "But I'm way too self-aware", "highlight": True},
    {"time": 123.53, "original": ""},
    {"time": 133.28, "original": "Just don't hang your hopes on me"},
    {"time": 136.63, "original": "I wanna feel something"},
    {"time": 139.26, "original": "God, you look so pretty"},
    {"time": 141.26, "original": "When you tell me that you love me"},
    {"time": 146.64, "original": ""},
    {"time": 148.69, "original": "I wish that I could lie"},
    {"time": 151.82, "original": "But my mind gets in the way"},
    {"time": 154.86, "original": "I know you think that I'm"},
    {"time": 157.57, "original": "Always way too self-aware", "highlight": True},
    {"time": 160.25, "original": "Oh, we could never be together"},
    {"time": 163.46, "original": "But it's nice to play pretend"},
    {"time": 166.4, "original": "I wish that I could lie"},
    {"time": 169.57, "original": "But I'm way too self-aware", "highlight": True},
    {"time": 171.98, "original": ""}
]

# Define a duração total para o loop da animação
TOTAL_MUSIC_DURATION = 181.0

def start_lyrics_animation():
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()

    update_terminal_size()

    start_time = time.monotonic()
    current_line_index = 0

    while time.monotonic() - start_time < TOTAL_MUSIC_DURATION:

        elapsed_time = time.monotonic() - start_time

        while current_line_index < len(LYRICS_DATA) and elapsed_time >= LYRICS_DATA[current_line_index]["time"]:

            current_line_index += 1

        try:
            # antes da 1a linha o índice fica em -1: mostra só título e versos futuros
            display_index_for_display = current_line_index - 1

            if display_index_for_display >= len(LYRICS_DATA):
                display_index_for_display = len(LYRICS_DATA) - 1

            display_content(display_index_for_display, LYRICS_DATA, CONTENT_INFO)

        except OSError:
            break

        next_target_time = TOTAL_MUSIC_DURATION

        if current_line_index < len(LYRICS_DATA):
            next_target_time = LYRICS_DATA[current_line_index]["time"]

        time_to_sleep = next_target_time - (time.monotonic() - start_time)
        time_to_sleep = max(0.01, time_to_sleep)
        time.sleep(time_to_sleep)

    update_terminal_size()
    sys.stdout.write(CLEAR_SCREEN)
    final_message = "FIM DA MÚSICA 🎶"

    final_message_col = max(1, (terminal_width - len(final_message)) // 2)
    final_message_row = terminal_height // 2

    sys.stdout.write(f"{CURSOR_POS(final_message_row, final_message_col)}{BOLD}{INFO_COLOR}{final_message}{RESET}\n")
    artist_title = f"{CONTENT_INFO['artist_lines'][0]} - {CONTENT_INFO['title_lines'][0]}"
    artist_title_col = max(1, (terminal_width - len(artist_title)) // 2)
    sys.stdout.write(f"{CURSOR_POS(final_message_row + 1, artist_title_col)}{BOLD}{INFO_COLOR}{artist_title}{RESET}\n")

    sys.stdout.flush()
    time.sleep(3)

if __name__ == "__main__":
    try: # habilita a interpretação de códigos ANSI no console do Windows
        start_lyrics_animation()
        sys.stdout.write(CLEAR_SCREEN)
        update_terminal_size()
        message = "Programa finalizado. Pressione Enter para sair."
        sys.stdout.write(CURSOR_POS(terminal_height // 2 - 1, max(1, (terminal_width - len(message)) // 2)))
        sys.stdout.write(message + "\n")
        sys.stdout.flush()
        input()
    except KeyboardInterrupt:
        print("\nExibição interrompida pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
    finally:
        cleanup_screen()
