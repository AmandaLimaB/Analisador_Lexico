import os 

import tkinter
import tkinter.filedialog

import string

# Criar uma instância da janela principal
root = tkinter.Tk()

# Ocultar a janela principal
root.withdraw()  

# Abre a caixa de diálogo para selecionar a pasta
pasta_selecionada = tkinter.filedialog.askdirectory(title="Selecione uma pasta")

print(f"Pasta selecionada: {pasta_selecionada}")

# Lista do caminho completo dos arquivos
lista_caminho_arquivos = []

# Lista do nome dos arquivos
lista_nomes_arquivos = []

# Caminho da pasta de teste
raiz_arq = ''

# Percorrer todos os arquivos da pasta e salva o nome em uma lista
for raiz, diretorios, arquivos in os.walk(pasta_selecionada):
    for arquivo in arquivos:
        caminho_completo = os.path.join(raiz, arquivo)
        lista_nomes_arquivos.append(arquivo)
        lista_caminho_arquivos.append(caminho_completo)
    raiz_arq = raiz

# Listas das palavras reservadas, símbolos reservados, letras acentuadas e delimitadores
palavras_reservadas = ["variables", "const", "class", "methods", "main", "return", "if", "else", "for", "read", "print", "void", "int", "float", "boolean", "string", "true", "false"]
operadores_aritmeticos = ["+", "-", "*", "/", "++", "--"]
operadores_relacionais = ["!=", "==", "<", "<=", ">", ">=", "="]
operadores_logicos = ["!", "&&", "||"]
delimitadores = [";", ",", ".", "(", ")", "[", "]", "{", "}", "->"]
caracteres_permitidos = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',    
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    ' ', '!', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', 
    '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', '\\', ']', '^',
    '_', '`', '{', '|', '}', '~']

# Percorrer os arquivos para abrir e ler o conteúdo
for nome_arquivo in lista_caminho_arquivos:
  with open(nome_arquivo, "r", encoding="utf-8") as arquivo:
      # Núemro da linha no arquivo para mostrar no arquivo final
      numero_linha = 0

      # Identificador se a leitura está em um comentário ou não
      comentario = False

      # Lista de tokens e erros
      lista_tokens = []
      lista_erros = []
      
      # Percorre cada linha do arquivo para analisar todos os tokens
      for linha in arquivo:
        # Contagem das linhas
        numero_linha += 1
        
        # Lugar onde cada token vai ser armazenado, e depois vai ser resetado para o token seguinte
        if not comentario:
          palavra_token = ''
        
        # Número que indica a posição do caracter da linha
        caracter = 0
        
        # Filtra linhas em branco ou espaços vazios que aparecem antes ou depois de cada linhas (não filtra os espaços vazios entre as linhas)
        if not linha.isspace():
          
          # Conferir se os tokens estão corretos de acordo com a linha, apenas para debug
          print("Conteúdo da linha do arquivo: ", linha)

          while comentario and caracter < len(linha):
            if caracter + 1 < len(linha) and linha[caracter] + linha[caracter + 1] == "*/":
              print("Fim comentário")
              comentario = False
              palavra_token += linha[caracter]
              caracter += 1
            if linha[caracter] != "\n":
              palavra_token += linha[caracter]
            if palavra_token[len(palavra_token) - 2] + palavra_token[len(palavra_token) - 1] == '*/':
                palavra_token = ''
            caracter += 1
            
          # O valor do caracter não pode passar o valor da linha para não ocorrer o erro out of range
          while caracter < len(linha) and not comentario:

            if caracter + 1 < len(linha) and linha[caracter] + linha[caracter + 1] == "/*":
              print("Comentário")
              palavra_token += linha[caracter]
              comentario = True
              caracter += 1
              while caracter + 1 < len(linha) and linha[caracter] + linha[caracter + 1] != '*/':
                if linha[caracter] != "\n":
                  palavra_token += linha[caracter]
                caracter += 1
              if palavra_token[len(palavra_token) - 2] + palavra_token[len(palavra_token) - 1] == '*/':
                palavra_token = ''
              break

            # Dígito (Reconhecer os números)
            elif linha[caracter].isdigit() or (caracter + 1 < len(linha) and (linha[caracter] == '-' and (op_aritmeticos or op_relacionais or id_delimitadores) and linha[caracter + 1].isdigit())):
              palavra_token += linha[caracter]

              # Verifica se tem mais de um ponto no número (True primeiro ponto, False segundo ponto). Se um ponto for achado no meio de um número o fracionario 
              # recebe o valor de False. Se algum outro ponto for achado o loop é quebrado.
              fracionario = False

              # Verifica os caracteres seguintes com as condições de ser número, ponto ou não ser espaço vazio
              while caracter + 1 < len(linha) and (linha[caracter + 1].isdigit() or linha[caracter + 1] == '.') and linha[caracter + 1] != ' ':
                caracter += 1
                palavra_token += linha[caracter]
                
                # Mudar o indicador de ponto
                if linha[caracter] == '.':
                  fracionario = True
                
                # Para caso tenha um segundo ponto
                if caracter + 1 < len(linha) and linha[caracter + 1] == '.' and fracionario:
                  break
              
              # Verificar se não é um número mal formado
              if palavra_token[len(palavra_token) - 1] == '.':
                lista_erros.append("{:02d} NMF {:s}".format(numero_linha, palavra_token))
              else:
                lista_tokens.append("{:02d} NRO {:s}".format(numero_linha, palavra_token))
              palavra_token = ''

            # Letra (Reconhecer os identificadores e palavras reservadas)
            elif linha[caracter].isalpha():
              
              palavra_token += linha[caracter]

              # Inicialmente identifica se é uma letra depois aceita outras letras, números ou underscore.
              while caracter + 1 < len(linha) and (linha[caracter + 1].isalpha() or linha[caracter + 1].isdigit() or linha[caracter + 1] == '_') and linha[caracter + 1] != ' ':
                caracter += 1
                palavra_token += linha[caracter]

              # Separar entre palavras reservadas ou identificadores
              if palavra_token in palavras_reservadas:
                lista_tokens.append("{:02d} PRE {:s}".format(numero_linha, palavra_token))         
              # Separar caracteres não permitidos nos identificadores
              else: 
                num_caracter = 0
                erro = False
                acerto = False
                palavra_token_aux = ''
                while num_caracter < len(palavra_token):
                  while num_caracter < len(palavra_token) and palavra_token[num_caracter] not in caracteres_permitidos:
                    palavra_token_aux += palavra_token[num_caracter]
                    num_caracter += 1
                    erro = True
                  if erro:
                    lista_erros.append("{:02d} TMF {:s}".format(numero_linha, palavra_token_aux))
                    erro = False
                    palavra_token_aux = ''
                  while num_caracter < len(palavra_token) and palavra_token[num_caracter] in caracteres_permitidos:
                    palavra_token_aux += palavra_token[num_caracter]
                    num_caracter += 1
                    acerto = True
                  if acerto:
                    lista_tokens.append("{:02d} IDE {:s}".format(numero_linha, palavra_token_aux))
                    acerto = False
                    palavra_token_aux = ''
              
              palavra_token = ''   

            # Símbolo (Reconhecer os símbolos e cadeias de caracteres) 
            elif linha[caracter] in string.punctuation:
              palavra_token += linha[caracter]

              # Identificadores do que está sendo separado no loop
              op_aritmeticos = False
              op_relacionais = False
              op_logicos = False
              id_delimitadores = False
              palavra = False
              comentario_linha = False
              
              # Identifica operadores com dois elementos ou uma cadeira de caracteres
              while palavra_token == '"' or (caracter + 1 < len(linha) and linha[caracter + 1] in string.punctuation and linha[caracter + 1] != ' '):
                
                # Comentário de linha
                if palavra_token + linha[caracter + 1] == "//":
                  caracter = len(linha)
                  palavra_token = ''
                  comentario_linha = True
                  break

                elif (palavra_token in operadores_aritmeticos or palavra_token + linha[caracter + 1] in operadores_aritmeticos) and (palavra_token + linha[caracter + 1] not in delimitadores):
                  op_aritmeticos = True
                  if palavra_token + linha[caracter + 1] in operadores_aritmeticos:
                    caracter += 1
                    palavra_token += linha[caracter]
                  break 
                
                elif palavra_token in operadores_relacionais or palavra_token + linha[caracter + 1] in operadores_relacionais:
                  op_relacionais = True
                  if palavra_token + linha[caracter + 1] in operadores_relacionais:
                    caracter += 1
                    palavra_token += linha[caracter]
                  break

                elif palavra_token in operadores_logicos or palavra_token + linha[caracter + 1] in operadores_logicos:
                  op_logicos = True
                  if palavra_token + linha[caracter + 1] in operadores_logicos:
                    caracter += 1
                    palavra_token += linha[caracter]
                  break

                elif palavra_token in delimitadores or palavra_token + linha[caracter + 1] in delimitadores:
                  id_delimitadores = True
                  if palavra_token + linha[caracter + 1] in delimitadores:
                    caracter += 1
                    palavra_token += linha[caracter]
                  break

                elif palavra_token == '"':
                  palavra = True                  
                  while caracter + 1 < len(linha) and (palavra_token[len(palavra_token) - 1] != '"' or len(palavra_token) == 1):
                    caracter += 1
                    palavra_token += linha[caracter]
                  break
                
                else:
                  lista_erros.append("{:02d} TMF {:s}".format(numero_linha, palavra_token))
                  palavra_token = ''
                  caracter += 1
                  palavra_token += linha[caracter]

              if op_aritmeticos or palavra_token in operadores_aritmeticos:
                op_aritmeticos = True
                lista_tokens.append("{:02d} ART {:s}".format(numero_linha, palavra_token))

              elif op_relacionais or palavra_token in operadores_relacionais:
                op_relacionais = True
                lista_tokens.append("{:02d} REL {:s}".format(numero_linha, palavra_token))

              elif op_logicos or palavra_token in operadores_logicos:
                lista_tokens.append("{:02d} LOG {:s}".format(numero_linha, palavra_token))
                
              elif id_delimitadores or palavra_token in delimitadores:
                id_delimitadores = True
                lista_tokens.append("{:02d} DEL {:s}".format(numero_linha, palavra_token))

              elif palavra:
                mal_formado = False
                if palavra_token[len(palavra_token) - 1] != '"':
                  lista_erros.append("{:02d} CadMF {:s}".format(numero_linha, palavra_token))
      
                else:
                  for num_caracter in range(1, len(palavra_token) - 1):
                    if palavra_token[num_caracter] not in caracteres_permitidos:
                      mal_formado = True
                      break
                  if mal_formado:
                    lista_erros.append("{:02d} CadMF {:s}".format(numero_linha, palavra_token))
                    
                  else:
                    lista_tokens.append("{:02d} CAC {:s}".format(numero_linha, palavra_token))
                                
              elif not comentario_linha:
                lista_erros.append("{:02d} TMF {:s}".format(numero_linha, palavra_token))
                          
              palavra_token = ''
              
            caracter += 1
      
      if comentario:
        lista_erros.append("{:02d} CoMF {:s}".format(numero_linha, palavra_token))

  
  
  nome, extensao = os.path.splitext(nome_arquivo)
  
  nome_saida = nome + '-saida' + extensao
  
  with open(nome_saida, "w", encoding="utf-8") as arquivo_saida:
    for linha in lista_tokens:
      linha = linha.rstrip("\n")
      arquivo_saida.write(linha + "\n")
    arquivo_saida.write("\n")
    for linha in lista_erros:
      linha = linha.rstrip("\n")
      arquivo_saida.write(linha + "\n")
