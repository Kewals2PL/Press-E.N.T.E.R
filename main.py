import time
import sys
import os
import pygame
import random
from pygame.locals import *

def play_typing_sound():
    """Funkcja odtwarzająca dźwięk maszyny do pisania."""
    sound_path = os.path.join("Assets", "Sounds", "SoundEffects", "typing_sound.wav")
    if not os.path.isfile(sound_path):
        print(f"Nie znaleziono pliku: {sound_path}")
        return
    sound = pygame.mixer.Sound(sound_path)
    sound.play()

def normalize_text(text):
    """Zamienia polskie znaki na ich odpowiedniki bez znaków diakrytycznych."""
    replacements = {
        'ą': 'a', 'ć': 'c', 'ę': 'e', 'ł': 'l', 'ń': 'n',
        'ó': 'o', 'ś': 's', 'ź': 'z', 'ż': 'z',
        'Ą': 'A', 'Ć': 'C', 'Ę': 'E', 'Ł': 'L', 'Ń': 'N',
        'Ó': 'O', 'Ś': 'S', 'Ź': 'Z', 'Ż': 'Z'
    }
    return ''.join(replacements.get(char, char) for char in text)

def display_text_with_typing(screen, text, font, x, y, line_height=40):
    """Wyświetlanie tekstu linia po linii z efektem pisania i dźwiękiem."""
    text = normalize_text(text)
    lines = text.split("\n")
    for i, line in enumerate(lines):
        for j in range(len(line) + 1):
            rendered_text = font.render(line[:j], True, (0, 255, 0))
            screen.fill((0, 0, 0))
            apply_vhs_effect(screen)
            # Rysujemy wcześniej wyświetlone linie w całości
            for k in range(i):
                previous_line = font.render(lines[k], True, (0, 255, 0))
                screen.blit(previous_line, (x, y + k * line_height))
            # Rysujemy aktualnie wypisywaną linię (do j znaków)
            screen.blit(rendered_text, (x, y + i * line_height))
            pygame.display.flip()
            play_typing_sound()
            pygame.time.delay(50)
    # Po zakończeniu pisania możemy wywołać krótką animację VHS
    animate_vhs(screen, duration=500)

def apply_vhs_effect(screen):
    """Dodaje animowany efekt VHS/zakłóceń na ekran."""
    for _ in range(10):
        x = random.randint(0, screen.get_width())
        y = random.randint(0, screen.get_height())
        w = random.randint(10, 30)
        h = random.randint(2, 6)
        color = (random.randint(0, 50), random.randint(100, 255), random.randint(0, 50))
        pygame.draw.rect(screen, color, (x, y, w, h))

def animate_vhs(screen, duration=500):
    """Uruchamia animację VHS przez określony czas (ms)."""
    start_time = pygame.time.get_ticks()
    while pygame.time.get_ticks() - start_time < duration:
        apply_vhs_effect(screen)
        pygame.display.flip()
        pygame.time.delay(50)

def toggle_fullscreen(screen):
    """Przełącza między trybem pełnoekranowym i okienkowym."""
    is_fullscreen = screen.get_flags() & FULLSCREEN
    if is_fullscreen:
        pygame.display.set_mode((800, 600))  # Tryb okienkowy
    else:
        pygame.display.set_mode((0, 0), FULLSCREEN)  # Pełny ekran

def options_menu(screen, font):
    """Wyświetla menu opcji z możliwością nawigacji strzałkami."""
    fonts = [
        pygame.font.Font(pygame.font.match_font('couriernew'), 36),
        pygame.font.Font(os.path.join("Assets", "Fonts", "Sixtyfour.ttf"), 36)
    ]
    font_names = ["Courier New", "Sixtyfour"]
    current_font_index = 0

    options = [
        "Pełny ekran / Okienko: Przełącz tryb wyświetlania.",
        f"Czcionka: {font_names[current_font_index]} - Przełącz czcionkę.",
        "Efekt VHS: WŁĄCZONY - Przełącz na wyłączenie efektu wizualnego.",
        "Powrót - Powrót do głównego menu."
    ]
    selected_index = 0
    vhs_effect_enabled = True

    running = True
    while running:
        screen.fill((0, 0, 0))
        for i, option in enumerate(options):
            color = (0, 255, 0) if i == selected_index else (100, 100, 100)
            rendered_text = font.render(option, True, color)
            screen.blit(rendered_text, (20, 150 + i * 40))

        if vhs_effect_enabled:
            apply_vhs_effect(screen)
        pygame.display.flip()
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_index = (selected_index - 1) % len(options)
                elif event.key == K_DOWN:
                    selected_index = (selected_index + 1) % len(options)
                elif event.key == K_RETURN:
                    if selected_index == 0:
                        toggle_fullscreen(screen)
                    elif selected_index == 1:
                        current_font_index = (current_font_index + 1) % len(fonts)
                        options[1] = f"Czcionka: {font_names[current_font_index]} - Przełącz czcionkę."
                    elif selected_index == 2:
                        vhs_effect_enabled = not vhs_effect_enabled
                        options[2] = f"Efekt VHS: {'WŁĄCZONY' if vhs_effect_enabled else 'WYŁĄCZONY'} - Przełącz na {'wyłączenie' if vhs_effect_enabled else 'włączenie'} efektu wizualnego."
                    elif selected_index == 3:
                        running = False

def main_menu(screen, font):
    """Wyświetla główne menu gry."""
    screen.fill((0, 0, 0))
    apply_vhs_effect(screen)
    text_to_display = (
        "Witaj w grze 'Press ENTER'.\n"
        "1. Rozpocznij grę\n"
        "2. Opcje\n"
        "3. Wyjdź"
    )
    # Najpierw wyświetlamy napis z efektem pisania
    display_text_with_typing(screen, text_to_display, font, 20, 150)

    lines = text_to_display.split("\n")

    running = True
    while running:
        screen.fill((0, 0, 0))
        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, (0, 255, 0))
            screen.blit(rendered_text, (20, 150 + i * 40))

        apply_vhs_effect(screen)
        pygame.display.flip()
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    game_loop(screen, font)  # Przejście do głównej pętli gry
                    running = False
                elif event.key == K_2:
                    options_menu(screen, font)  # Przejście do opcji
                elif event.key == K_3:
                    pygame.quit()
                    sys.exit()

def game_loop(screen, font):
    """Pętla główna gry obsługująca wyświetlanie i interakcje."""
    text_to_display = (
        "Witaj, Prezydencie Sylestii.\n"
        "Obar, nasz sąsiedni kraj, wypowiedział nam wojnę nuklearną.\n"
        "Twoje decyzje zadecydują o losie naszego świata.\n"
        "Naciśnij ENTER, aby kontynuować..."
    )

    screen.fill((0, 0, 0))
    apply_vhs_effect(screen)
    display_text_with_typing(screen, text_to_display, font, 20, 150)

    lines = text_to_display.split("\n")

    running = True
    while running:
        screen.fill((0, 0, 0))
        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, (0, 255, 0))
            screen.blit(rendered_text, (20, 150 + i * 40))

        apply_vhs_effect(screen)
        pygame.display.flip()
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key == K_RETURN:
                running = False

    middle_story(screen, font)

def middle_story(screen, font):
    """Część gry obsługująca fabułę i decyzje gracza."""
    text_to_display = (
        "Nadchodzi wiadomość od generała armii:\n"
        "'Panie Prezydencie, mamy trzy opcje działania:\n"
        "1. Uderzyć nuklearnie jako pierwsi.\n"
        "2. Spróbować negocjacji.\n"
        "3. Czekać na ich ruch.'\n"
        "Wybierz opcję:"
    )
    display_text_with_typing(screen, text_to_display, font, 20, 150)

    lines = text_to_display.split("\n")

    choice_made = False
    while not choice_made:
        screen.fill((0, 0, 0))
        for i, line in enumerate(lines):
            rendered_text = font.render(line, True, (0, 255, 0))
            screen.blit(rendered_text, (20, 150 + i * 40))

        apply_vhs_effect(screen)
        pygame.display.flip()
        pygame.time.delay(50)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_1:
                    ending_nuclear_attack(screen, font)
                    choice_made = True
                elif event.key == K_2:
                    ending_negotiations(screen, font)
                    choice_made = True
                elif event.key == K_3:
                    ending_waiting(screen, font)
                    choice_made = True

def ending_nuclear_attack(screen, font):
    """Zakończenie dla ataku nuklearnego."""
    text = (
        "Zdecydowałeś się na uderzenie nuklearne jako pierwsi...\n"
        "Nasze rakiety uderzyły w strategiczne cele w Obarze.\n"
        "Obar odpowiedział pełnoskalowym kontratakiem nuklearnym.\n"
        "Świat pogrążył się w nuklearnej apokalipsie.\n"
        "KONIEC GRY: Ziemia została zniszczona."
    )
    display_text_with_typing(screen, text, font, 20, 150)
    wait_for_exit()

def ending_negotiations(screen, font):
    """Zakończenie dla negocjacji."""
    text = (
        "Zdecydowałeś się na negocjacje z Obarem...\n"
        "Wysłaliśmy naszych dyplomatów, aby spotkali się z liderem Obary.\n"
        "Negocjacje były napięte, ale udało się osiągnąć porozumienie.\n"
        "KONIEC GRY: Uratowałeś świat."
    )
    display_text_with_typing(screen, text, font, 20, 150)
    wait_for_exit()

def ending_waiting(screen, font):
    """Zakończenie dla czekania."""
    text = (
        "Zdecydowałeś się czekać na ruch Obary...\n"
        "Obar rozpoczął atak nuklearny. Nasze miasta zostały zniszczone.\n"
        "Nie byliśmy przygotowani na kontratak. Ludzkość poniosła ogromne straty.\n"
        "KONIEC GRY: Twoja bezczynność doprowadziła do katastrofy."
    )
    display_text_with_typing(screen, text, font, 20, 150)
    wait_for_exit()

def wait_for_exit():
    """Czekaj na zakończenie gry z animacją w tle."""
    screen = pygame.display.get_surface()
    running = True
    while running:
        animate_vhs(screen, duration=100)
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

if __name__ == "__main__":
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((0, 0), FULLSCREEN)  # Domyślnie pełny ekran
    pygame.display.set_caption("Press ENTER")
    font = pygame.font.Font(pygame.font.match_font('couriernew'), 36)
    main_menu(screen, font)
