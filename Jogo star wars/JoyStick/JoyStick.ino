#include <Mouse.h>
#include <Keyboard.h>

// Pinos analógicos conectados ao joystick
const int pinX = A0; // Eixo X
const int pinY = A1; // Eixo Y
const int attackBtn = 2; // Botão de ataque
const int startBtn = 3; // Botão de start

// Tecla que vai ser pressionada ao clicar no botão
const int espaco = MOUSE_LEFT;
const int inicio = ' ';

// Variável que serve para armazenar o estado que o botão estava da última vez
int estadoAnteriorBotao_espaco = HIGH;
int estadoAnteriorBotao_iniciar = HIGH;

// Faixa de valores do joystick
const int minVal = 0;    // Valor mínimo lido
const int maxVal = 1023; // Valor máximo lido

// Faixa de movimento do mouse
const int mouseMin = -5; // Movimento mínimo do mouse
const int mouseMax = 5;  // Movimento máximo do mouse

void setup() {
  // Inicializa os botões
  pinMode(attackBtn, INPUT_PULLUP);
  pinMode(startBtn, INPUT_PULLUP);
  // Inicializa o mouse e o teclado
  Mouse.begin();
  Keyboard.begin();
}

void loop() {
  // Lê o estado dos botões
  int estadoAtualBotao_iniciar = digitalRead(startBtn);
  int estadoAtualBotao_espaco = digitalRead(attackBtn);

  // Verifica o estado dos botões
  if(estadoAnteriorBotao_espaco == HIGH && estadoAtualBotao_espaco == LOW){
    Mouse.click();
  }
  if(estadoAnteriorBotao_iniciar == HIGH && estadoAtualBotao_iniciar == LOW){
    Keyboard.press(inicio);
    delay(50);
    Keyboard.release(inicio);
  }

  // Armazena o estado atual dos botões para a próxima vez que forem pressionados
  estadoAnteriorBotao_espaco = estadoAtualBotao_espaco;
  estadoAnteriorBotao_iniciar = estadoAtualBotao_iniciar;
  
  // Lê os valores analógicos do joystick
  int xVal = analogRead(pinX) + 58;
  int yVal = analogRead(pinY) + 20;

  // Mapeia os valores do joystick para a faixa de movimento do mouse
  int mouseX = map(xVal, minVal, maxVal, mouseMin, mouseMax);
  int mouseY = map(yVal, minVal, maxVal, mouseMin, mouseMax);

  // Move o cursor do mouse
  Mouse.move(mouseX, mouseY);

  // Aguarda um curto período antes da próxima atualização
  delay(10);
}
