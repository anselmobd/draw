import pytest
from draw.core.engine import DrawEngine
from draw.renderers.mock_renderer import MockRenderer

@pytest.fixture
def engine():
    renderer = MockRenderer(width=100, height=100)
    return DrawEngine(renderer), renderer

def test_basic_movement(engine):
    de, mock = engine
    # Começa no centro (50, 50)
    de.execute("U10 R10 D10 L10")
    
    # Devem ser 4 linhas
    assert len(mock.lines) == 4
    
    # Primeira linha: (50, 50) -> (50, 40)
    assert mock.lines[0][0] == (50.0, 50.0)
    assert mock.lines[0][1] == (50.0, 40.0)
    
    # Posição final deve ser (50, 50)
    assert (de.x, de.y) == (50.0, 50.0)

def test_blind_movement(engine):
    de, mock = engine
    # Move sem desenhar 10 para cima e depois desenha 10 para direita
    de.execute("BU10 R10")
    
    # Apenas uma linha deve ter sido registrada (a do R10)
    assert len(mock.lines) == 1
    assert mock.lines[0][0] == (50.0, 40.0)
    assert mock.lines[0][1] == (60.0, 40.0)

def test_no_update_movement(engine):
    de, mock = engine
    # Desenha para cima mas não atualiza posição, depois desenha para direita
    de.execute("NU10 R10")
    
    # Ambas começam no mesmo ponto (50, 50)
    assert mock.lines[0][0] == (50.0, 50.0) # Up
    assert mock.lines[1][0] == (50.0, 50.0) # Right

def test_color_change(engine):
    de, mock = engine
    de.execute("C4 U5 C1 R5")
    
    assert mock.lines[0][2] == 4
    assert mock.lines[1][2] == 1

def test_scale(engine):
    de, mock = engine
    de.execute("S8 U1") # Escala 8, move 1 unidade -> (8 / 4) * 1 = 2 pixels
    assert mock.lines[0][1][1] == 48.0 # 50 - 2

def test_rotation_A(engine):
    de, mock = engine
    # TA -90 (ou A -1?) faz o U (0, -1) virar R (1, 0)
    # Atualmente rad = math.radians(-self.angle). 
    # Para A1 (90 graus), rad = -90.
    # U=(0,-1) -> rx = 0*cos(-90) - (-1)*sin(-90) = 0 - (-1)*(-1) = -1.
    # Por isso U vira L. O comportamento atual é rotação para a ESQUERDA (Anti-horário).
    de.execute("A1 U10")
    assert mock.lines[0][1] == (40.0, 50.0) # Vira Left

def test_rotation_TA(engine):
    de, mock = engine
    de.execute("TA 45 U10")
    # Gira 45 graus para a ESQUERDA (Anti-horário)
    import math
    dist = 10 * (de.scale / 4.0)
    # rad = -45
    # rx = 0*cos(-45) - (-1)*sin(-45) = -sin(45) = -0.707
    # ry = 0*sin(-45) + (-1)*cos(-45) = -cos(45) = -0.707
    expected_x = 50.0 - (dist * math.sin(math.radians(45)))
    expected_y = 50.0 - (dist * math.cos(math.radians(45)))
    
    assert mock.lines[0][1][0] == pytest.approx(expected_x)
    assert mock.lines[0][1][1] == pytest.approx(expected_y)
