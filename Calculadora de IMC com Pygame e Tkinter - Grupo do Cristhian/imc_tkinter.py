import tkinter as tk
from tkinter import ttk, TclError, messagebox
from PIL import Image, ImageTk

# --- CONFIGURAÇÕES DE DESIGN ---
COR_FUNDO = "#e0f7fa"
COR_PAINEL = "#b2ebf2"
COR_TEXTO = "#004d40"
COR_RESULTADO_IDEAL = "#00796b"
COR_RESULTADO_ALERTA = "#f57c00"
COR_RESULTADO_OBESO = "#d32f2f"


class CalculadoraIMC_Final:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora de IMC")
        self.root.geometry("450x480")
        self.root.resizable(False, False)
        self.root.config(bg=COR_FUNDO)

        style = ttk.Style()
        style.configure("TScale", background=COR_FUNDO)

        # Carrega as imagens que foram processadas pelo script ajudante
        self.carregar_imagens_padronizadas()

        # Cria a interface final
        self.criar_layout()

        # Faz o cálculo inicial ao abrir o app
        self.calcular_imc()

    def carregar_imagens_padronizadas(self):
        """Carrega as imagens que foram processadas e padronizadas."""
        self.imagens_imc = {}
        # Nomes das novas imagens
        nomes_map = {
            "abaixo": "abaixo_final.png",
            "ideal": "ideal_final.png",
            "sobrepeso": "sobrepeso_final.png",
            "obesidade": "obesidade_final.png"
        }

        for chave, nome_arquivo in nomes_map.items():
            try:
                img_original = Image.open(nome_arquivo)
                self.imagens_imc[chave] = ImageTk.PhotoImage(img_original)
            except FileNotFoundError:
                messagebox.showerror("Erro de Arquivo",
                                     f"A imagem processada '{nome_arquivo}' não foi encontrada.\n\n"
                                     "Por favor, rode o script 'processador_de_imagens.py' primeiro.")
                self.root.destroy()
                return

    def criar_layout(self):
        """Cria a estrutura da aplicação com grid para posicionamento preciso."""
        # --- Frame Esquerdo (Entradas) ---
        frame_esquerdo = tk.Frame(self.root, bg=COR_FUNDO, padx=20, pady=20)
        frame_esquerdo.pack(side="left", fill="both", expand=True)

        tk.Label(frame_esquerdo, text="Seu Peso (kg)", font=("Arial", 14), bg=COR_FUNDO, fg=COR_TEXTO).pack(
            pady=(0, 10))
        self.entry_peso = ttk.Entry(frame_esquerdo, font=("Arial", 16), width=6, justify="center")
        self.entry_peso.pack(pady=5)
        self.entry_peso.insert(0, "70.5")
        self.entry_peso.bind("<KeyRelease>", self.calcular_imc)

        ttk.Separator(frame_esquerdo, orient="horizontal").pack(fill="x", pady=20)

        tk.Label(frame_esquerdo, text="Sua Altura (cm)", font=("Arial", 14), bg=COR_FUNDO, fg=COR_TEXTO).pack(pady=10)
        self.altura_var = tk.IntVar(value=170)
        self.slider_altura = ttk.Scale(frame_esquerdo, from_=100, to=220, orient="horizontal", length=200,
                                       variable=self.altura_var, command=self.calcular_imc)
        self.slider_altura.pack(pady=5)
        self.label_altura_valor = tk.Label(frame_esquerdo, text="170 cm", font=("Arial", 16, "bold"), bg=COR_FUNDO,
                                           fg=COR_TEXTO)
        self.label_altura_valor.pack(pady=10)

        # --- Frame Direito (Resultado com Grid Layout) ---
        frame_direito = tk.Frame(self.root, bg=COR_PAINEL, padx=20, pady=20)
        frame_direito.pack(side="right", fill="both", expand=True)

        # Configura a grade para ter uma coluna centralizada
        frame_direito.columnconfigure(0, weight=1)

        # Linha 0: Título
        tk.Label(frame_direito, text="Resultado", font=("Arial", 14), bg=COR_PAINEL, fg=COR_TEXTO).grid(row=0, column=0,
                                                                                                        pady=(0, 10))

        # Linha 1: Valor do IMC
        self.label_imc_valor = tk.Label(frame_direito, text="24.1", font=("Arial", 48, "bold"), bg=COR_PAINEL,
                                        fg=COR_RESULTADO_IDEAL)
        self.label_imc_valor.grid(row=1, column=0, pady=5)

        # Linha 2: Imagem (posicionada de forma estável)
        self.label_imagem = tk.Label(frame_direito, bg=COR_PAINEL)
        self.label_imagem.grid(row=2, column=0, pady=10)

        # Linha 3: Categoria do IMC
        self.label_imc_categoria = tk.Label(frame_direito, text="Peso Ideal", font=("Arial", 16), bg=COR_PAINEL,
                                            fg=COR_RESULTADO_IDEAL)
        self.label_imc_categoria.grid(row=3, column=0, pady=5)

    def calcular_imc(self, _=None):
        """Calcula e exibe o resultado do IMC no painel direito."""
        try:
            peso_str = self.entry_peso.get().replace(',', '.', 1)
            if not peso_str or not peso_str.replace('.', '', 1).isdigit(): return

            peso = float(peso_str)
            altura_cm = self.altura_var.get()
            self.label_altura_valor.config(text=f"{int(altura_cm)} cm")

            if altura_cm == 0: return

            altura_m = altura_cm / 100
            imc = peso / (altura_m ** 2)

            if imc < 18.5:
                categoria, cor, chave_imagem = "Abaixo do peso", COR_RESULTADO_ALERTA, "abaixo"
            elif 18.5 <= imc < 25:
                categoria, cor, chave_imagem = "Peso Ideal", COR_RESULTADO_IDEAL, "ideal"
            elif 25 <= imc < 30:
                categoria, cor, chave_imagem = "Sobrepeso", COR_RESULTADO_ALERTA, "sobrepeso"
            else:
                categoria, cor, chave_imagem = "Obesidade", COR_RESULTADO_OBESO, "obesidade"

            self.label_imc_valor.config(text=f"{imc:.1f}", fg=cor)
            self.label_imc_categoria.config(text=categoria, fg=cor)

            # Atualiza a imagem
            imagem_para_mostrar = self.imagens_imc[chave_imagem]
            self.label_imagem.config(image=imagem_para_mostrar)
            self.label_imagem.image = imagem_para_mostrar

        except (ValueError, TclError):
            pass


if __name__ == "__main__":
    janela = tk.Tk()
    app = CalculadoraIMC_Final(janela)
    janela.mainloop()