from tkinter import filedialog
import pygame
import sys
import tkinter as tk

# Inicializa Pygame
pygame.init()

# Tamaño de la ventana
initial_width = 800
initial_height = 600
screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
pygame.display.set_caption("Boys vs Girls Classic Live")

# Cargar ícono personalizado
icon = pygame.image.load("Icono.png").convert_alpha()
pygame.display.set_icon(icon)

# Colores
BLACK = (0, 0, 0)
PINK = (255, 192, 203)
BLUE = (0, 0, 255)

# Variables de juego
bar_position = initial_width / 2
bar_speed = initial_width * 0.025
boys_wins = 0
girls_wins = 0

# Cargar imágenes
background_img = pygame.image.load("background.jpg").convert()
boy_img = pygame.image.load("GokuNormal.png").convert_alpha()
girl_img = pygame.image.load("KeflaNormal.png").convert_alpha()
boy_attack_img = pygame.image.load("GokuAtack.png").convert_alpha()
girl_attack_img = pygame.image.load("KeflaAtack.png").convert_alpha()

# Escalar imágenes
def scale_images():
    global boy_img, girl_img, boy_attack_img, girl_attack_img
    boy_img = pygame.transform.scale(boy_img, (int(screen.get_width() * 0.2), int(screen.get_height() * 0.3)))
    girl_img = pygame.transform.scale(girl_img, (int(screen.get_width() * 0.2), int(screen.get_height() * 0.3)))
    boy_attack_img = pygame.transform.scale(boy_attack_img, (int(screen.get_width() * 0.2), int(screen.get_height() * 0.3)))
    girl_attack_img = pygame.transform.scale(girl_attack_img, (int(screen.get_width() * 0.2), int(screen.get_height() * 0.3)))

scale_images()

# Fuente de texto
font = pygame.font.Font(None, int(screen.get_width() * 0.093))

# Función para mostrar un mensaje de victoria y reiniciar el juego
def show_winner(team):
    global boys_wins, girls_wins
    if team == "Boys":
        boys_wins += 1
    elif team == "Girls":
        girls_wins += 1

    root = tk.Tk()
    root.withdraw()
    root.destroy()
    restart_game()

# Función para reiniciar el juego
def restart_game():
    global boy_img, girl_img, bar_position
    boy_img = pygame.image.load("GokuNormal.png").convert_alpha()
    girl_img = pygame.image.load("KeflaNormal.png").convert_alpha()

    boy_img = pygame.transform.scale(boy_img, (int(screen.get_width() * 0.2), int(screen.get_height() * 0.3)))
    girl_img = pygame.transform.scale(girl_img, (int(screen.get_width() * 0.2), int(screen.get_height() * 0.3)))

    bar_position = screen.get_width() / 2

# Función para cambiar la imagen seleccionada
def change_image():
    root = tk.Tk()
    root.withdraw()  # Esconder la ventana principal de tkinter

    file_path = filedialog.askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("PNG Files", "*.png"), ("JPG Files", "*.jpg"), ("JPEG Files", "*.jpeg")]
    )
    
    root.destroy()  # Destruir la ventana de Tkinter tras la selección

    if file_path:
        return file_path
    else:
        return None

# Crear menú contextual con opciones
def show_context_menu(mouse_pos):
    pygame.event.set_blocked(None)
    root = tk.Tk()
    root.withdraw()

    def menu_callback(option):
        global boy_img, girl_img, boy_attack_img, girl_attack_img, background_img
        new_img_path = change_image()

        if new_img_path:
            try:
                new_image = pygame.image.load(new_img_path).convert_alpha()
                if option == "Change Boys Image":
                    boy_img = new_image
                elif option == "Change Girls Image":
                    girl_img = new_image
                elif option == "Change Boys Attack Image":
                    boy_attack_img = new_image
                elif option == "Change Girls Attack Image":
                    girl_attack_img = new_image
                elif option == "Change Background":
                    background_img = pygame.image.load(new_img_path).convert()
                scale_images()
                # Redibujar la ventana inmediatamente
                draw_screen()
                # Cerrar la ventana del menú
                root.destroy()
            except pygame.error as e:
                print(f"Error al cargar la imagen: {e}")
                root.destroy()  # Asegurarse de cerrar la ventana incluso si hay un error

    menu = tk.Menu(root, tearoff=0)
    menu.add_command(label="Change Boys Image", command=lambda: menu_callback("Change Boys Image"))
    menu.add_command(label="Change Girls Image", command=lambda: menu_callback("Change Girls Image"))
    menu.add_command(label="Change Boys Attack Image", command=lambda: menu_callback("Change Boys Attack Image"))
    menu.add_command(label="Change Girls Attack Image", command=lambda: menu_callback("Change Girls Attack Image"))
    menu.add_command(label="Change Background", command=lambda: menu_callback("Change Background"))

    menu.tk_popup(mouse_pos[0], mouse_pos[1])

    root.mainloop()
    pygame.event.set_allowed(None)

# Función para redibujar la pantalla
def draw_screen():
    background_scaled = pygame.transform.scale(background_img, (screen.get_width(), screen.get_height()))
    screen.blit(background_scaled, (0, 0))

    pygame.draw.rect(screen, BLUE, (0, int(screen.get_height() * 0.33), bar_position, int(screen.get_height() * 0.33)))
    pygame.draw.rect(screen, PINK, (bar_position, int(screen.get_height() * 0.33), screen.get_width() - bar_position, int(screen.get_height() * 0.33)))

    if bar_position > 0:
        screen.blit(boy_img, (bar_position - boy_img.get_width(), int(screen.get_height() * 0.33)))
    if bar_position < screen.get_width():
        screen.blit(girl_img, (bar_position, int(screen.get_height() * 0.33)))

    boys_text = font.render(f"Boys: {boys_wins}", True, BLACK)
    girls_text = font.render(f"Girls: {girls_wins}", True, BLACK)
    screen.blit(boys_text, (int(screen.get_width() * 0.0625), int(screen.get_height() * 0.05)))
    screen.blit(girls_text, (int(screen.get_width() * 0.65), int(screen.get_height() * 0.05)))

    pygame.display.flip()

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            bar_speed = event.w * 0.025
            boy_img = pygame.transform.scale(boy_img, (int(event.w * 0.125), int(event.h * 0.167)))
            girl_img = pygame.transform.scale(girl_img, (int(event.w * 0.125), int(event.h * 0.167)))
            font = pygame.font.Font(None, int(event.w * 0.093))

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.mouse.get_pos()
            show_context_menu(mouse_pos)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                bar_position += bar_speed
                boy_img = boy_attack_img
            elif event.key == pygame.K_g:
                bar_position -= bar_speed
                girl_img = girl_attack_img

            if bar_position <= 0:
                show_winner("Girls")
            elif bar_position >= screen.get_width():
                show_winner("Boys")
            elif event.key == pygame.K_n:
                show_winner("Boys")
            elif event.key == pygame.K_h:
                show_winner("Girls")

    draw_screen()

pygame.quit()
sys.exit()
