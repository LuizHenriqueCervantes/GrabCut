import cv2
import numpy as np
import matplotlib.pyplot as plt

 #Caminho da imagem
image_path = r'C:\Users\hrick\Documents\VsCode\Python\PDI\segmentacao\walking.jpg'

def remove_background():

    #Carregar a imagem
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    #Inicializar a máscara como zeros
    mask = np.zeros(image.shape[:2], np.uint8)

    #Definir a região de interesse (ROI)
    rect = cv2.selectROI('Selecione a Região de Interesse', image)

    #Inicializar o modelo GrabCut
    bgd_model = np.zeros((1, 65), np.float64)
    fgd_model = np.zeros((1, 65), np.float64)

    #Aplicar o GrabCut
    cv2.grabCut(image, mask, rect, bgd_model, fgd_model, 5, cv2.GC_INIT_WITH_RECT)

    #Modificar a máscara para obter a segmentação final
    mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    #Aplicar a máscara à imagem original
    segmented_image = image * mask2[:, :, np.newaxis]

    #Plotar
    plt.figure(figsize=(12, 6))

    #Plotar imagem original
    plt.subplot(1, 2, 1)
    plt.imshow(image)
    plt.title('Imagem Original')

    #Plotar sem o background
    plt.subplot(1, 2, 2)
    plt.imshow(segmented_image)
    plt.title('Sem background')

    plt.show()

remove_background()
