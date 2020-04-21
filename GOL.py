import pygame
import numpy as np
import time

pygame.init()
pauseExect = False

# Ancho y alto de la pantalla
width, height = 1000, 1000

# Creación de pantalla
screen = pygame.display.set_mode((height, width))

# Color de fondo: casi negro, casi oscuro
bg = 25, 100, 25

# Pintar fondo con color elegido
screen.fill(bg)

nxC = 25
nyC = 25

dimCW = width / nxC
dimCH = width / nyC

# Estado de las celdas. Vivas = 1; Muertas = 0
gameState = np.zeros(nxC)

# Bucle de ejecución
while True:

	newGameState = np.copy(gameState)
	screen.fill(bg)
	time.sleep(0.1)
	
	# Eventos de teclado y ratón
	ev = pygame.event.get()

	for event in ev:

		if event.type == pygame.KEYDOWN:

			pauseExect = not pauseExect

		mouseClick = pygame.mouse.get_pressed()

		if sum(mouseClick) > 0:

			posX,posY = pygame.mouse.get_pos()
			celX,celY = int(np.floor(posX/ dimCW)), int(np.floor(posY/dimCH))
			newGameState[celX,celY] = not mouseClick[2]

	for y in range(0, nxC):
		
		for x in range(0, nyC):

			if not pauseExect:

				# Calculamos el número de vecinos cercanos
				n_neigh = gameState[(x - 1) % nxC, (y - 1) % nyC] + \
						  gameState[(x)     % nxC, (y - 1) % nyC] + \
						  gameState[(x + 1) % nxC, (y - 1) % nyC] + \
						  gameState[(x - 1) % nxC, (y)     % nyC] + \
						  gameState[(x + 1) % nxC, (y)     % nyC] + \
						  gameState[(x - 1) % nxC, (y+1)   % nyC] + \
						  gameState[(x)     % nxC, (y+1)   % nyC] + \
						  gameState[(x + 1) % nxC, (y+1)   % nyC]

				# Regla 1: Una célula muerta con exactamente 3 vecinas vivas, "revive"
				if gameState[x, y] == 0 and n_neigh == 3:

					newGameState[x, y] = 1

				# Regla 2: Una célula viva con menos de 2 o más de 3 vecinas vivas, "muere"
				elif gameState[x, y] == 1 and (n_neigh < 2 or n_neigh > 3):

					newGameState[x, y] = 0

				poly = [((x) * dimCW, y * dimCH), ((x + 1) * dimCW, y * dimCH),
						((x + 1) * dimCW, (y + 1) * dimCH),
						((x) * dimCW, (y + 1) * dimCH)]

				# Se dibuja la celda para cada par de x e y
				if newGameState[x,y] == 0:

					pygame.draw.polygon(screen, (128, 128, 128), poly, 1)

				else:

					pygame.draw.polygon(screen, (255, 255, 255), poly, 0)

	# Actualizamos el estado del juego
	gameState = np.copy(newGameState)
	pygame.display.flip()
