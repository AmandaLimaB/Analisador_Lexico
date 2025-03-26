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

# Percorrer todos os arquivos da pasta
for raiz, diretorios, arquivos in os.walk(pasta_selecionada):
    for arquivo in arquivos:
        caminho_completo = os.path.join(raiz, arquivo)
        lista_nomes_arquivos.append(arquivo)
        lista_caminho_arquivos.append(caminho_completo)
    raiz_arq = raiz

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
      # Núemro da linha no arquivo
      numero_linha = 0
      
      # Percorre cada linha do arquivo
      for linha in arquivo:
        numero_linha += 1
        
        # Filtra linhas em branco ou espaços vazios
        if not linha.isspace():
          
          # Conferir se os tokens estão corretos de acordo com a linha
          print("Conteúdo da linha do arquivo: ", linha) 
          
          palavra_token = ''
          caracter = 0
          
          # O valor do caracter não pode passar o valor da linha para não ocorrer o erro out of range
          while caracter < len(linha):

            # Dígito
            if linha[caracter].isdigit():
              palavra_token += linha[caracter]

              # Verifica se tem mais de um ponto no número (1 primeiro ponto, -1 segundo ponto)
              fracionario = 1

              # Verifica os caracteres seguintes com a condição de não ver um caracter inválido
              while caracter + 1 < len(linha) and (linha[caracter + 1].isdigit() or linha[caracter + 1] == '.') and linha[caracter + 1] != ' ':
                caracter += 1
                palavra_token += linha[caracter]
                
                # Mudar o indicador de ponto
                if linha[caracter] == '.':
                  fracionario *= -1
                
                # Para caso tenha um segundo ponto
                if linha[caracter + 1] == '.' and fracionario == -1:
                  break
              
              print('(Tipo: Número, Valor: "%s")' % (palavra_token))
              #####  print("%.2d NRO %s" % (numero_linha, palavra_token))
              palavra_token = ''

            # Letra
            elif linha[caracter].isalpha():
              palavra_token += linha[caracter]
              while caracter + 1 < len(linha) and (linha[caracter + 1].isalpha() or linha[caracter + 1].isdigit() or linha[caracter + 1] == '_') and linha[caracter + 1] != ' ':
                caracter += 1
                palavra_token += linha[caracter]
              if palavra_token in palavras_reservadas:
                print('(Tipo: Palavra reservada, Valor: "%s")' % (palavra_token))
                #### print("%.2d PRE %s" % (numero_linha, palavra_token))
              
              ########################################## CONFERIR #############################################
              else:
                for caracter_id in palavra_token:
                  if caracter_id in acentos:
                    print('(Tipo: Identificador MAL FORMADO, Valor: "%s")' % (palavra_token))
                    break
                  print('(Tipo: Identificador, Valor: "%s")' % (palavra_token))
                ### print("%.2d IDE %s" % (numero_linha, palavra_token))
              palavra_token = ''   

            # Símbolo
            elif linha[caracter] in string.punctuation:
              palavra_token += linha[caracter]

              op_aritmeticos = False
              op_relacionais = False
              op_logicos = False
              palavra = False
              
              while caracter + 1 < len(linha) and (linha[caracter + 1] in string.punctuation) and linha[caracter + 1] != ' ' and palavra_token != '"':
                
                if caracter + 1 < len(linha):
                  if palavra_token in operadores_aritmeticos and palavra_token + linha[caracter + 1] not in operadores_aritmeticos:
                    op_aritmeticos = True
                    break

                  elif palavra_token in operadores_relacionais and palavra_token + linha[caracter + 1] not in operadores_relacionais:
                    op_relacionais = True
                    break

                  elif palavra_token in operadores_logicos and palavra_token + linha[caracter + 1] not in operadores_logicos:
                    op_logicos = True
                    break
                  
                caracter += 1
                palavra_token += linha[caracter]

              if palavra_token == '"':
                palavra = True
                caracter += 1
                palavra_token += linha[caracter]
                while palavra_token[len(palavra_token) - 1] != '"' and caracter < len(linha):
                  palavra_token += linha[caracter]
                  caracter += 1

              if op_aritmeticos or palavra_token in operadores_aritmeticos:
                print('(Tipo: Operador Aritmético, Valor: "%s")' % (palavra_token))

              elif op_relacionais or palavra_token in operadores_relacionais:
                print('(Tipo: Operador relacional, Valor: "%s")' % (palavra_token))

              elif op_logicos or palavra_token in operadores_logicos:
                print('(Tipo: Operador Lógico, Valor: "%s")' % (palavra_token))

              elif palavra:
                print('(Tipo: Cadeia de caracter, Valor: %s)' % (palavra_token))
              
              else:
                print('(Tipo: Simbolo, Valor: "%s")' % (palavra_token))
          
              palavra_token = ''
              
            caracter += 1





'''
PENDENCIAS: 

* Tirar os acentos
* Tirar os comentários
'''


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