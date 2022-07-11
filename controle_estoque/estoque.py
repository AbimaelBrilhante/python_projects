import sqlite3
import pandas as pd
import csv
import os

print('[1] - Cadastrar Produto \n' 
      '[2] - Cadastrar Entrada de Produto \n' 
      '[3] - Cadastrar Saída de Produto \n' 
      '[4] - Consultar Movimentação de Estoque \n' 
      '[5] - Consultar Saldo de estoque \n' 
      '[6] - Editar Produto \n'
      '[7] - Excluir Produto \n' 
      '[8] - Excluir Entrada/Saida \n' 
      '[9] - Exportar Ficha de Estoque \n')



class Inventario:

    def __init__(self,arquivo):
        self.conexao = sqlite3.connect(arquivo)
        self.cursor = self.conexao.cursor()

    def criar_tabelas(self):
        tabela_materiais = 'CREATE TABLE IF NOT EXISTS dados_materiais(cod_produto text,descricao_produto text,' \
                           'unidade_de_medida text,cor text,tamanho text)'
        movimentacao_estoque = 'CREATE TABLE IF NOT EXISTS inventario_relatorio(id numeric, cod_produto text,' \
                               'descricao_produto text,quantidade numeric,data text,numero_documento text, movimentacao text)'
        self.cursor.execute(tabela_materiais)
        self.cursor.execute(movimentacao_estoque)

    def cadastrar_produto(self,cod_produto,*args):
        inserir = 'INSERT OR IGNORE INTO dados_materiais (cod_produto,descricao_produto,unidade_de_medida,cor,tamanho) values(?,?,?,?,?)'
        self.cursor.execute(inserir, (cod_produto, *args))
        self.conexao.commit()

    def verificar_cadastro(self,cod_produto):
        produtos_cadastrados = []
        consulta = 'SELECT cod_produto,descricao_produto,unidade_de_medida,cor,tamanho FROM dados_materiais WHERE cod_produto LIKE ?'
        self.cursor.execute(consulta, (f'%{cod_produto}%',))
        for linha in self.cursor.fetchall():
            produtos_cadastrados.append(linha[0])

        if cod_produto not in produtos_cadastrados:
            print("Produto Não cadastrado. Cadastrar produto")
            exit()
        else:
            pass

    def estoque(self,cod_produto,*args):
        estoque = 'INSERT OR IGNORE INTO inventario_relatorio (cod_produto,descricao_produto,' \
                    'quantidade,data,numero_documento,movimento) VALUES(?,?,?,?,?,?)'
        self.cursor.execute(estoque, (cod_produto, *args))
        self.conexao.commit()

    def consultar_movimentacao(self,cod_produto):
        consulta = 'SELECT id,cod_produto,descricao_produto,quantidade, movimento FROM inventario_relatorio WHERE cod_produto LIKE ?'
        self.cursor.execute(consulta, (f'%{cod_produto}%',))
        for linha in self.cursor.fetchall():
            print(linha)

    def consultar_saldo(self,cod_produto):
        saldo = 0
        consulta = 'SELECT cod_produto,descricao_produto,quantidade, movimento FROM inventario_relatorio WHERE cod_produto LIKE ?'
        self.cursor.execute(consulta, (f'%{cod_produto}%',))
        for linha in self.cursor.fetchall():
            saldo+=linha[2]
        print(f'Saldo em estoque do produto {linha[0]} - {linha[1]}: {saldo}')

    def editar_produto(self,cod_produto, descricao_produto,unidade_de_medida,cor,tamanho):
        consulta = 'UPDATE dados_materiais SET descricao_produto=?,unidade_de_medida=?,' \
                   'cor=?,tamanho=? WHERE cod_produto=?'
        self.cursor.execute(consulta, (descricao_produto,unidade_de_medida,cor,tamanho,cod_produto))
        self.conexao.commit()
        print(f'Produto {cod_produto} alterado com sucesso')

    def excluir_produto(self,cod_produto):
        consulta = 'DELETE FROM dados_materiais WHERE cod_produto=?'
        self.cursor.execute(consulta, (cod_produto,))
        self.conexao.commit()
        print(f'Produto {cod_produto} excluído com sucesso')

    def excluir_entrada_saida(self,id):
        consulta = 'DELETE FROM inventario_relatorio WHERE id=?'
        self.cursor.execute(consulta, (id,))
        self.conexao.commit()

    def exportar_ficha_de_estoque(self):
        self.cursor.execute('SELECT * FROM inventario_relatorio')
        with open("Relatorio de Inventario.csv", "w") as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=";")
            csv_writer.writerow([i[0] for i in self.cursor.description])
            csv_writer.writerows(self.cursor)
        dirpath = os.getcwd() + "/Relatorio de Inventario.csv"
        print("Dados exportados com sucesso para {}".format(dirpath))
        for linha in self.cursor.fetchall():
            print(linha)


    def fechar_conexao(self):
        self.cursor.close()
        self.conexao.close()

inventario_relatorio = Inventario('inventario_relatorio.db')
inventario_relatorio.criar_tabelas()
opcao = (input("Digite uma Opção: "))

if opcao == "9":
    inventario_relatorio.exportar_ficha_de_estoque()
    exit()

continuar = "s"
while continuar == "s":
    if opcao =="1":
        inventario_relatorio.cadastrar_produto(input("Código do Produto: "), input("Descrição do Produto: "),
                                               input("Unidade de Medida: "),input("Cor do Produto: "),
                                               input("Tamanho do Produto: "))
        continuar = input("cadastrar novo produto? s/n ")
    elif opcao =="2":
        digitacao = input("Código do Produto: ")
        inventario_relatorio.verificar_cadastro(digitacao)
        inventario_relatorio.estoque(digitacao, input("Descrição do Produto: "),
                                     float(input("Quantidade do Produto: ")), input("Data: "),
                                     input("Número do documento de Entrada: "),"ENTRADA")
        continuar = input("cadastrar nova entrada? s/n ")
    elif opcao == "3":
        digitacao = input("Código do Produto: ")
        inventario_relatorio.verificar_cadastro(digitacao)
        inventario_relatorio.estoque(digitacao, input("Descrição do Produto: "),
                                     float(input("Quantidade do Produto: "))*-1, input("Data: "),
                                     input("Número do documento de Saída: "),"SAIDA")
        continuar = input("cadastrar nova saída? s/n ")
    elif opcao == "4":
        inventario_relatorio.consultar_movimentacao(input("Código do Produto: "))
        continuar = input("Consultar outro produto ? s/n ")
    elif opcao == "5":
        inventario_relatorio.consultar_saldo(input("Código do Produto: "))
        continuar = input("Consultar outro produto ? s/n ")
    elif opcao == "6":
        inventario_relatorio.editar_produto(input("Código do Produto: "),input("Descrição do Produto: "),
                                                  input("Unidade de Medida: "),input("Cor: "),input("Tamanho: "))
        continuar = input("Editar outro produto ? s/n ")
    elif opcao == "7":
        inventario_relatorio.excluir_produto(input("Código do Produto: "))
        continuar = input("Excluir outro produto ? s/n ")
    elif opcao == "8":
        inventario_relatorio.excluir_entrada_saida(input("Id a ser excluído: "))
        continuar = input("Excluir outro(a) entrada/saída ? s/n ")


"""    else:
        print('Digite uma opção válida')"""






#2EXPORTAR FICHA DE CADASTRO EM EXCEL ORGANIZADO
#3FORMATAÇÃO DA DATA
#4LINKAR TABELA DO INVENTÁRIO COM BD


