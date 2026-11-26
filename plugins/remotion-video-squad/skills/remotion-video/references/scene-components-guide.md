# Guia de Componentes e Padrões de Cena

## Tipos de Cena por Função Narrativa

### Cena de Abertura (Intro)
**Objetivo**: Capturar atenção nos primeiros 2-3s
**Componentes típicos**: título bold, subtítulo, fundo marcante
**Animações**: fade in + scale pop no título, slide up no subtítulo
**Duração sugerida**: 3-5s (90-150 frames)

```
Estrutura visual:
┌─────────────────────────────────┐
│                                 │
│                                 │
│        TÍTULO PRINCIPAL         │  ← bold, grande (60-120px)
│        subtítulo menor          │  ← 30-40px
│                                 │
│                                 │
└─────────────────────────────────┘
```

### Cena de Problema (Problem)
**Objetivo**: Criar identificação com a dor do usuário
**Componentes**: ícone de "X" ou emoji, texto do problema, animação de desconforto
**Animações**: shake, fade in de texto por partes
**Duração sugerida**: 4-6s (120-180 frames)

### Cena de Solução (Solution)
**Objetivo**: Apresentar o produto/ideia como resposta ao problema
**Componentes**: logo, nome do produto, bullets de benefícios, tick verde
**Animações**: transição suave da cena de problema, elementos entrando sequencialmente
**Duração sugerida**: 5-8s (150-240 frames)

### Cena de Demo/Feature (Demo)
**Objetivo**: Mostrar o produto em ação (mockup de tela, GIF, vídeo)
**Componentes**: frame de dispositivo, screenshot/vídeo inner, legenda
**Animações**: slide in do dispositivo, fade in do conteúdo
**Duração sugerida**: 5-10s (150-300 frames)

### Cena de Prova Social (Social Proof)
**Objetivo**: Construir credibilidade com dados, depoimentos, logos
**Componentes**: número grande (ex: "10.000+ clientes"), citação, avatar
**Animações**: counter animado (0 → número), fade in de citação
**Duração sugerida**: 3-5s (90-150 frames)

### Cena de CTA (Call to Action)
**Objetivo**: Converter — levar o usuário a tomar ação
**Componentes**: texto de CTA, URL ou @handle, botão animado
**Animações**: pulse no botão, fundo vibrante, confetes (opcional)
**Duração sugerida**: 3-5s (90-150 frames)

## Biblioteca de Componentes Reutilizáveis

### AnimatedTitle
```tsx
// Título que entra com spring + fade
const AnimatedTitle: React.FC<{ text: string; delay?: number }> = ({ text, delay = 0 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  
  const opacity = interpolate(frame - delay, [0, 15], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const y = spring({ frame: frame - delay, fps, from: 30, to: 0, config: { damping: 80 } });
  
  return (
    <div style={{
      opacity,
      transform: `translateY(${y}px)`,
      fontSize: 80,
      fontWeight: 900,
      color: "white",
      textAlign: "center",
    }}>
      {text}
    </div>
  );
};
```

### GradientBackground
```tsx
// Fundo com gradiente animado
const GradientBackground: React.FC<{ from: string; to: string }> = ({ from, to }) => {
  const frame = useCurrentFrame();
  const angle = interpolate(frame, [0, 300], [135, 225]);
  
  return (
    <AbsoluteFill style={{
      background: `linear-gradient(${angle}deg, ${from}, ${to})`,
    }} />
  );
};
```

### CounterNumber
```tsx
// Número que conta de 0 até o target
const CounterNumber: React.FC<{ target: number; suffix?: string }> = ({ target, suffix = "" }) => {
  const frame = useCurrentFrame();
  const value = Math.round(interpolate(frame, [0, 60], [0, target], { extrapolateRight: "clamp" }));
  
  return (
    <div style={{ fontSize: 120, fontWeight: 900, color: "white" }}>
      {value.toLocaleString()}{suffix}
    </div>
  );
};
```

### PillBadge
```tsx
// Badge colorida (como na demo da Deborah Folloni)
const PillBadge: React.FC<{ text: string; color: string; delay?: number }> = ({ text, color, delay = 0 }) => {
  const frame = useCurrentFrame();
  const scale = spring({ frame: frame - delay, fps: 30, from: 0, to: 1, config: { damping: 50 } });
  
  return (
    <div style={{
      transform: `scale(${scale})`,
      backgroundColor: color,
      borderRadius: 50,
      padding: "8px 24px",
      fontSize: 28,
      fontWeight: 700,
      color: "white",
      display: "inline-block",
    }}>
      {text}
    </div>
  );
};
```

### ProgressBar
```tsx
// Barra de progresso animada
const ProgressBar: React.FC<{ color: string }> = ({ color }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const width = interpolate(frame, [0, durationInFrames], [0, 100]);
  
  return (
    <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: 6, backgroundColor: "rgba(255,255,255,0.2)" }}>
      <div style={{ width: `${width}%`, height: "100%", backgroundColor: color }} />
    </div>
  );
};
```

## Paletas de Cores por Estilo

### Minimalista
```
Fundo: #FFFFFF ou #F8F8F8
Texto: #0F0F0F
Destaque: #0066FF
Secundário: #666666
```

### Dark Tech
```
Fundo: #0A0A0A
Texto: #FFFFFF
Destaque: #7C3AED (roxo neon) ou #00FF88 (verde neon)
Secundário: #333333
```

### Colorido/Vibrante
```
Fundo: #FF6B6B → #4ECDC4 (gradiente)
Texto: #FFFFFF
Destaque: #FFE66D (amarelo)
Secundário: #292F36
```

### Corporativo
```
Fundo: #1A237E (azul escuro) ou #FFFFFF
Texto: #FFFFFF ou #212121
Destaque: #1565C0
Secundário: #B0BEC5
```

## Tipografia Recomendada (Google Fonts via @remotion/google-fonts)

```tsx
import { loadFont } from "@remotion/google-fonts/Inter";
import { loadFont as loadPoppins } from "@remotion/google-fonts/Poppins";
import { loadFont as loadSpaceGrotesk } from "@remotion/google-fonts/SpaceGrotesk";

// Para tech/startup: Inter ou Space Grotesk
// Para marketing/criativo: Poppins ou Outfit
// Para impacto: Black Han Sans ou Oswald
```

Ou via staticFile se a fonte for customizada:
```tsx
<style>{`
  @font-face {
    font-family: 'CustomFont';
    src: url('${staticFile("fonts/CustomFont-Bold.woff2")}') format('woff2');
  }
`}</style>
```

## Transições entre Cenas

### Fade (mais comum e clean)
```tsx
// No início de cada cena: fade in
const fadeIn = interpolate(frame, [0, 15], [0, 1], { extrapolateRight: "clamp" });

// No final de cada cena: fade out
const fadeOut = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {
  extrapolateLeft: "clamp",
});

const opacity = Math.min(fadeIn, fadeOut);
```

### Slide Horizontal
```tsx
// Cena nova entra da direita
const x = interpolate(frame, [0, 20], [width, 0], { extrapolateRight: "clamp" });
// style={{ transform: `translateX(${x}px)` }}
```

### Scale Zoom
```tsx
const scale = interpolate(frame, [0, 20], [1.1, 1], { extrapolateRight: "clamp" });
// Cria efeito de "zoom out" na entrada
```
