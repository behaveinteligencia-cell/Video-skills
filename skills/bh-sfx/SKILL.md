---
name: bh-sfx
description: Coloca efeitos sonoros (woosh, pop, mouse click, riser, impact, glitch, money, correct ding e sons de meme como vine boom, fahhh e dexter) por cima do áudio de um vídeo já editado, seguindo a montagem ou os gestos da pessoa, e entrega o vídeo pronto mais uma faixa só com os efeitos para ajustar no CapCut, Premiere ou DaVinci. Use SEMPRE que pedirem "coloca efeito sonoro", "põe os sons no vídeo", "sound design do reels", "sfx", "whoosh nos cortes", "vine boom", "som de meme", "deixa o vídeo mais dinâmico com som", "efeitos sonoros igual aos influenciadores", "bh-sfx", ou mandarem um vídeo pedindo os efeitos de edição. Também analisa um vídeo de referência para aprender onde ele usa efeito sonoro ("analisa os sons desse reels", "que efeitos esse vídeo usa") e coloca por baixo da fala loops de storytelling e trechos de música (conexão, vibes, lifestyle, ostentação). Não use para limpar ruído do áudio (melhorar_audio do Worxpace) nem para cortar o vídeo (bh-videos).
---

# bh-sfx

Efeito sonoro bom é o que a pessoa não percebe como efeito: ele marca o corte, sublinha a frase que importa e some. Efeito demais vira barulho e cansa em dez segundos. Na dúvida entre colocar e tirar, tire.

## O que precisa estar instalado

- **ffmpeg** e **ffprobe** no PATH. No Windows: `winget install ffmpeg`. No Mac: `brew install ffmpeg`.
- **Python 3** com `numpy` (`pip install numpy`).
- Para a skill saber o que é falado e quando, **faster-whisper** (`pip install faster-whisper`). Sem ele, peça a legenda em `.srt` (o CapCut e o Premiere exportam) e passe com `--transcricao`. Sem nenhum dos dois, dá para trabalhar só com os cortes e as pausas, mas avise que as marcações por fala ficaram de fora.

Os scripts ficam em `scripts/` e os sons em `sons/`, dentro da pasta desta skill (o diretório base informado quando a skill é carregada; ele muda conforme a instalação, então não assuma `~/.claude/skills/`). Os comandos abaixo rodam na pasta do vídeo, então chame os scripts pelo caminho completo da skill, como `python "<diretório base da skill>/scripts/analisar.py"`. Onde estiver escrito `SKILL/`, troque por esse caminho.

## Colocar efeitos num vídeo

1. **Analise o vídeo.**
   ```
   python SKILL/scripts/analisar.py VIDEO.mp4 --folhas quadros/ > analise.json
   ```
   O JSON traz a duração, os `cortes` (troca de cena), as `pausas` da fala, as `palavras` com o tempo de cada uma e as `folhas`: imagens em `quadros/` com dois quadros por segundo e o tempo escrito em cada um. **Abra as folhas e olhe.** Elas mostram o que o áudio não mostra: o texto que entra na tela, o print, o número, o gesto. No estilo meme, o gatilho do efeito está todo nelas. Em vídeo de uma pessoa falando para a câmera, o corte seco quase não muda a imagem e pode não aparecer em `cortes`. Nesse caso o fim de cada pausa costuma ser o ponto do corte. Se ainda faltar corte, rode de novo com `--limiar-corte 0.15`.

2. **Leia `references/regras.md`**, decida se o vídeo pede o estilo edição ou o estilo meme, e se pede trilha por baixo da fala (loop de storytelling ou música), e marque. Cada marcação precisa de um motivo que caiba numa linha: um corte, uma palavra, um número que aparece, a virada da frase, um gesto. Sem motivo, não entra. Se não der para saber o estilo pelo vídeo, pergunte antes de marcar.

3. **Escreva o arquivo de marcações** ao lado do vídeo, com o motivo de cada uma:
   ```json
   {"marcacoes": [
     {"t": 0.00, "som": "riser", "volume": 0.4, "alinhar": "fim", "motivo": "abre no gancho"},
     {"t": 1.84, "som": "woosh", "volume": 0.6, "motivo": "corte para o close"},
     {"t": 6.30, "som": "correct-ding", "volume": 0.5, "motivo": "\"o segredo é...\""}
   ]}
   ```
   `t` é o segundo em que o som começa. Com `"alinhar": "fim"` o som termina em `t`, que é o certo para o riser (sobe até o momento) e às vezes para o woosh (chega junto com o corte).

4. **Gere o vídeo.**
   ```
   python SKILL/scripts/aplicar_sfx.py VIDEO.mp4 marcacoes.json
   ```
   Saem dois arquivos ao lado do vídeo: `VIDEO_sfx.mp4`, com tudo misturado, e `VIDEO_sfx_faixa.wav`, só com os efeitos, do segundo 0 até o fim. A faixa é o que a pessoa solta no editor por cima do vídeo original para mexer à mão. A imagem não é recodificada, então o vídeo não perde qualidade. Se uma marcação cair inteira fora do vídeo, o script avisa e ignora. Se os efeitos ficarem altos ou baixos no conjunto, rode de novo com `--volume-geral 0.7` (ou 1.3) em vez de reescrever as marcações.

5. **Entregue** os dois arquivos com a lista das marcações em tabela curta (tempo, efeito, motivo) e uma linha de como ajustar: "quer menos, mais alto ou trocar algum, me diz o tempo". Se usou um trecho de `conexao-vibes-lifestyle-dia-a-dia-ostentacao/`, avise que é música comercial: a versão que vai ao ar deve receber a música pela biblioteca do Instagram, senão o vídeo pode ser silenciado.

## Analisar um vídeo de referência

Quando mandarem um vídeo de criador para a skill aprender o estilo:

```
python SKILL/scripts/analisar.py REFERENCIA.mp4 --picos > referencia.json
```

Gere também as folhas (`--folhas quadros/`) e olhe primeiro: vídeo de "meus efeitos favoritos" costuma mostrar o nome de cada arquivo na tela, e aí o trabalho é só ler. Confira também se o vídeo é mesmo de efeito sonoro. Vídeo de "músicas para viralizar" ou de loops é de trilha: os trechos entram por baixo da fala, não como efeito pontual.

`picos` lista os ataques fortes no áudio: lugares prováveis de efeito sonoro, mas também de palavras com ênfase e batidas da música. Cruze cada pico com `cortes`, `palavras` e as folhas, monte uma tabela (tempo, o que acontece na tela ou na fala, efeito provável) e peça para a pessoa confirmar o tipo de cada som. Você não escuta o áudio, e chutar o tipo do efeito estraga a regra que vai sair dali. Com as respostas, atualize `references/regras.md`: o que dispara cada efeito, quantos por vídeo, o volume em relação à voz.

Recorte os sons do vídeo de referência só quando a agência pedir. Antes, veja se o som está sozinho no áudio (silêncio antes e depois, sem voz por cima, como nos vídeos 1 e 4) ou misturado com voz e música, e diga isso na entrega. Os recortes entram numa pasta de categoria que a agência nomear.

## Trocar ou acrescentar sons

Os sons ficam em pastas de categoria dentro de `sons/`, recortados dos vídeos de referência: `efeitos-sonoros-diversos/`, `gancho-impacto-viral/`, `storytelling-impacto-atencao/` e `conexao-vibes-lifestyle-dia-a-dia-ostentacao/`. O que cada pasta tem e quando usar está em `references/regras.md`. Cada arquivo é chamado pelo próprio nome (`"som": "vine-boom"`), e o nome da pasta alterna entre os arquivos dela.

Os sons soltos em `sons/` foram sintetizados por `scripts/gerar_sons_base.py` e ficam de reserva. Quando uma pasta tem um som de mesmo nome, o da pasta ganha. Para trocar um som, salve o novo arquivo com o mesmo nome na mesma pasta. Para variar, crie uma pasta com o nome do efeito (`sons/woosh/`) com várias versões: a skill alterna entre elas. Som de meme só funciona se for o original, porque a graça está em reconhecer. Efeito novo é só colocar o arquivo numa pasta e descrever em `references/regras.md` quando ele entra.
