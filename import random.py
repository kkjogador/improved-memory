import tkinter as tk
from tkinter import messagebox
import random
import pygame
import sys

class JogoDesafios:
    def __init__(self, root):
        self.root = root
        self.root.title("Jogo de Desafios")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")
        
        # Label de Progresso
        self.progresso_label = tk.Label(self.root, text="Progresso: Desafio 1", font=("Arial", 16), bg="#f0f0f0", fg="#333")
        self.progresso_label.pack(pady=20)
        
        # Botão para iniciar o jogo
        self.botao_inicio = tk.Button(self.root, text="Iniciar Desafios", font=("Arial", 14), bg="#4CAF50", fg="white", command=self.iniciar_jogo)
        self.botao_inicio.pack(pady=30, padx=20, fill="both")
        
        # Lista de perguntas
        self.perguntas = [
            {"pergunta": "Quantos meses tem 28 dias?", "opcoes": ["1", "12", "6", "Nenhum"], "resposta_correta": "12"},
            {"pergunta": "Qual é o maior planeta do Sistema Solar?", "opcoes": ["Terra", "Marte", "Júpiter", "Saturno"], "resposta_correta": "Júpiter"},
            {"pergunta": "Quem pintou a Mona Lisa?", "opcoes": ["Picasso", "Van Gogh", "Da Vinci", "Michelangelo"], "resposta_correta": "Da Vinci"},
            {"pergunta": "Qual é a capital da França?", "opcoes": ["Berlim", "Paris", "Madri", "Roma"], "resposta_correta": "Paris"},
            {"pergunta": "Quanto é 5 + 7?", "opcoes": ["12", "10", "11", "13"], "resposta_correta": "12"},
            {"pergunta": "Em que ano o homem chegou à Lua?", "opcoes": ["1969", "1950", "1971", "1980"], "resposta_correta": "1969"}
        ]
        
    def iniciar_jogo(self):
        self.botao_inicio.pack_forget()  # Esconde o botão de iniciar
        self.desafios = [self.perguntas_e_respostas, self.iniciar_labirinto, self.iniciar_jogo_memoria]
        random.shuffle(self.desafios)
        self.progresso_label.config(text="Progresso: Desafio 1")
        self.proximo_desafio()

    def proximo_desafio(self):
        if len(self.desafios) > 0:
            desafio = self.desafios.pop()
            desafio()

    def perguntas_e_respostas(self):
        self.pergunta_atual = random.choice(self.perguntas)
        self.pergunta_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.pergunta_frame.pack(pady=20)
        
        self.pergunta_label = tk.Label(self.pergunta_frame, text=self.pergunta_atual["pergunta"], font=("Arial", 16), bg="#f0f0f0")
        self.pergunta_label.pack(pady=10)
        
        self.botao_respostas = []
        for opcao in self.pergunta_atual["opcoes"]:
            botao = tk.Button(self.pergunta_frame, text=opcao, font=("Arial", 12), bg="#2196F3", fg="white", command=lambda opcao=opcao: self.verificar_resposta(opcao))
            botao.pack(pady=5, padx=20, fill="both")
            self.botao_respostas.append(botao)

    def verificar_resposta(self, resposta):
        for botao in self.botao_respostas:
            botao.pack_forget()  # Esconde os botões após a escolha
        if resposta == self.pergunta_atual["resposta_correta"]:
            self.progresso_label.config(text="Progresso: Desafio 2")
            self.proximo_desafio()
        else:
            messagebox.showerror("Erro", "Resposta errada! Tente denovo.")
            self.pergunta_frame.pack_forget()
            self.perguntas_e_respostas()

    def iniciar_labirinto(self):
        pygame.init()
        largura, altura = 400, 400
        tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("Desafio do Labirinto")
        branco = (255, 255, 255)
        preto = (0, 0, 0)
        azul = (0, 0, 255)
        jogador = pygame.Rect(50, 50, 20, 20)
        saida = pygame.Rect(350, 350, 20, 20)
        paredes = [pygame.Rect(100, 0, 20, 300), pygame.Rect(200, 100, 20, 300)]
        clock = pygame.time.Clock()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            teclas = pygame.key.get_pressed()
            if teclas[pygame.K_LEFT]:
                jogador.x -= 5
            if teclas[pygame.K_RIGHT]:
                jogador.x += 5
            if teclas[pygame.K_UP]:
                jogador.y -= 5
            if teclas[pygame.K_DOWN]:
                jogador.y += 5

            tela.fill(branco)
            pygame.draw.rect(tela, azul, jogador)
            pygame.draw.rect(tela, (0, 255, 0), saida)

            for parede in paredes:
                pygame.draw.rect(tela, preto, parede)
                if jogador.colliderect(parede):
                    jogador.x, jogador.y = 50, 50

            if jogador.colliderect(saida):
                pygame.quit()
                self.progresso_label.config(text="Progresso: Desafio 3")
                self.proximo_desafio()
                return

            pygame.display.flip()
            clock.tick(30)

    def iniciar_jogo_memoria(self):
        self.janela_memoria = tk.Toplevel(self.root)
        self.janela_memoria.title("Jogo da Memória")
        self.janela_memoria.geometry("400x400")

        cartas = list("AABBCCDDEEFF")
        random.shuffle(cartas)
        botoes = []
        primeira_carta = []
        pares_encontrados = []

        def revelar_carta(linha, coluna, botao):
            if botao["text"] == "" and len(primeira_carta) < 2:
                botao["text"] = cartas[linha * 4 + coluna]
                primeira_carta.append((linha, coluna, botao))
                if len(primeira_carta) == 2:
                    self.janela_memoria.after(500, verificar_pares)

        def verificar_pares():
            nonlocal primeira_carta, pares_encontrados
            c1, c2 = primeira_carta
            if cartas[c1[0] * 4 + c1[1]] == cartas[c2[0] * 4 + c2[1]]:
                pares_encontrados.append(cartas[c1[0] * 4 + c1[1]])
            else:
                c1[2]["text"] = ""
                c2[2]["text"] = ""
            primeira_carta = []
            if len(pares_encontrados) == 6:
                messagebox.showinfo("Parabéns!", "Você completou o jogo da memória!")
                self.janela_memoria.destroy()
                self.progresso_label.config(text="Progresso: Desafio Concluído")
        
        for i in range(3):
            linha_botoes = []
            for j in range(4):
                botao = tk.Button(self.janela_memoria, text="", width=10, height=5,
                                  command=lambda i=i, j=j: revelar_carta(i, j, botoes[i][j]), bg="#FFEB3B")
                botao.grid(row=i, column=j, padx=5, pady=5)
                linha_botoes.append(botao)
            botoes.append(linha_botoes)

# Iniciar a interface principal
root = tk.Tk()
jogo = JogoDesafios(root)
root.mainloop()
