import time
import sys
import os
import threading
import random

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"

HIGHLIGHT_COLOR = ""
MAIN_COLOR = ""

INACTIVE_LYRIC_COLOR = "\033[38;5;239m"

INFO_COLOR = ""

CURSOR_POS = lambda row, col: f"\033[{row};{col}H"
CLEAR_SCREEN = "\033[H\033[J"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

TEXT_WIDTH = 60
TEXT_HEIGHT = 15
terminal_width = 80
terminal_height = 24

screen_lock = threading.Lock()

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

    with screen_lock:
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

                active_highlight_color = HIGHLIGHT_COLOR
                wrapped_lines = split_and_wrap_text(line_text_to_wrap, LYRIC_WRAP_WIDTH)

                is_highlighted = line_data.get("highlight", False)

                for line_part in wrapped_lines:
                    if i == current_line_index:
                        color = BOLD + (active_highlight_color if is_highlighted or line_data.get("time", -1) == 0.0 else MAIN_COLOR)
                    
                    else:
                        color = INACTIVE_LYRIC_COLOR

                    display_line = f"{color}{line_part}{RESET}"

                    if current_display_row < TEXT_HEIGHT:
                        row_to_render = start_row + current_display_row
                        sys.stdout.write(CURSOR_POS(row_to_render, start_col))
                        sys.stdout.write(display_line)
                    
                    current_display_row += 1 

                else:
                    current_display_row += 1

            else: current_display_row += 1

    sys.stdout.flush()

def cleanup_screen():
    with screen_lock:
        sys.stdout.write(CLEAR_SCREEN)
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


CONTENT_INFO = {
    "title_lines": [
        "Nome da musica ou titulo do poema"
    ],
    "artist_lines": [
        "Nome do artista ou autor"
    ]
}

LYRICS_DATA = [
    # Dicionario com tempo (segundos) e texto ("orignal")
    {"time": 0.0, "original": "Esta é a primeira frase de exemplo do modelo."},
    {"time": 4.5, "original": "O ritmo da animação é definido por estes tempos."},
    {"time": 9.0, "original": "Adicione aqui as demais frases e seus respectivos tempos."},
    # Exemplo com destaque especifico
    {"time": 15.0, "original": "Linhas com 'highlight': true podem ter uma cor diferente.0", "highlight": True},
    {"time": 20.0, "original": "Fim."}
]

# Define a duração total para o loop da animação
TOTAL_MUSIC_DURACTION = 25.0

def start_lyrics_animation():
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.write(CLEAR_SCREEN)
    sys.stdout.flush()

    update_terminal_size()

    start_time = time.monotonic()
    current_line_index = 0

    while time.monotonic() - start_time < TOTAL_MUSIC_DURACTION:

        elapsed_time = time.monotonic() - start_time

        while current_line_index < len(LYRICS_DATA) and elapsed_time >= LYRICS_DATA[current_line_index]["time"]:
            
            current_line_index += 1

        try:
            display_index_for_display = current_line_index - 1
            
            if display_index_for_display < 0 and LYRICS_DATA and LYRICS_DATA[0]["time"] == 0.0:
                display_index_for_display = 0
            
            if display_index_for_display < 0:
                continue

            if display_index_for_display >= len(LYRICS_DATA):
                display_index_for_display = len(LYRICS_DATA) - 1
                
            display_content(display_index_for_display, LYRICS_DATA, CONTENT_INFO)

        except OSError:
            break

        next_target_time = TOTAL_MUSIC_DURACTION

        if current_line_index < len(LYRICS_DATA):
            next_target_time = LYRICS_DATA[current_line_index]["time"]

        time_to_sleep = next_target_time - (time.monotonic() - start_time)
        time_to_sleep = max(0.01, time_to_sleep)
        time.sleep(time_to_sleep)

    with screen_lock:                       
        update_terminal_size()
        sys.stdout.write(CLEAR_SCREEN)      
        final_message = "FIM DA MÚSICA 🎶 (Modelo Base)"
        
        color_code = BOLD + INFO_COLOR

        final_message_col = (terminal_width - len(final_message) - len(color_code) - len(RESET)) // 2
        final_message_row = terminal_height // 2
        
        sys.stdout.write(f"{CURSOR_POS(final_message_row, final_message_col)}{color_code}{final_message}{RESET}\n")
        artist_title = f"{CONTENT_INFO['artist_lines'][0]} - {CONTENT_INFO['title_lines'][0]}"
        sys.stdout.write(f"{CURSOR_POS(final_message_row + 1, (terminal_width - len(artist_title) - len(INFO_COLOR) - len(RESET)) // 2)}{BOLD}{INFO_COLOR}{artist_title}{RESET}\n")
        
        sys.stdout.flush()
    time.sleep(3)

if __name__ == "__main__":
    try:
        start_lyrics_animation()
        with screen_lock:
            sys.stdout.write(CLEAR_SCREEN)
            update_terminal_size()
            message = "Programa finalizado. Pressione Enter para sair."
            sys.stdout.write(CURSOR_POS(terminal_height // 2 - 1, (terminal_width - len(message)) // 2))
            sys.stdout.write(message + "\n")
            sys.stdout.flush()
        input()
    except KeyboardInterrupt:
        print("\nExibição interrompida pelo usuário.")
    except Exception as e:
        print(f"\nOcorreu um erro: {e}")
    finally:
        cleanup_screen()