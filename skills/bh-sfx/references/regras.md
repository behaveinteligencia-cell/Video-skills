# Regras de efeitos sonoros

Tiradas de quatro vídeos de referência mandados pela agência (lista no fim). Os sons de cada um foram recortados e ficam numa pasta de categoria em `sons/`:

| Pasta | Vídeo | O que tem |
| --- | --- | --- |
| `efeitos-sonoros-diversos/` | 4 | 10 efeitos de edição |
| `gancho-impacto-viral/` | 1 | 8 sons de meme |
| `storytelling-impacto-atencao/` | 2 | 10 loops de trilha |
| `conexao-vibes-lifestyle-dia-a-dia-ostentacao/` | 3 | 7 trechos de músicas comerciais |

Cada arquivo é chamado pelo próprio nome na marcação (`"som": "impact"`). Os sons soltos em `sons/` são sintetizados e ficam só de reserva: quando um som real tem o mesmo nome (`riser`, `pop`, `counter`, `glitch`, `money`), o real é o usado.

## Os dois estilos

As referências usam efeito sonoro de dois jeitos diferentes. Descubra qual o vídeo pede antes de marcar qualquer coisa.

**Estilo edição** (vídeo 4, do editor no estúdio). O efeito acompanha a montagem: corte, texto que entra, número na tela, transição. É o padrão para vídeo de dica, tutorial e autoridade, com a pessoa falando para a câmera.

**Estilo meme** (vídeo 1, do criador na sala). O efeito acompanha o **gesto e a expressão** da pessoa: ela leva a mão à cabeça e entra o vine boom, se joga no sofá e entra o osso estalando, faz joinha e entra o som de resposta certa. Aqui o gatilho não está na fala, está na imagem. Por isso a análise precisa olhar as folhas de quadros (`--folhas`). É o estilo do humor, da encenação e do "POV".

Um vídeo pode misturar os dois, mas em geral um manda.

## Quanto usar

- **No estilo edição, um efeito a cada 2 a 4 segundos, no máximo.** Em vídeo de 30 s, algo entre 8 e 15 marcações.
- **No estilo meme, um efeito por gesto que conta a piada**, e nenhum nos gestos de transição. O vídeo 1 tem 8 efeitos em 14 s porque é uma vitrine de sons. Num vídeo de verdade, dois já bastam.
- **Nunca dois efeitos no mesmo instante.** A exceção é o riser terminando onde entra um boom ou impact.
- **O mesmo efeito não aparece três vezes seguidas.** Se três cortes seguidos pedem woosh, um fica sem nada ou vira mouse-click.
- **A voz manda.** O efeito fica abaixo da fala. Se ele cobre uma palavra, abaixe o volume ou mude o tempo.

## Efeitos sonoros diversos (estilo edição)

Os dez efeitos do vídeo 4 ficam em `sons/efeitos-sonoros-diversos/`. São os originais recortados do vídeo de referência, limpos: no vídeo, cada um tinha silêncio total antes e depois e nenhuma voz por cima. São a primeira escolha para o estilo edição.

| `som` | Quando | Volume inicial |
| --- | --- | --- |
| `woosh` | Transição, corte com mudança de enquadramento, elemento que entra deslizando. | 0.5 a 0.7 |
| `pop` | Texto, emoji, ícone ou elemento que aparece na tela. Item de lista. | 0.5 a 0.6 |
| `mouse-click` | Clique ou toque na tela do computador ou do celular, selecionar algo, trocar de aba. Também serve de woosh discreto. | 0.4 a 0.6 |
| `camera-shutter` | Print, foto, quadro congelado, imagem estática que entra na tela. | 0.5 a 0.7 |
| `counter` | Número subindo na tela (faturamento, seguidores, contagem), ranking passando. | 0.4 a 0.5 |
| `riser` | Prepara um momento: termina (`"alinhar": "fim"`) exatamente onde entra a revelação, o impact ou o corte grande. Muito bom terminando no fim do gancho. Tem só 0,6 s: é uma subida curta. | 0.4 a 0.6 |
| `impact` | Impacto: a frase de virada, a revelação, o título grande. No máximo 1 ou 2 por vídeo. | 0.6 a 0.8 |
| `glitch` | Erro, falha, "travou", troca brusca, assunto de tecnologia ou IA. | 0.4 a 0.6 |
| `money` | Dinheiro, venda, preço, faturamento, "isso vale R$...". | 0.5 a 0.6 |
| `correct-ding` | Acerto, check, "é isso", resposta certa, a ideia principal que fecha. No máximo 1 ou 2 por vídeo. | 0.5 |

Os arquivos vêm no volume cheio, quase no limite. Comece pelo volume da tabela e nunca passe de 0.8.

Sem versão real, só sintetizada, ficam: `whoosh` (use `woosh`), `click` (use `mouse-click`), `camera` (use `camera-shutter`), `boom` (use `impact`), `correct` e `ding` (use `correct-ding`), `error`, `punch` e `crack`. Use os sintetizados só quando nenhum real servir.

## Gancho, impacto e viral

Os oito sons do vídeo 1 ficam em `sons/gancho-impacto-viral/`. São os originais recortados do vídeo de referência, e cada um é chamado pelo próprio nome na marcação (`"som": "vine-boom"`). Eles servem para três momentos:

- **Gancho** (primeiros 3 segundos): um som que para o dedo de quem rola o feed. O `fahhh` na frustração da abertura, o `vine-boom` na frase que choca, o `dexter-meme` no olhar fixo antes da revelação.
- **Impacto**: a virada, a revelação, o tapa da frase. `vine-boom`, `punch-gaming` ou `bone-crack`.
- **Viral**: o momento de meme que a pessoa vai querer mandar para alguém. Cada som acompanha o gesto da tabela abaixo.

| Na tela | `som` |
| --- | --- |
| Olha o celular e se frustra, "deu ruim" | `fahhh` |
| Se joga no sofá, tomba, cai | `bone-crack` |
| Mãos na cabeça, choque, olhar para a câmera depois de algo absurdo | `vine-boom` |
| Encara a câmera em silêncio, suspense irônico | `dexter-meme` |
| Paga ou compra pelo celular | `applepay` |
| Coça a cabeça, confuso, errou | `error-meme` |
| Soca, chuta, ação física na direção da câmera | `punch-gaming` |
| Joinha, aprovação, "aprovado" | `answer-correct` |

No vídeo 1, cada som começa junto com o gesto e dura enquanto o gesto dura.

Prefira estes aos sintetizados sempre que o momento for de gancho, impacto ou meme. O `error-meme` tem esse nome para não se confundir com o `error` sintetizado do estilo edição.

Cuidados com estes arquivos:
- Vêm de um vídeo do Instagram, com o áudio comprimido. Os mais usados merecem ser trocados pelo original em alta qualidade, com o mesmo nome de arquivo.
- O `fahhh`, o `vine-boom` e o `dexter-meme` estão mais curtos que o meme original, porque o criador cortou cada um para entrar o som seguinte.
- O `applepay` é bem mais baixo que os outros. Marque com volume perto de 1.0.
- Use **no máximo dois por vídeo**. Meme repetido perde a graça.

## Gatilhos na fala

Pistas para o estilo edição, não regras automáticas:

- **Virada:** "mas", "só que", "porém", "aí que", "o problema é". Pede `impact`, ou um corte com `woosh`.
- **Revelação:** "o segredo", "a resposta", "na verdade", "olha isso". Pede `correct-ding` ou `impact`, com `riser` antes se houver tempo.
- **Listas:** "primeiro", "segundo", "número 1", "dica 2". Pede `pop` ou `mouse-click` em cada item.
- **Dinheiro:** preço, "faturei", "vendi", "R$". Pede `money`.
- **Números** que sobem na tela ou são ditos com ênfase. Pede `counter` ou `pop`.

## Storytelling, impacto e prender atenção

Os dez loops do vídeo 2 ficam em `sons/storytelling-impacto-atencao/`. Cada loop é chamado pelo próprio nome na marcação. São trechos curtos (2 a 6 segundos) de loops instrumentais. Entram **por baixo** da fala, para dar clima a um trecho da história, e não como efeito pontual.

Os arquivos são a versão **com a voz do criador original**, como estão no vídeo de referência. Foi escolha da agência, porque a versão sem voz perdia qualidade. A voz dele fica audível por baixo da sua. Por isso, use volume baixo.

| `som` | Clima | Use quando |
| --- | --- | --- |
| `question` | curiosidade | o vídeo abre com uma pergunta |
| `into-the-fog` | mistério | algo ainda não foi explicado |
| `quiet-suspicion` | desconfiança | "tem alguma coisa errada aqui" |
| `lost-in-thought` | reflexão | a pessoa pensa alto, fala de um erro, conta um momento difícil |
| `in-between` | transição | passagem de uma parte da história para a próxima |
| `keep-moving` | ritmo, avanço | lista de passos, "e aí eu fui fazendo" |
| `reckoning` | acerto de contas | a revelação, o momento em que a verdade aparece |
| `second-guess` | dúvida | "será que eu tava certo?", a objeção do público |
| `forward-motion` | progresso | a virada para o resultado, o "depois" |
| `pizzicato-clock` | tempo, urgência | prazo, "você tem pouco tempo", contagem |

Como usar:
- **Um loop por trecho da história**, mudando quando o clima muda. É o que o vídeo 2 faz: a música troca a cada 2 a 5 segundos, sempre junto com a virada da fala.
- **Storytelling:** acompanhe a história com a sequência de climas (por exemplo `question` → `into-the-fog` → `reckoning` → `forward-motion`).
- **Impacto:** `reckoning` na revelação. Pode somar com um `vine-boom` ou `impact` no mesmo ponto.
- **Prender atenção:** troque de loop num ponto em que a pessoa poderia sair do vídeo. A mudança de som reacende a atenção.
- **Volume de 0.2 a 0.35.** Mais alto que isso cobre a sua voz e deixa a voz do criador original aparecer.
- Os trechos não se repetem sozinhos e têm entrada e saída suaves. Se o trecho da história for mais longo que o loop, emende o próximo loop do clima seguinte em vez de esticar o mesmo.

## Conexão, vibes, lifestyle, dia a dia e ostentação

Os sete trechos de música do vídeo 3 ficam em `sons/conexao-vibes-lifestyle-dia-a-dia-ostentacao/`. Cada um tem de 2 a 2,6 segundos, o pedaço que o vídeo de referência mostra. Entram por baixo da fala, como os loops de storytelling, para dar a cara do vídeo.

O clima abaixo vem do que se conhece de cada música. Os trechos não foram ouvidos na hora de montar esta tabela: ajuste se algum não bater.

| `som` | Música | Categoria | Use quando |
| --- | --- | --- | --- |
| `echo-sax` | Echo Sax, Caleb Arredondo | Conexão | momento emocional, bastidor, história pessoal |
| `death-of-a-bluebird` | Death of a Bluebird, Rorschach Roy | Conexão | reflexão, vulnerabilidade, virada de vida |
| `blade-runner-2049` | Blade Runner 2049, Synthwave Goose | Vibes | estética, noite, cidade, clima de filme |
| `goth` | Goth, Sidewalks and Skeletons | Vibes | atmosfera escura, mistério, estética |
| `hell-n-back` | Hell N Back, Bakar | Lifestyle, dia a dia | rotina, "um dia comigo", leveza |
| `timeless` | Timeless, The Weeknd | Ostentação | conquista, resultado, compra, viagem |
| `million-dollar-baby` | Million Dollar Baby, Tommy Richman | Ostentação, lifestyle | confiança, estilo, "chegou lá" |

Volume de 0.2 a 0.35 por baixo da fala. Sem fala, como num trecho só de imagem, até 0.7.

**Direitos autorais.** São músicas comerciais. Vídeo postado com elas embutidas pode ser silenciado ou derrubado pelo Instagram. A skill coloca a música para a agência ver como fica. Toda vez que usar uma destas, avise na entrega e lembre que a versão que vai ao ar deve receber a música pela biblioteca do próprio Instagram, com o arquivo sem ela.

## Vídeos de referência

1. https://www.instagram.com/p/DeEur5kx7eI/ : estilo meme, 8 sons ligados a gestos. Recortados em `sons/gancho-impacto-viral/`.
2. https://www.instagram.com/p/DZFgpDNhwb-/ : 10 loops de storytelling. Recortados em `sons/storytelling-impacto-atencao/`.
3. https://www.instagram.com/p/DJiR_oVIV9N/ : 7 músicas comerciais. Trechos em `sons/conexao-vibes-lifestyle-dia-a-dia-ostentacao/`.
4. https://www.instagram.com/p/DGtcBb8vqnR/ : estilo edição, 10 sons. Recortados em `sons/efeitos-sonoros-diversos/`.

A ordem dos links segue a ordem dos arquivos que a agência mandou (Video 1 a Video 4). A ligação entre cada link e cada arquivo não foi conferida.
