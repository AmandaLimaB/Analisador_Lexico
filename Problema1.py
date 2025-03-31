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
acentos = ['À', 'Á', 'Â', 'Ã', 'Ä', 'Å', 'Æ', 'Ç', 'È', 'É', 'Ê', 'Ë', 'Ì', 'Í', 'Î', 'Ï', 
 'Ð', 'Ñ', 'Ò', 'Ó', 'Ô', 'Õ', 'Ö', 'Ø', 'Ù', 'Ú', 'Û', 'Ü', 'Ý', 'Þ', 'ß', 'à', 
 'á', 'â', 'ã', 'ä', 'å', 'æ', 'ç', 'è', 'é', 'ê', 'ë', 'ì', 'í', 'î', 'ï', 'ð', 
 'ñ', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ù', 'ú', 'û', 'ü', 'ý', 'þ', 'ÿ']

# Percorrer os arquivos para abrir e ler o conteúdo
for arquivo in lista_caminho_arquivos:
  with open(arquivo, "r", encoding="utf-8") as arquivo:
      # Núemro da linha no arquivo para mostrar no arquivo final
      numero_linha = 0

      comentario = False
      
      # Percorre cada linha do arquivo para analisar todos os tokens
      for linha in arquivo:
        # Contagem das linhas
        numero_linha += 1
        
        # Lugar onde cada token vai ser armazenado, e depois vai ser resetado para o token seguinte
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
              caracter += 1
            caracter += 1
            
          # O valor do caracter não pode passar o valor da linha para não ocorrer o erro out of range
          while caracter < len(linha) and not comentario:

            if caracter + 1 < len(linha) and linha[caracter] + linha[caracter + 1] == "/*":
              print("Comentário")
              comentario = True
              caracter += 1
              break

            # Dígito (Reconhecer os números)
            elif linha[caracter].isdigit():
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
                if linha[caracter + 1] == '.' and fracionario:
                  break
              
              # Verificar se não é um número mal formado
              if palavra_token[len(palavra_token) - 1] == '.':
                print('(Tipo: Número MAL FORMADO, Valor: "%s")' % (palavra_token)) ###################################################
              else:
                print('(Tipo: Número, Valor: "%s")' % (palavra_token)) ###################################################
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
                print('(Tipo: Palavra reservada, Valor: "%s")' % (palavra_token)) ###################################################         
              else:
                print('(Tipo: Identificador, Valor: "%s")' % (palavra_token)) ###################################################
              
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
              
              # Identifica operadores com dois elementos ou uma cadeira de caracteres
              while palavra_token == '"' or (caracter + 1 < len(linha) and linha[caracter + 1] in string.punctuation and linha[caracter + 1] != ' '):
                
                # Comentário de linha
                if palavra_token + linha[caracter + 1] == "//":
                  caracter = len(linha)
                  palavra_token = ''
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
                  print('(Tipo: Simbolo, Valor: "%s")' % (palavra_token)) #########################################################################
                  palavra_token = ''
                  caracter += 1
                  palavra_token += linha[caracter]

              if op_aritmeticos or palavra_token in operadores_aritmeticos:
                print('(Tipo: Operador Aritmético, Valor: "%s")' % (palavra_token)) #########################################################################

              elif op_relacionais or palavra_token in operadores_relacionais:
                print('(Tipo: Operador relacional, Valor: "%s")' % (palavra_token)) #########################################################################

              elif op_logicos or palavra_token in operadores_logicos:
                print('(Tipo: Operador Lógico, Valor: "%s")' % (palavra_token)) #########################################################################

              elif id_delimitadores or palavra_token in delimitadores:
                print('(Tipo: Delimitador, Valor: "%s")' % (palavra_token)) #########################################################################

              elif palavra:
                mal_formado = False
                if palavra_token[len(palavra_token) - 1] != '"':
                  print('(Tipo: Cadeira MAL FORMADA FALTA ASPAS, Valor: %s)' % (palavra_token)) #########################################################################
                else:
                  for caracter_id in palavra_token:
                    if caracter_id in acentos:
                      mal_formado = True
                      break
                  if mal_formado:
                    print('(Tipo: Cadeira MAL FORMADA COM ACENTO, Valor: %s)' % (palavra_token)) #########################################################################
                  else:
                    print('(Tipo: Cadeia de caracter SEM ASPAS, Valor: %s)' % (palavra_token)) #########################################################################
          
              palavra_token = ''
              
            caracter += 1
        
        print("NUMERO LINHAAAA: ", numero_linha)
      
      if comentario:
        print("Comentário não fechado") #################################################################################






'''
ARQUIVOS DE SAÍDA, JÁ CORRETO


# Criar os arquivos de saída (vazios por enquanto)
for arquivos in lista_nomes_arquivos:
  nome, extensao = os.path.splitext(arquivos)
  print(nome)
  nome_saida = raiz_arq + '/' + nome + '-saida' + extensao
  print(nome_saida)
  with open(nome_saida, "w", encoding="utf-8") as arquivo:
    arquivo.write("Este é um arquivo criado em Python!\n")
    arquivo.write(nome_saida)
'''