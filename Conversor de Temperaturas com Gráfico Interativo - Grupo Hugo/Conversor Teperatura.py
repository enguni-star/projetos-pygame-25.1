import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 750  # Aumentei a altura para o gráfico e as diferenças
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Conversor de Temperaturas com Gráfico")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 128, 0)
ORANGE = (255, 165, 0)

# Fontes
FONT = pygame.font.Font(None, 40)
SMALL_FONT = pygame.font.Font(None, 30)

# Variáveis de entrada
celsius_input = ""
fahrenheit_input = ""
kelvin_input = ""

# Variáveis de resultado
celsius_val = 0.0
fahrenheit_val = 0.0
kelvin_val = 0.0

celsius_result_text = "Celsius: "
fahrenheit_result_text = "Fahrenheit: "
kelvin_result_text = "Kelvin: "

diff_cf_text = "Fahrenheit - Celsius: "
diff_kc_text = "Kelvin - Celsius: "
diff_kf_text = "Kelvin - Fahrenheit: "

active_input = None  # Qual campo de entrada está ativo (celsius, fahrenheit, kelvin)

# Retângulos dos campos de entrada
input_rect_celsius = pygame.Rect(50, 100, 200, 50)
input_rect_fahrenheit = pygame.Rect(300, 100, 200, 50)
input_rect_kelvin = pygame.Rect(550, 100, 200, 50)

# Retângulo do botão de converter
convert_button_rect = pygame.Rect(350, 450, 150, 60)

# Configurações do gráfico
GRAPH_START_Y = 250
BAR_HEIGHT = 30
BAR_MAX_WIDTH = 400
GRAPH_OFFSET = 100  # Offset para valores negativos no gráfico (para que a barra comece sempre à direita do 0 visual)
TEMP_SCALE_FACTOR = 1  # Quantos pixels por grau (ajuste para visualização)


# Funções de conversão
def celsius_to_fahrenheit(c):
    return (c * 9 / 5) + 32


def celsius_to_kelvin(c):
    return c + 273.15


def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9


def fahrenheit_to_kelvin(f):
    return (f - 32) * 5 / 9 + 273.15


def kelvin_to_celsius(k):
    return k - 273.15


def kelvin_to_fahrenheit(k):
    return (k - 273.15) * 9 / 5 + 32


def convert_temperatures():
    global celsius_result_text, fahrenheit_result_text, kelvin_result_text
    global celsius_val, fahrenheit_val, kelvin_val
    global diff_cf_text, diff_kc_text, diff_kf_text

    try:
        if active_input == 'celsius' and celsius_input:
            celsius_val = float(celsius_input)
            fahrenheit_val = celsius_to_fahrenheit(celsius_val)
            kelvin_val = celsius_to_kelvin(celsius_val)
        elif active_input == 'fahrenheit' and fahrenheit_input:
            fahrenheit_val = float(fahrenheit_input)
            celsius_val = fahrenheit_to_celsius(fahrenheit_val)
            kelvin_val = fahrenheit_to_kelvin(fahrenheit_val)
        elif active_input == 'kelvin' and kelvin_input:
            kelvin_val = float(kelvin_input)
            celsius_val = kelvin_to_celsius(kelvin_val)
            fahrenheit_val = kelvin_to_fahrenheit(kelvin_val)
        else:
            celsius_result_text = "Celsius: "
            fahrenheit_result_text = "Fahrenheit: "
            kelvin_result_text = "Kelvin: "
            diff_cf_text = "Fahrenheit - Celsius: "
            diff_kc_text = "Kelvin - Celsius: "
            diff_kf_text = "Kelvin - Fahrenheit: "
            celsius_val = 0.0
            fahrenheit_val = 0.0
            kelvin_val = 0.0
            print("Nenhum valor para converter ou campo ativo inválido.")
            return  # Sai da função se não houver entrada válida

        # Atualiza os textos de resultado
        celsius_result_text = f"Celsius: {celsius_val:.2f}°C"
        fahrenheit_result_text = f"Fahrenheit: {fahrenheit_val:.2f}°F"
        kelvin_result_text = f"Kelvin: {kelvin_val:.2f}K"

        # Calcula e atualiza os textos de diferença
        diff_cf_text = f"Fahrenheit - Celsius: {(fahrenheit_val - celsius_val):.2f}"
        diff_kc_text = f"Kelvin - Celsius: {(kelvin_val - celsius_val):.2f}"
        diff_kf_text = f"Kelvin - Fahrenheit: {(kelvin_val - fahrenheit_val):.2f}"

    except ValueError:
        celsius_result_text = "Celsius: Erro!"
        fahrenheit_result_text = "Fahrenheit: Erro!"
        kelvin_result_text = "Kelvin: Erro!"
        diff_cf_text = "Fahrenheit - Celsius: Erro!"
        diff_kc_text = "Kelvin - Celsius: Erro!"
        diff_kf_text = "Kelvin - Fahrenheit: Erro!"
        celsius_val = 0.0
        fahrenheit_val = 0.0
        kelvin_val = 0.0
        print("Entrada inválida. Digite apenas números.")


# Loop principal do jogo
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Verifica qual campo de entrada foi clicado
            if input_rect_celsius.collidepoint(event.pos):
                active_input = 'celsius'
                fahrenheit_input = ""  # Limpa os outros campos
                kelvin_input = ""
            elif input_rect_fahrenheit.collidepoint(event.pos):
                active_input = 'fahrenheit'
                celsius_input = ""
                kelvin_input = ""
            elif input_rect_kelvin.collidepoint(event.pos):
                active_input = 'kelvin'
                celsius_input = ""
                fahrenheit_input = ""
            elif convert_button_rect.collidepoint(event.pos):
                convert_temperatures()
            else:
                active_input = None  # Clicou fora dos campos de entrada

        if event.type == pygame.KEYDOWN:
            if active_input:
                if event.key == pygame.K_RETURN:  # Pressionou Enter
                    convert_temperatures()
                elif event.key == pygame.K_BACKSPACE:
                    if active_input == 'celsius':
                        celsius_input = celsius_input[:-1]
                    elif active_input == 'fahrenheit':
                        fahrenheit_input = fahrenheit_input[:-1]
                    elif active_input == 'kelvin':
                        kelvin_input = kelvin_input[:-1]
                else:
                    # Permite apenas dígitos, um ponto decimal e o sinal de menos (no início)
                    current_input_str = ""
                    if active_input == 'celsius':
                        current_input_str = celsius_input
                    elif active_input == 'fahrenheit':
                        current_input_str = fahrenheit_input
                    elif active_input == 'kelvin':
                        current_input_str = kelvin_input

                    if event.unicode.isdigit():
                        if active_input == 'celsius':
                            celsius_input += event.unicode
                        elif active_input == 'fahrenheit':
                            fahrenheit_input += event.unicode
                        elif active_input == 'kelvin':
                            kelvin_input += event.unicode
                    elif event.unicode == '.' and '.' not in current_input_str:
                        if active_input == 'celsius':
                            celsius_input += event.unicode
                        elif active_input == 'fahrenheit':
                            fahrenheit_input += event.unicode
                        elif active_input == 'kelvin':
                            kelvin_input += event.unicode
                    elif event.unicode == '-' and not current_input_str:  # Só permite '-' no início
                        if active_input == 'celsius':
                            celsius_input += event.unicode
                        elif active_input == 'fahrenheit':
                            fahrenheit_input += event.unicode
                        elif active_input == 'kelvin':
                            kelvin_input += event.unicode

    # Preenche o fundo da tela
    SCREEN.fill(WHITE)

    # Desenha os rótulos e campos de entrada
    # Celsius
    pygame.draw.rect(SCREEN, BLACK if active_input == 'celsius' else GRAY, input_rect_celsius, 2)
    text_surface_celsius = FONT.render("Celsius:", True, BLACK)
    SCREEN.blit(text_surface_celsius, (input_rect_celsius.x, input_rect_celsius.y - 40))
    input_text_celsius_surface = FONT.render(celsius_input, True, BLACK)
    SCREEN.blit(input_text_celsius_surface, (input_rect_celsius.x + 5, input_rect_celsius.y + 10))

    # Fahrenheit
    pygame.draw.rect(SCREEN, BLACK if active_input == 'fahrenheit' else GRAY, input_rect_fahrenheit, 2)
    text_surface_fahrenheit = FONT.render("Fahrenheit:", True, BLACK)
    SCREEN.blit(text_surface_fahrenheit, (input_rect_fahrenheit.x, input_rect_fahrenheit.y - 40))
    input_text_fahrenheit_surface = FONT.render(fahrenheit_input, True, BLACK)
    SCREEN.blit(input_text_fahrenheit_surface, (input_rect_fahrenheit.x + 5, input_rect_fahrenheit.y + 10))

    # Kelvin
    pygame.draw.rect(SCREEN, BLACK if active_input == 'kelvin' else GRAY, input_rect_kelvin, 2)
    text_surface_kelvin = FONT.render("Kelvin:", True, BLACK)
    SCREEN.blit(text_surface_kelvin, (input_rect_kelvin.x, input_rect_kelvin.y - 40))
    input_text_kelvin_surface = FONT.render(kelvin_input, True, BLACK)
    SCREEN.blit(input_text_kelvin_surface, (input_rect_kelvin.x + 5, input_rect_kelvin.y + 10))

    # Desenha o botão de converter
    pygame.draw.rect(SCREEN, BLUE, convert_button_rect)
    convert_text_surface = FONT.render("Converter", True, WHITE)
    text_rect = convert_text_surface.get_rect(center=convert_button_rect.center)
    SCREEN.blit(convert_text_surface, text_rect)

    # Exibe os resultados das conversões
    result_celsius_surface = FONT.render(celsius_result_text, True, BLACK)
    SCREEN.blit(result_celsius_surface, (50, 520))

    result_fahrenheit_surface = FONT.render(fahrenheit_result_text, True, BLACK)
    SCREEN.blit(result_fahrenheit_surface, (50, 560))

    result_kelvin_surface = FONT.render(kelvin_result_text, True, BLACK)
    SCREEN.blit(result_kelvin_surface, (50, 600))

    # Exibe as diferenças numéricas
    diff_cf_surface = SMALL_FONT.render(diff_cf_text, True, RED)
    SCREEN.blit(diff_cf_surface, (50, 640))

    diff_kc_surface = SMALL_FONT.render(diff_kc_text, True, GREEN)
    SCREEN.blit(diff_kc_surface, (50, 670))

    diff_kf_surface = SMALL_FONT.render(diff_kf_text, True, ORANGE)
    SCREEN.blit(diff_kf_surface, (50, 700))

    # --- Desenha o gráfico de barras ---
    graph_x_offset = 200  # Posição X inicial das barras
    bar_y_pos = GRAPH_START_Y

    # Desenha o rótulo do gráfico
    graph_label = FONT.render("Representação Gráfica das Temperaturas", True, BLACK)
    SCREEN.blit(graph_label, (graph_x_offset, GRAPH_START_Y - 50))


    # Função auxiliar para desenhar barras (ajustando para valores negativos e escala)
    def draw_temp_bar(screen, value, y_pos, color, label_text):
        # Para lidar com valores negativos, ajustamos o ponto de início da barra.
        # Um "ponto zero" visual é criado para que barras negativas cresçam para a esquerda
        # e positivas para a direita.
        scaled_value = value * TEMP_SCALE_FACTOR

        # O ponto central (zero) do gráfico
        center_x = graph_x_offset + GRAPH_OFFSET  # Onde o "zero" visual está

        # Se o valor for negativo, a barra desenha para a esquerda
        if scaled_value < 0:
            bar_start_x = center_x + scaled_value  # Subtrai o valor negativo para mover o início
            bar_width = abs(scaled_value)
        else:  # Se o valor for positivo, a barra desenha para a direita
            bar_start_x = center_x
            bar_width = scaled_value

        # Garante que a largura da barra não exceda o limite visual, ou seja 0
        bar_width = max(0, min(bar_width, BAR_MAX_WIDTH))

        pygame.draw.rect(screen, color, (bar_start_x, y_pos, bar_width, BAR_HEIGHT))

        # Desenha a linha de referência do zero
        pygame.draw.line(screen, BLACK, (center_x, y_pos), (center_x, y_pos + BAR_HEIGHT), 2)

        label_surface = SMALL_FONT.render(label_text, True, BLACK)
        screen.blit(label_surface, (graph_x_offset - 30, y_pos + 5))


    # Barra Celsius
    draw_temp_bar(SCREEN, celsius_val, bar_y_pos, RED, "C:")
    bar_y_pos += BAR_HEIGHT + 10  # Espaçamento entre as barras

    # Barra Fahrenheit (convertido para Celsius para comparação visual na mesma escala)
    # Para o gráfico ser comparável, é melhor usar a escala de Celsius como base visual.
    # Fahrenheit tem uma escala diferente, então precisa ser ajustado se quisermos uma comparação de "tamanho"
    # ou podemos simplesmente exibir a barra com o valor Fahrenheit, o que o torna menos comparável visualmente
    # ao lado do Celsius. Vamos exibir na sua própria escala para mostrar a magnitude.
    draw_temp_bar(SCREEN, fahrenheit_val, bar_y_pos, GREEN, "F:")
    bar_y_pos += BAR_HEIGHT + 10

    # Barra Kelvin (convertido para Celsius para comparação visual na mesma escala)
    draw_temp_bar(SCREEN, kelvin_val, bar_y_pos, BLUE, "K:")

    # Atualiza a tela
    pygame.display.flip()

# Sai do Pygame
pygame.quit()
sys.exit()