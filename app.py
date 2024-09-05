from datetime import datetime
import re
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

class Transacao:
    def __init__(self, tipo, valor, saldo_atual):
        self.tipo = tipo
        self.valor = valor
        self.data_hora = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        self.saldo_atual = saldo_atual

class Deposito(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: 'Conta'):
        conta.saldo += self.valor

class Saque(Transacao):
    def __init__(self, valor: float):
        self.valor = valor

    def registrar(self, conta: 'Conta'):
        conta.saldo -= self.valor

class Conta:

    def __init__(self, numero: int, cliente: 'Cliente', limite: float, agencia:int):
        self.numero = numero
        self.agencia = agencia
        self.cliente = cliente
        self.saldo = 1000.0
        self.limite = limite
        self.extrato = []

    def consulta_saldo(self) -> float:
        return float(self.saldo)

    def sacar(self, valor):
        if valor > self.limite:
            return False, "O saque excede o limite"
        if valor > self.saldo:
            return False, "Saldo insuficiente"
        self.saldo -= valor
        self.extrato.append(Transacao('saque', valor, self.saldo))
        return True, "Saque realizado com sucesso"

    def depositar(self, valor):
        if valor <= 0:
            return False, "Valor de depósito inválido"
        self.saldo += valor
        self.extrato.append(Transacao('deposito', valor, self.saldo))
        return True, "Depósito realizado com sucesso"
    
    @classmethod
    def nova_conta(cls, cliente: 'Cliente', numero: int) -> 'Conta':
        conta = cls(numero, cliente)
        cliente.adicionar_conta(conta)
        cls.agencia += 1
        return conta
    
class Historico:
    def __init__(self):
        self.transacoes = []

    def adicionar_transacao(self, transacao: 'Transacao'):
        self.transacoes.append(transacao)

class Cliente:
    def __init__(self, endereco, nome, cpf, data_nasc):
        self.endereco = endereco
        self.nome = nome
        self.cpf = cpf
        self.data_nasc = data_nasc
        self.contas = []

    def realizar_transacao(self, conta: Conta, transacao: 'Transacao'):
        transacao.registrar(conta)

    def adicionar_conta(self, conta: 'Conta'):
        self.contas.append(conta)


def formatar_data(event, campo):
    texto = campo.get().replace("/", "")
    novo_texto = ""

    # Adicionando a barra automaticamente nos lugares corretos
    for i in range(len(texto)):
        if i == 2 or i == 4:
            novo_texto += "/" + texto[i]
        else:
            novo_texto += texto[i]

    campo.delete(0, 'end')
    campo.insert(0, novo_texto[:10])



class BancoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Banco App")
        self.root.configure(background="#1d1e1e")        
        
        self.root.geometry('1060x600')
        self.root.resizable(False, False)

        self.lista_usuarios = []


        # Frame de cadastro de cliente
        self.frame = Frame(self.root, bd=4, highlightbackground="#444949", highlightthickness=2, background='#2f3031')
        self.frame.place(relx=0.02, rely=0.2, relwidth=0.96, relheight=0.75)

        self.frame2 = Frame(self.root, bd=4, background='#1d1e1e')
        self.frame2.place(relx=0.02, rely=0.01, relwidth=0.96, relheight=0.18)

        self.inicio()
        

    def inicio(self):
        self.limpa_tela()
        Label(self.frame2, text="Sistema de Gerenciamento de Contas", bg = '#1d1e1e', fg = 'white',font=('Arial', 16, 'bold')).pack()

        Button(self.frame, text="Cadastrar Cliente", bg='#2ac70e', font=('Arial', 10,'bold'), command=self.tela_cliente).place(relx=0.45, rely=0.10)

        x = 0.100
        y = 0.10

        for index, cliente in enumerate(self.lista_usuarios):
            usuarioCadastrados = Button(self.frame, text=f"{cliente.nome}", font=('Arial', 14,'bold'), width= 15,
                                        bg='#2f3031',fg="white", command=lambda idx=index: self.mostraConta(idx))

            y += 0.10 
            if y > 0.75:
                y = 0.20
                x += 0.200
            usuarioCadastrados.place(relx= x, rely= y)

    def limpa_tela(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        for widget in self.frame2.winfo_children():
            widget.destroy()
        

    def tela_cliente(self):
        self.limpa_tela()
        
        Label(self.frame, text="Cadastro de Usuário", bg="#2f3031", fg = "white", font=('Arial', 25)).pack()
        Label(self.frame, text="CPF", bg="#2f3031", fg = "white", font=('Arial', 14)).place(relx=0.150, rely=0.2)
        self.Cpf = Entry(self.frame)
        self.Cpf.place(relx=0.150, rely=0.30)

        Label(self.frame, text="Primeiro Nome",bg="#2f3031", fg = "white", font=('Arial', 14)).place(relx=0.150, rely=0.45)
        self.Nome = Entry(self.frame)
        self.Nome.place(relx=0.150, rely=0.55)

        Label(self.frame, text="Data de Nascimento (dd/mm/aaaa)", fg="white", bg="#2f3031",font=('Arial', 14)).place(relx=0.425, rely=0.2)
        self.DataNasc = Entry(self.frame)
        self.DataNasc.place(relx=0.425, rely=0.30)
        self.DataNasc.bind("<KeyRelease>", lambda event: formatar_data(event, self.DataNasc))

        Label(self.frame, text="Endereço",bg="#2f3031", fg = "white", font=('Arial', 14)).place(relx=0.425, rely=0.45)
        self.Endereco = Entry(self.frame)
        self.Endereco.place(relx=0.425, rely=0.55)

        

        Button(self.frame, text="Salvar", bg='#2ac70e',font=('Arial',10,'bold'),command=self.salvar_cliente).place(relx=0.8, rely=0.85)
        # Vinculando o Enter para salvar o usuário
        self.root.bind('<Return>', lambda event: self.salvar_cliente())
        Button(self.frame, text="Voltar", bg='red',fg="white",font=('Arial',10,'bold'),command=self.inicio).place(relx=0.9, rely=0.85)

    def salvar_cliente(self):
        endereco = self.Endereco.get()
        nome = self.Nome.get()
        cpf = self.Cpf.get()
        data = self.DataNasc.get()

        if not cpf.isdigit():
            return messagebox.showerror("Aviso", "O campo CPF só aceita números!")
        
        if len(endereco) > 20:
            return messagebox.showerror("Aviso", "O Endereço só pode ter no maximo 20 letras!")
        if len(nome) > 15:
            return messagebox.showerror("Aviso", "O Nome só pode ter no maximo 15 letras!")
        
        # Validação de nome sem números ou caracteres especiais
        if not re.match("^[A-Za-z ]+$", nome):  # Permite letras e espaços
            return messagebox.showerror("Aviso", "O campo Nome só aceita letras!")
        
        try:
            data_nascimento = datetime.strptime(data, "%d/%m/%Y")
            if data_nascimento >= datetime.now():
                return messagebox.showerror("Erro", "A data de nascimento deve ser anterior ao dia de hoje!")
        except ValueError:
            return messagebox.showerror("Erro", "Data de nascimento inválida! Use o formato dd/mm/aaaa.")

        

        for cliente in self.lista_usuarios:
            if cliente.cpf == cpf:
                return messagebox.showerror("Erro", "CPF já cadastrado!")

        cliente = Cliente(endereco, nome, cpf, data)
        self.lista_usuarios.append(cliente)               
        
        return self.inicio()
    
    def mostraConta(self, usuario_index):
        self.limpa_tela()

        usuario = self.lista_usuarios[usuario_index]
        Label(self.frame2, text=f"Bem vindo, {usuario.nome}", bg='#1d1e1e', fg='white', font=('Arial', 12)).place(relx=0.0, rely=0.10)
        Label(self.frame2, text=f"CPF: {usuario.cpf}", bg='#1d1e1e', fg='white', font=('Arial', 12)).place(relx=0.25, rely=0.10)
        Label(self.frame2, text=f"Endereço: {usuario.endereco}", bg='#1d1e1e', fg='white', font=('Arial', 12)).place(relx=0.45, rely=0.10)
        Label(self.frame2, text=f"Data Nasc: {usuario.data_nasc}", bg='#1d1e1e', fg='white', font=('Arial', 12)).place(relx=0.65, rely=0.10)

        x = 0.100
        y = 0.20

        for count, conta in enumerate(usuario.contas):
            conta_button = Button(self.frame, text=f"Agência: {conta.agencia} - C/C: {conta.numero}", font=('Arial', 14, 'bold'),
                                  width=25, bg='#2f3031', fg="white", command=lambda c=count: self.inicializador(usuario_index, c))
            y += 0.10
            if y > 0.75:
                y = 0.20
                x += 0.400
            conta_button.place(relx=x, rely=y)

        Button(self.frame, text="Adicionar Conta", bg='#2ac70e', font=('Arial', 10, 'bold'), command=lambda: self.adicionarConta(usuario_index)).pack()
        Button(self.frame, text="Voltar", bg="red", fg="white", font=('Arial', 10, 'bold'), command=self.inicio).place(relx=0.90, rely=0.85)

    def adicionarConta(self, usuario_index):
        self.limpa_tela()
        
        usuario = self.lista_usuarios[usuario_index]
        
        Label(self.frame, text=f"Adicionar Conta para {usuario.nome}", bg="#2f3031", fg = "white", font=('Arial', 25)).pack()

        Label(self.frame, text="Agência:", bg="#2f3031", fg = "white",font=('Arial', 14)).place(relx=0.150, rely=0.2)
        agencia_entry = Entry(self.frame)
        agencia_entry.place(relx=0.150, rely=0.3)

        Label(self.frame, text="C/C:", bg="#2f3031", fg = "white",font=('Arial', 14)).place(relx=0.425, rely=0.2)
        conta_corrente_entry = Entry(self.frame)
        conta_corrente_entry.place(relx = 0.425, rely=0.3)

        Label(self.frame, text="Limite", bg="#2f3031", fg = "white",font=('Arial', 14)).place(relx=0.150, rely=0.5)
        limite_entry = Entry(self.frame)
        limite_entry.place(relx = 0.150, rely=0.6)

        btnSalvarConta = Button(self.frame, text="Salvar", bg="#2ac70e", font=('Arial',10,'bold'),
                                command=lambda: self.salvarConta(usuario_index, agencia_entry.get(), conta_corrente_entry.get(), limite_entry.get()))
        btnSalvarConta.place(relx=0.80, rely=0.85)

        # Vinculando o Enter para salvar a conta
        self.root.bind('<Return>', lambda event: self.salvarConta(usuario_index, agencia_entry.get(), conta_corrente_entry.get(), limite_entry.get()))

        btnVoltar = Button(self.frame, text="Voltar", bg="red", fg="white",font=('Arial',10,'bold'), command=lambda: self.mostraConta(usuario_index))
        btnVoltar.place(relx=0.90, rely=0.85)

   

    def salvarConta(self, usuario_index, agencia, conta_corrente, limite):
        usuario = self.lista_usuarios[usuario_index]

        if len(agencia) > 5 or len(conta_corrente) > 5:
            return messagebox.showinfo("Aviso!", "Agência e Conta corrente só podem ter no máximo 5 caracteres!")
        if len(agencia) == 0 or len(conta_corrente) == 0:
            return messagebox.showinfo("Aviso!", "Todos os campos são obrigatórios!")
        try:
            novo_limite = float(limite)
        except ValueError:
            return messagebox.showinfo("Erro!", "O campo limite só aceita números!")
        if novo_limite <= 0:
            return messagebox.showinfo("Erro", "Digite um limite acima de 0")
        if not conta_corrente.isdigit() or not agencia.isdigit():
            return messagebox.showinfo("Erro!", "O campo Conta Corrente só pode conter números!")


        # Cria uma nova conta e adiciona ao cliente
        nova_conta = Conta(numero=int(conta_corrente), cliente=usuario, limite=novo_limite, agencia=agencia)
        usuario.adicionar_conta(nova_conta)
        self.mostraConta(usuario_index)



    def inicializador(self, usuario_index, conta_index):
        self.limpa_tela()

        usuario = self.lista_usuarios[usuario_index]
        conta = usuario.contas[conta_index]

        labelNome = Label(self.frame2, text=f"Bem vindo, {usuario.nome}", bg="#1d1e1e", fg="white", font=('Arial', 14))
        labelNome.place(relx=0.00, rely=0.03, relwidth=0.2)

        labelSaldo = Label(self.frame2, text=f"Limite de Saque: R$ {conta.limite:.2f}", bg="#1d1e1e", fg="white", font=('Arial', 14))
        labelSaldo.place(relx=0.4, rely=0.03)

        self.labelSaldo = Label(self.frame2, text=f"Saldo: R$ {conta.saldo:.2f}", bg="#1d1e1e", fg="white", font=('Arial', 14))
        self.labelSaldo.place(relx=0.8, rely=0.03, relwidth=0.2)

        self.saque()
        self.deposito()
        self.botaoConfirmar(usuario_index, conta_index)
        self.criarExtrato(usuario_index, conta_index)
        self.botaoSair(usuario_index)

        self.root.bind('<Return>', lambda event: self.pegaInfo(usuario_index, conta_index))

    def saque(self):
        labelSaque = Label(self.frame2, text="Saque: ", bg="#1d1e1e", fg="white", font=('Arial', 14))
        labelSaque.place(relx=0.00, rely=0.60, relwidth=0.2)

        self.entrySaque = Entry(self.frame2, font=('Arial', 14))
        self.entrySaque.place(relx=0.13, rely=0.60, relwidth=0.2)

    def deposito(self):
        labelDeposito = Label(self.frame2, text="Depósito: ", bg="#1d1e1e", fg="white", font=('Arial', 14))
        labelDeposito.place(relx=0.49, rely=0.60, relwidth=0.2)

        self.entryDeposito = Entry(self.frame2, font=('Arial', 14))
        self.entryDeposito.place(relx=0.63, rely=0.60, relwidth=0.2)

    def botaoConfirmar(self, usuario_index, conta_index):
        botaoConfirma = Button(self.frame2, text="Confirmar", font=('Arial', 14), command=lambda: self.pegaInfo(usuario_index, conta_index), bg="#101527", fg="#11EC41")
        botaoConfirma.place(relx=0.85, rely=0.60)

    def botaoSair(self, usuario_index):
        botaoSair = Button(self.frame2, text="Sair", font=('Arial', 14), command=lambda: self.mostraConta(usuario_index), bg="#101527", fg="#11EC41")
        botaoSair.place(relx=0.95, rely=0.60)

    def criarExtrato(self, usuario_index, conta_index):
        self.scrollbar = Scrollbar(self.frame)
        self.scrollbar.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(self.frame, columns=('Saque', 'Depósito', 'Saldo', 'Data/Hora'), show='headings', yscrollcommand=self.scrollbar.set)
        self.tree.pack(expand=True, fill=BOTH)

        self.tree.heading('Saque', text='Saque')
        self.tree.heading('Depósito', text='Depósito')
        self.tree.heading('Saldo', text='Saldo')
        self.tree.heading('Data/Hora', text='Data/Hora')

        self.scrollbar.config(command=self.tree.yview)

        conta = self.lista_usuarios[usuario_index].contas[conta_index]
        for transacao in conta.extrato:
            saque = transacao.valor if transacao.tipo == 'saque' else ''
            deposito = transacao.valor if transacao.tipo == 'deposito' else ''
            self.tree.insert('', 'end', values=(f"R$ {saque:.2f}" if saque else '', f"R$ {deposito:.2f}" if deposito else '', f"R$ {transacao.saldo_atual:.2f}", transacao.data_hora))

    def pegaInfo(self, usuario_index, conta_index):
        saqueEntry = self.entrySaque.get()
        depositoEntry = self.entryDeposito.get()

        conta = self.lista_usuarios[usuario_index].contas[conta_index]

        try:
            if saqueEntry:
                saque = float(saqueEntry)
                sucesso, mensagem = conta.sacar(saque)
                if not sucesso:
                    return messagebox.showinfo("Erro", mensagem)
                self.entrySaque.delete(0, END)

            if depositoEntry:
                deposito = float(depositoEntry)
                sucesso, mensagem = conta.depositar(deposito)
                if not sucesso:
                    return messagebox.showinfo("Erro", mensagem)
                self.entryDeposito.delete(0, END)

            
            self.labelSaldo.config(text=f"Saldo: R$ {conta.saldo:.2f}")

            # Atualiza o extrato
            self.tree.insert('', 'end', values=(f"R$ {saque:.2f}" if saqueEntry else '', f"R$ {deposito:.2f}" if depositoEntry else '', f"R$ {conta.saldo:.2f}", datetime.now().strftime('%d/%m/%Y %H:%M:%S')))

        except ValueError:
            messagebox.showinfo("Erro", "Digite valores numéricos!")
        



if __name__ == "__main__":
    root = Tk()
    app = BancoApp(root)
    root.mainloop()
