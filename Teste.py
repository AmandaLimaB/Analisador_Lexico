for i in range(192, 256):
  print(chr(i))
  


'''
for arquivo in lista_caminho_arquivos:
  with open(arquivo, "r", encoding="utf-8") as arquivo:
      for linha in arquivo:
        print("LINHAAAAAAAA -------------", linha)
        palavra_token = ''
        digito = False
        letra = False
        simbolo = False

        for caracter in linha:
          
          if caracter == " ":
            if palavra_token in palavras_reservadas:
              print('(Tipo: Palavra-chave, Valor: "%s")' % (palavra_token))
            elif digito:
              print('(Tipo: Número, Valor: "%s")' % (palavra_token))
            elif letra:
              print('(Tipo: Identificador, Valor: "%s")' % (palavra_token))
            elif simbolo:
              print('(Tipo: Simbolo, Valor: "%s")' % (palavra_token))
            
            palavra_token = ''
            digito = False
            letra = False
            simbolo = False        
          
          elif caracter.isdigit():
            palavra_token += caracter
            digito = True
            letra = False
            simbolo = False
          
          elif caracter.isalpha():
            palavra_token += caracter
            digito = False
            letra = True
            simbolo = False
          
          elif caracter in string.punctuation:
            palavra_token += caracter
            digito = False
            letra = False
            simbolo = True
        if palavra_token in palavras_reservadas:
          print('(Tipo: Palavra-chave, Valor: "%s")' % (palavra_token))
        elif digito:
          print('(Tipo: Número, Valor: "%s")' % (palavra_token))
        elif letra:
          print('(Tipo: Identificador, Valor: "%s")' % (palavra_token))
        elif simbolo:
          print('(Tipo: Simbolo, Valor: "%s")' % (palavra_token))
          
             


print("O jogador %s tem %.2f metros de altura." % (nome, altura))


(Tipo: Palavra-chave, Valor: "int")
(Tipo: Identificador, Valor: "x")
(Tipo: Operador, Valor: "=")
(Tipo: Número, Valor: "10")
(Tipo: Pontuação, Valor: ";")

       
        
        
        
      
        for palavra in palavras:
          if palavra.isdigit():
            print(palavra + " é número")
          elif palavra.isalpha():
            print(palavra + " é letra")
          else:
            print(palavra + " é símbolo")
        

'''