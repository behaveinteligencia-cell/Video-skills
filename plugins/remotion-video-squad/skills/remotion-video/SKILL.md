---
name: remotion-video
description: >
  Use this skill when the user wants to create a video with Remotion, generate
  animated video content, run the Remotion squad, or transform an idea into
  Remotion code. Triggers on: "criar vídeo remotion", "gerar vídeo com remotion",
  "animação remotion", "squad remotion", "fazer vídeo remotion", "video remotion
  do zero", "rodar o squad de vídeo", "quero um vídeo sobre", "criar animação
  com react remotion".
metadata:
  version: "0.1.0"
  author: "Agência Behave"
---

# Remotion Video Squad

Orquestre o squad completo de 3 agentes para transformar uma ideia em um vídeo Remotion com roteiro, arquitetura de cenas e código TSX prontos para usar no Claude Code.

## Visão Geral do Workflow

```
USUÁRIO (prompt/ideia)
        ↓
  [COLETA DE BRIEFING]
        ↓
  [AGENTE: Roteirista]  →  roteiro.md
        ↓
  [AGENTE: Arquiteto de Cenas]  →  arquitetura-cenas.md
        ↓
  [AGENTE: Dev Remotion]  →  src/*.tsx + prompt-remotion-final.md
        ↓
  [CONSOLIDAÇÃO]  →  todos os arquivos + COMO-USAR.md
```

## Conceitos Remotion que os agentes devem conhecer

Antes de orquestrar os agentes, internalizar esta arquitetura:

- **Composition**: o vídeo inteiro
- **Scene**: cada parte do vídeo (ex: Cena 1, Cena 2...)
- **Component**: elemento animável dentro de uma cena (texto, imagem, shape, etc.)
- **`/public`**: pasta de assets (fontes, imagens, vídeos, GIFs, áudios)
- **`/src`**: pasta de código (cenas + componentes + arquivo principal)
- **`useCurrentFrame()`**: hook para acessar o frame atual e criar animações
- **`interpolate()`**: função para mapear frames em valores animados
- **`spring()`**: animações com física (entrada suave)
- **`AbsoluteFill`**: container full-screen para cenas

## Fase 1 — Coleta de Briefing

Usar `AskUserQuestion` para coletar as seguintes informações (em uma única pergunta multiescolha agrupada ou em sequência lógica):

### Pergunta 1 — Tema e Objetivo
Perguntar:
- Qual é o tema/ideia principal do vídeo?
- Qual é o objetivo? (apresentar produto, explicar conceito, promover serviço, conteúdo educacional, etc.)
- Qual é a audiência?

### Pergunta 2 — Formato e Duração
Opções sugeridas:
- 15 segundos (reel/story)
- 30 segundos (anúncio curto)
- 60 segundos (explicativo)
- 90 segundos (apresentação completa)

### Pergunta 3 — Estilo Visual
Opções:
- Minimalista (fundo limpo, tipografia bold, poucos elementos)
- Colorido/Vibrante (gradientes, confetes, cores saturadas)
- Corporativo (azul/cinza, sério, profissional)
- Dark Mode (fundo escuro, neon, tech)
- Personalizado (usuário descreve)

### Pergunta 4 — Assets Disponíveis
Perguntar se o usuário já tem:
- Logo (formato PNG com transparência?)
- Imagens específicas?
- Fonte customizada?
- Paleta de cores definida (hex)?
- Vídeo de fundo ou GIF?

Se não tiver assets, registrar que o código deve usar apenas cores sólidas, gradientes CSS e tipografia do sistema.

## Fase 2 — Executar Agente Roteirista

Após coletar o briefing, lançar o agente `roteirista` com o seguinte contexto completo:

```
BRIEFING:
- Tema: [tema coletado]
- Objetivo: [objetivo coletado]  
- Audiência: [audiência coletada]
- Duração: [duração escolhida]
- Estilo: [estilo escolhido]
- Assets disponíveis: [lista de assets ou "nenhum"]
- Paleta de cores: [cores ou "livre"]
```

O agente roteirista deve retornar um roteiro com:
- Número de cenas (4-8 cenas para vídeos de 15-90s)
- Título de cada cena
- Descrição narrativa do que acontece
- Texto/copy que aparece na tela
- Emoção/mood de cada cena
- Duração sugerida em segundos

## Fase 3 — Executar Agente Arquiteto de Cenas

Com o roteiro gerado, lançar o agente `arquiteto-cenas` com:

```
ROTEIRO: [output completo do roteirista]
ESTILO: [estilo escolhido pelo usuário]
ASSETS: [lista de assets disponíveis]
PALETA: [cores definidas]
```

O arquiteto deve retornar para CADA CENA:
- Nome do componente TSX (ex: `SceneIntro`, `SceneDemo`)
- Duração em frames (30fps: 1s = 30 frames)
- Lista de sub-componentes (ex: `TitleText`, `SubtitleText`, `LogoImage`)
- Animações por componente (entrada, saída, efeito)
- Cores, fontes e estilos específicos
- Assets referenciados da pasta `/public`

## Fase 4 — Executar Agente Dev Remotion

Com a arquitetura completa, lançar o agente `dev-remotion` com:

```
ROTEIRO: [output do roteirista]
ARQUITETURA: [output do arquiteto-cenas]
ESTILO: [estilo visual]
ASSETS: [assets disponíveis]
DURAÇÃO TOTAL: [duração em frames]
```

O Dev Remotion deve gerar:
1. Um arquivo TSX por cena (`Scene01Intro.tsx`, `Scene02Demo.tsx`, etc.)
2. O arquivo principal de composição (`MainComposition.tsx`)
3. O prompt estruturado final para Claude Code (`prompt-remotion-final.md`)
4. O checklist de assets (`assets-checklist.md`)

## Fase 5 — Salvar Todos os Arquivos

Após receber os outputs de todos os agentes, salvar os seguintes arquivos em `/sessions/nifty-busy-tesla/mnt/outputs/remotion-video/`:

### Arquivos a criar:

1. **`roteiro.md`** — output completo do agente roteirista
2. **`arquitetura-cenas.md`** — output completo do agente arquiteto
3. **`src/Scene01[NomeCena].tsx`** — um arquivo por cena
4. **`src/MainComposition.tsx`** — arquivo de composição principal
5. **`prompt-remotion-final.md`** — prompt estruturado para Claude Code
6. **`assets-checklist.md`** — lista de assets necessários em `/public`
7. **`COMO-USAR.md`** — instruções de instalação e uso

### Conteúdo de COMO-USAR.md:

```markdown
# Como usar este projeto Remotion

## 1. Instale o Remotion Skills no Claude Code
npx skills add remotion-dev/skills

## 2. Crie um projeto Remotion (se não tiver)
npx create-video@latest

## 3. Copie os arquivos
- Copie a pasta `src/` para dentro do seu projeto Remotion
- Adicione os assets listados em `assets-checklist.md` na pasta `/public`

## 4. Gere/refine com Claude Code
- Abra Claude Code na pasta do projeto
- Cole o conteúdo de `prompt-remotion-final.md` no Claude Code
- O Claude vai gerar/ajustar o código com Remotion Skills

## 5. Visualize no Remotion Studio
npx remotion studio

## 6. Itere cena por cena
- Veja uma cena por vez no Studio
- Peça ajustes específicos ao Claude Code
- Repita até ficar perfeito

## 7. Renderize o vídeo final
npx remotion render
```

## Fase 6 — Apresentar Resultados

Ao final, apresentar ao usuário:
- Link para cada arquivo gerado
- Resumo do que foi criado (quantas cenas, duração total, componentes principais)
- Próximos passos claros (como usar com Claude Code)

Usar linguagem encorajadora e objetiva. Destacar que o `prompt-remotion-final.md` é o arquivo mais importante — é ele que o usuário cola no Claude Code para gerar o vídeo final.

## Referências

Para detalhes de arquitetura Remotion, templates de cena e exemplos de código, consultar os arquivos em `references/`.
