import tkinter as tk
from tkinter import messagebox
import random

class JogoAdivinhacao:
    def __init__(self, master):
        self.master = master
        master.title("🎯 Jogo da Adivinhação")
        master.geometry("450x300")
        master.configure(bg="#FFC0CB")  # rosa claro

        self.numero_secreto = random.randint(1, 100)
        self.tentativas = 0
        self.max_tentativas = 10
        self.palpites_usados = set()

        self.label = tk.Label(master, text="🎯 Digite um número de 1 a 100:", bg="#FFC0CB", fg="blue", font=("Arial", 14))
        self.label.pack(pady=10)

        self.entrada = tk.Entry(master, font=("Arial", 14))
        self.entrada.pack()

        self.botao = tk.Button(master, text="🚀 Enviar", command=self.verificar_palpite, bg="blue", fg="white", font=("Arial", 12))
        self.botao.pack(pady=10)

        self.mensagem = tk.Label(master, text="", bg="#FFC0CB", fg="blue", font=("Arial", 12))
        self.mensagem.pack()

        # Permitir enviar com a tecla Enter
        master.bind('<Return>', self.verificar_palpite)

    def verificar_palpite(self, event=None):
        palpite_str = self.entrada.get()
        if not palpite_str.isdigit():
            self.mensagem.config(text="❌ Digite um número válido!", fg="red")
            return

        palpite = int(palpite_str)

        if palpite < 1 or palpite > 100:
            self.mensagem.config(text="❌ Número deve estar entre 1 e 100.", fg="red")
            return

        if palpite in self.palpites_usados:
            self.mensagem.config(text="⚠️ Você já tentou esse número! Tente outro.", fg="red")
            return

        self.palpites_usados.add(palpite)
        self.tentativas += 1

        if palpite < self.numero_secreto:
            self.mensagem.config(text=f"📈 Dica: O número é MAIOR que {palpite}!", fg="blue")
        elif palpite > self.numero_secreto:
            self.mensagem.config(text=f"📉 Dica: O número é MENOR que {palpite}!", fg="blue")
        else:
            messagebox.showinfo("🎉 PARABÉNS!", f"✨ Você acertou o número {self.numero_secreto} em {self.tentativas} tentativas! ✨")
            self.master.destroy()
            return

        tent_restantes = self.max_tentativas - self.tentativas
        self.mensagem.config(text=self.mensagem.cget("text") + f"\n⏳ Tentativas restantes: {tent_restantes}", fg="blue")

        if tent_restantes == 0:
            messagebox.showinfo("💀 FIM DE JOGO!", f"Você perdeu! O número era {self.numero_secreto}.")
            self.master.destroy()
            return

        self.entrada.delete(0, tk.END)  # limpa a entrada para o próximo palpite

if __name__ == "__main__":
    root = tk.Tk()
    jogo = JogoAdivinhacao (root)
    root.mainloop()