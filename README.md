# Skills de vídeo da Agência Behave

Skills do Claude para produzir, animar e finalizar vídeos. Cada pasta em `skills/` é uma skill completa, com o `SKILL.md` e os arquivos de apoio. Em `plugins/` fica o squad de Remotion, que vem com agentes e por isso é instalado como plugin.

A `bh-videos` fica de fora deste repositório.

## Skills

### Vídeo animado do zero com HyperFrames (vídeo feito em HTML)

| Skill | O que faz |
| --- | --- |
| [`hyperframes`](skills/hyperframes/SKILL.md) | Cria composições, títulos, sobreposições, legendas sincronizadas, narração, animação que reage ao áudio, destaques de texto animados e transições entre cenas. É a skill principal do HyperFrames. |
| [`hyperframes-cli`](skills/hyperframes-cli/SKILL.md) | Comandos `npx hyperframes` para criar o projeto, validar, pré-visualizar e renderizar, e para resolver problemas do ambiente de render. |
| [`hyperframes-media`](skills/hyperframes-media/SKILL.md) | Prepara os arquivos: narração por voz sintética (Kokoro), transcrição para legenda (Whisper) e remoção de fundo para usar como camada transparente. |
| [`hyperframes-registry`](skills/hyperframes-registry/SKILL.md) | Instala blocos e componentes prontos do registro e encaixa nas composições. |
| [`website-to-hyperframes`](skills/website-to-hyperframes/SKILL.md) | Recebe a URL de um site e transforma em vídeo: anúncio, tour do produto ou lançamento. |

### Vídeo animado do zero com Remotion (React)

| Plugin | O que faz |
| --- | --- |
| [`remotion-video-squad`](plugins/remotion-video-squad/README.md) | Squad com três agentes em sequência: o roteirista escreve o roteiro em cenas, o arquiteto de cenas transforma em especificação técnica e o dev Remotion gera o código `.tsx`. A skill é `remotion-video`. |

### Produção com mídia gerada

| Skill | O que faz |
| --- | --- |
| [`hypit`](skills/hypit/SKILL.md) | Dirige e produz vídeos com Hypit a partir de briefing, referências ou material enviado, com mídia gerada e componentes animados. |

### Corte e finalização

| Skill | O que faz |
| --- | --- |
| [`buttercut-windows-setup`](skills/buttercut-windows-setup/SKILL.md) | Instala ou conserta o ButterCut (agente de corte bruto de vídeo) no Windows, onde o setup oficial não roda. |
| [`bh-sfx`](skills/bh-sfx/SKILL.md) | Coloca efeitos sonoros, sons de meme, loops de storytelling e trechos de música por cima do áudio de um vídeo editado. Entrega o vídeo pronto mais uma faixa só com os sons. Precisa de ffmpeg e Python. |

## Instalação

### Skills

Copie a pasta da skill para `~/.claude/skills/`:

```bash
git clone https://github.com/behaveinteligencia-cell/Video-skills.git
cp -r Video-skills/skills/hyperframes ~/.claude/skills/
cp -r Video-skills/skills/bh-sfx ~/.claude/skills/
# e assim por diante para cada skill
```

Para instalar todas de uma vez:

```bash
cp -r Video-skills/skills/* ~/.claude/skills/
```

Depois é só chamar `/hyperframes`, `/bh-sfx` etc. no Claude Code.

### Plugin do Remotion

O `remotion-video-squad` tem agentes, então entra como plugin. No Claude Code:

```bash
claude --plugin-dir Video-skills/plugins/remotion-video-squad
```

No claude.ai, compacte a pasta `plugins/remotion-video-squad` em `.zip` e envie como plugin da conta.

## Pré-requisitos

- **HyperFrames**: Node.js 22 ou superior e FFmpeg.
- **Remotion**: Node.js e um projeto Remotion para rodar o código gerado.
- **bh-sfx**: ffmpeg, Python 3 com `numpy` e, de preferência, `faster-whisper`.
- **ButterCut**: Windows com Python, ffmpeg e WhisperX (a skill instala o que faltar).
