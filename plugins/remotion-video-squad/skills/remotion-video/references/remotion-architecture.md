# Arquitetura Remotion — Referência Técnica

## Estrutura de Projeto

```
meu-video/
├── public/          ← TODOS os assets aqui (imagens, fontes, vídeos, GIFs, áudios)
│   ├── fonts/
│   ├── images/
│   └── videos/
├── src/
│   ├── scenes/      ← Um arquivo .tsx por cena
│   │   ├── Scene01Intro.tsx
│   │   ├── Scene02Demo.tsx
│   │   └── Scene03CTA.tsx
│   ├── components/  ← Componentes reutilizáveis
│   │   ├── AnimatedText.tsx
│   │   ├── LogoBounce.tsx
│   │   └── Confetti.tsx
│   └── MainComposition.tsx  ← Arquivo principal que monta tudo
├── package.json
└── remotion.config.ts
```

## Anatomia do Arquivo Principal (MainComposition.tsx)

```tsx
import { Composition } from "remotion";
import { Scene01Intro } from "./scenes/Scene01Intro";
import { Scene02Demo } from "./scenes/Scene02Demo";
import { Scene03CTA } from "./scenes/Scene03CTA";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="MainVideo"
        component={MainVideo}
        durationInFrames={900}   // 30s a 30fps
        fps={30}
        width={1920}
        height={1080}
      />
    </>
  );
};

// Componente que concatena as cenas
const MainVideo: React.FC = () => {
  return (
    <>
      <Series>
        <Series.Sequence durationInFrames={150}>  {/* 5s */}
          <Scene01Intro />
        </Series.Sequence>
        <Series.Sequence durationInFrames={300}>  {/* 10s */}
          <Scene02Demo />
        </Series.Sequence>
        <Series.Sequence durationInFrames={150}>  {/* 5s */}
          <Scene03CTA />
        </Series.Sequence>
      </Series>
    </>
  );
};
```

## Anatomia de uma Cena (Scene01Intro.tsx)

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, spring } from "remotion";

export const Scene01Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animação de entrada: fade in nos primeiros 20 frames
  const opacity = interpolate(frame, [0, 20], [0, 1], {
    extrapolateRight: "clamp",
  });

  // Animação com spring (física): slide up
  const translateY = spring({
    frame,
    fps,
    config: { damping: 80, stiffness: 200 },
    from: 50,
    to: 0,
  });

  return (
    <AbsoluteFill style={{ backgroundColor: "#0f0f0f" }}>
      <div
        style={{
          opacity,
          transform: `translateY(${translateY}px)`,
          fontSize: 80,
          color: "white",
          fontWeight: "bold",
          position: "absolute",
          top: "40%",
          left: "50%",
          transform: `translateX(-50%) translateY(${translateY}px)`,
        }}
      >
        Título Principal
      </div>
    </AbsoluteFill>
  );
};
```

## Tabela de Conversão: Tempo → Frames (30fps)

| Duração | Frames |
|---------|--------|
| 0.5s    | 15     |
| 1s      | 30     |
| 2s      | 60     |
| 3s      | 90     |
| 5s      | 150    |
| 10s     | 300    |
| 15s     | 450    |
| 30s     | 900    |
| 60s     | 1800   |
| 90s     | 2700   |

## Formatos de Saída Comuns

| Formato | Width | Height | Uso |
|---------|-------|--------|-----|
| Landscape HD | 1920 | 1080 | YouTube, apresentação |
| Square | 1080 | 1080 | Instagram feed |
| Portrait | 1080 | 1920 | Stories, Reels, TikTok |
| Widescreen | 1280 | 720 | Web, embed |

## Hooks Essenciais

### `useCurrentFrame()`
```tsx
const frame = useCurrentFrame();
// frame = número do frame atual (começa em 0)
```

### `useVideoConfig()`
```tsx
const { fps, width, height, durationInFrames } = useVideoConfig();
// fps = frames por segundo (padrão 30)
```

## Funções de Animação

### `interpolate()` — mapeia frames em valores
```tsx
// Opacidade de 0→1 nos frames 0→20
const opacity = interpolate(frame, [0, 20], [0, 1], {
  extrapolateLeft: "clamp",
  extrapolateRight: "clamp",
});

// Movimento de 0→100px nos frames 10→40
const x = interpolate(frame, [10, 40], [0, 100]);
```

### `spring()` — animação física suave
```tsx
const scale = spring({
  frame,
  fps,
  config: {
    damping: 100,    // amortecimento (maior = menos bounce)
    stiffness: 200,  // rigidez (maior = mais rápido)
    mass: 0.5,       // massa (maior = mais lento)
  },
  from: 0,
  to: 1,
});
```

## Padrões de Animação Comuns

### Fade In
```tsx
const opacity = interpolate(frame, [0, 20], [0, 1], { extrapolateRight: "clamp" });
```

### Fade Out (nos últimos 20 frames da cena)
```tsx
const opacity = interpolate(frame, [durationInFrames - 20, durationInFrames], [1, 0], {
  extrapolateLeft: "clamp",
});
```

### Slide In da Direita
```tsx
const x = spring({ frame, fps, from: 200, to: 0 });
// style={{ transform: `translateX(${x}px)` }}
```

### Scale Pop
```tsx
const scale = spring({ frame, fps, config: { damping: 50 }, from: 0, to: 1 });
// style={{ transform: `scale(${scale})` }}
```

### Typewriter (letra por letra)
```tsx
const text = "Olá Mundo!";
const lettersToShow = Math.floor(interpolate(frame, [0, 60], [0, text.length], {
  extrapolateRight: "clamp",
}));
const displayText = text.slice(0, lettersToShow);
```

## Usando Assets da Pasta /public

```tsx
import { staticFile } from "remotion";

// Imagem
<Img src={staticFile("images/logo.png")} />

// Vídeo
<Video src={staticFile("videos/background.mp4")} />

// Áudio
<Audio src={staticFile("audio/music.mp3")} />

// Fonte customizada (declarar no CSS global ou inline)
<style>{`
  @font-face {
    font-family: 'MinhaFonte';
    src: url('${staticFile("fonts/MinhaFonte.woff2")}');
  }
`}</style>
```

## Imports Remotion mais usados

```tsx
import {
  AbsoluteFill,      // container full-screen
  useCurrentFrame,   // frame atual
  useVideoConfig,    // config do vídeo (fps, width, height)
  interpolate,       // mapear frames → valores
  spring,            // animação física
  Sequence,          // temporizador de início
  Series,            // concatenador de sequências
  Img,               // imagem otimizada
  Video,             // vídeo otimizado
  Audio,             // áudio
  staticFile,        // referência a /public
  Easing,            // curvas de easing
} from "remotion";
```
