# Introdução

## Serviço e protocolos de transporte

- Disponibiliza uma **ligação lógica entre aplicações** (processos) que estão a ser executadas em Sistemas terminais

- Os protocolos de transporte sao executados nos sistemas terminais
  - O emissor: parte a mensagem gerada pela aplicação em **segmentos** que passa á camada de rede.
  - O recetor: junta os diferentes **segmentos** que constituem uma mensagem que passa á respetiva aplicação.
  - Internet: TCP e UDP.
  
## Transporte vs Rede

### Camada de Rede

- fornece uma ligação lógica entre dois Sistemas terminais

> Nao existe uma ligação entre dois sistemas terminais, existe um caminho que é calculado.

### Camada de Transporte

- Fornece uma comunicação lógica entre processos ou aplicações
- Melhora os serviços disponibilizados pela camada de rede
- Troca de dados fiável e ordenada (TCP)
  - Controlo de **fluxo**, Estabelecimento da ligação
  - Controlo de **erros**
  - Controlo de **congestão**
- Troca de dados nao fiável e desordenada (UDP)
- Serviços nao disponíveis: garantia de atraso máximo e largura de banda minima

## Transporte

- E msm necessário ter uma camada de transporte?

> Em principio sim, uma das funções principais e o endereçamento das ligações, o nível de transporte adiciona um nível de diferenciação dentro de uma maquina, sem ele nao consigo identificar os processos dentro de uma maquina.
Ha no entanto aplicações especiais que so precisam do endereço da porta e n necessitam de protocolo da camada de transporte.
Sem ele nao csg ter aplicações a correr nas maquinas pois estas necessitam de portas

- Tudo o que a camada de transporte faz nao pode ser feito pelas aplicações?

> Alem da atribuição de uma porta, se a aplicação csg fazer essa atribuição n seria necessário o transporte. Mas a parte da multiplexagem e desmultiplexagem nao pode ser feita pela aplicação pois esta n sabe que o pacote é para ela.

- Nao é possível desenvolver aplicações diretamente sobre o IP?

> Nao pelo motivo respondido na anterior

- Nao é possível desenvolver aplicações diretamente sobre a camada lógica (MAC)?

> Sim em hardware especifico mas no mundo normal nao.

## Multiplexagem e Desmultiplexagem

### Desmultiplexagem

È efetuada pelo sistema terminal destino ao receber um datagrama IP

- Cada datagrama contem um segmento TCP ou UDP
- Cada segmento possui a identificação da porta de origem

...............................

----

NAO ORIENTANDO A CONEXãO

- As aplicações criam um socket... e limitam-se a enviar datagramas para IP Destino, Porta destino

```java
DatagramSocket s = new DatagramSocket();
DatagramSocket p = new DatagramSocket(aEnviar,aEnviar.length, IP,9999);
s.send(p);
```

ORIENTANDO A CONEXãO (TCP)

Um socket é definido pelos dois pontos q se unem na conexão, e so flui dados entre os dois processos

- As aplicações criam um socket e uma conexão com servidor destino para enviar dados.

## Pilha protocolar TCP/IP

### (TCP)

### (UDP)

**Funções do UDP:**

- menos fiável que o tcp
- orientado ao datagrama
- interface da aplicação com o ip para multiplexar e desmultiplexar tráfego
- usa o conceito de porta / numero de porta
  - direciona datagramas IP para o nível superior
  - portas reservadas: 0 a 1023, dinâmicas: 1024 a 65535

> Usado qd ha exigências de delay baixo é usado o UDP (por exemplo jogos online)

Controlo de Erros (UDP)

Checksum:

- Checksum = 0 calculo n foi efetuado
- Checksum != significa que recetor deteta erro na soma e:
  - o datagram é descartado
  - nao e gerada a mensagem de erro para enviar ao transmissor
  - a aplicação de receção é notificada

**O que leva a escolher o UDP:**

- Maior controlo sobre o envio dos dados por parte da aplicação (serve de fuga ao controlo de congestão do TCP)
  - APLICAÇÃO CONTROLA QUANDO DEVE ENVIAR OU REENVIAR OS dados sem deixar essa decisão ao serviço de transporte
  - aplicação decide quantos bytes envia realmente de cada vez
- Nao ha estabelecimento e terminação da conexão, diminuindo p atraso da comunicação
- nao e necessário manter informação de estado da conexão
- Menor overhead de dados(cabeçalho UDP sao apenas 8 bytes)

**Funções do TCP:**

- Permite transporte fiável de dados aplicacionais fim-a-fim
- Efetua associações lógicas fim-a-fim (conexões)
- Cada conexão e identificada por um socket TCP e cada conexão é um circuito virtual entre portas de aplicações (também designadas por portas de serviço)
- Multiplexa os dados de varias aplicações através de numero de porta
- Efetua control de erros, fluxo e de congestão (ISTO O UDP N FAZ)
- As implementações do TCP sao diferentes entre Sistemas Operativos