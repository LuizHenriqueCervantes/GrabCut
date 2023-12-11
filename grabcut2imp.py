import numpy as np
import cv2

#Cor do retangulo de seleção
BLUE = [255, 0, 0]

#Background
RED = [0, 0, 255]       
DRAW_BG = {'color': RED, 'val': 0}

#Foreground
GREEN = [0, 255, 0]       
DRAW_FG = {'color': GREEN, 'val': 1}

#Flags
rect = (0, 0, 1, 1)
drawing = False            # flag para desenhar as curvas
rectangle = False          # flag para desenhar o retângulo
rect_over = False          # flag para verificar se o retangulo ficou completo
rect_or_mask = 100         # flag selecionar entre rect ou mask
value = DRAW_FG            # atribuir o valor do DRAW_FG
thickness = 3              # espessura do pincel

#Ações do mouse
def onmouse(event, x, y, flags, param):
    global img, img2, drawing, value, mask, rectangle, rect, rect_or_mask, ix, iy, rect_over

    #Desenhar o retangulo
    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle = True
        ix, iy = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
            img = img2.copy()
            cv2.rectangle(img, (ix, iy), (x, y), BLUE, 2)
            rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
            rect_or_mask = 0
    elif event == cv2.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True
        cv2.rectangle(img, (ix, iy), (x, y), BLUE, 2)
        rect = (min(ix, x), min(iy, y), abs(ix - x), abs(iy - y))
        rect_or_mask = 0
        print(" Aperte 'n' para ver o resultado \n")

    #Desenhar com o pincel
    if event == cv2.EVENT_LBUTTONDOWN:
        if rect_over == False:
            print("Desenhe o retângulo primeiro \n")
        else:
            drawing = True
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)
    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == True:
            drawing = False
            cv2.circle(img, (x, y), thickness, value['color'], -1)
            cv2.circle(mask, (x, y), thickness, value['val'], -1)

#Pega a imagem do diretório
img = cv2.imread(r'C:\Users\hrick\Documents\VsCode\Python\PDI\segmentacao\carro_esportivo.jpeg')

#Faz uma copia da imagem original
img2 = img.copy()                          

#Cria uma matriz bidimensional preenchida com zeros
mask = np.zeros(img.shape[:2], dtype=np.uint8) 

#Output image to be shown
output = np.zeros(img.shape, np.uint8)           

#Crias as janelas
cv2.namedWindow('output')
cv2.namedWindow('input')
cv2.setMouseCallback('input', onmouse)
cv2.moveWindow('input', img.shape[1] + 10, 90)

print(" Instruções: \n")
print(" Selecione a área com o botão direito do mouse \n")
while True:
    cv2.imshow('output', output)
    cv2.imshow('input', img)

    #Aguarda receber um valor do teclado
    k = 0xFF & cv2.waitKey(1)

    # Atalhos para controlar o menu
    if k == 27:          #Esc para sair
        break
    elif k == ord('0'):  #Desenhar o plano de fundo
        print(" Marque as regiões a serem retiradas com o botão esquerdo \n")
        value = DRAW_BG
    elif k == ord('1'):  #Desenhar a imagem a ser mantida
        print(" Marque as regiões a serem mantidas com o botão esquerdo \n")
        value = DRAW_FG

    elif k == ord('r'):  #Reseta para as configurações padrão
        print(" Resetando \n")
        rect = (0, 0, 1, 1)
        drawing = False
        rectangle = False
        rect_or_mask = 100
        rect_over = False
        value = DRAW_FG
        img = img2.copy()
        mask = np.zeros(img.shape[:2], dtype=np.uint8)
        output = np.zeros(img.shape, np.uint8)

    elif k == ord('n'):         #Roda o GrabCut
        print(" Marque os planos utilizando 0 ou 1 e a seguir pressione 'n' \n")
        if rect_or_mask == 0:   #GrabCut com retângulo
            bgdmodel = np.zeros((1, 65), np.float64)
            fgdmodel = np.zeros((1, 65), np.float64)
            cv2.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_RECT)
            rect_or_mask = 1
        elif rect_or_mask == 1: #GrabCut com a mascara
            bgdmodel = np.zeros((1, 65), np.float64)
            fgdmodel = np.zeros((1, 65), np.float64)
            cv2.grabCut(img2, mask, rect, bgdmodel, fgdmodel, 1, cv2.GC_INIT_WITH_MASK)

    mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
    output = cv2.bitwise_and(img2, img2, mask=mask2)

cv2.destroyAllWindows()
