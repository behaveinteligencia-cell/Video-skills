# Template: Prompt Estruturado para Claude Code + Remotion Skills

Este é o formato exato do prompt final que o Dev Remotion deve gerar no arquivo `prompt-remotion-final.md`. Cole este prompt completo no Claude Code após instalar o Remotion Skills.

---

## Estrutura do Prompt Final

```markdown
# Prompt Remotion — [TÍTULO DO VÍDEO]

## Configuração Geral
- **ID da Composition**: [NomeDoVideo]
- **Duração total**: [X] frames ([Y] segundos a 30fps)
- **Resolução**: [1920x1080 / 1080x1080 / 1080x1920]
- **FPS**: 30
- **Estilo Visual**: [Minimalista / Dark / Colorido / Corporativo]
- **Paleta de cores**: 
  - Fundo: [hex]
  - Texto primário: [hex]
  - Destaque: [hex]
  - Secundário: [hex]

## Assets em /public
[Listar todos os arquivos que devem estar na pasta /public antes de rodar]
- `images/logo.png` — Logo da marca (PNG com transparência)
- `fonts/MinhaFonte-Bold.woff2` — Fonte bold customizada
- `videos/background.mp4` — Vídeo de fundo (opcional)

## Estrutura de Cenas

### Cena 1: [NomeDaCena1]
- **Componente**: `Scene01[NomeDaCena1].tsx`
- **Frames**: 0 a [X] ([Y]s)
- **Descrição**: [O que acontece narrativamente]
- **Copy na tela**: "[Texto exato que aparece]"
- **Componentes visuais**:
  - Background: [cor sólida / gradiente / vídeo]
  - Título: "[texto]" — fonte [X]px, cor [hex], posição [centro/esquerda/direita]
  - Subtítulo: "[texto]" — fonte [X]px, cor [hex]
  - Imagem: `staticFile("images/[arquivo]")` — tamanho [X]px
- **Animações**:
  - Título: fade in + slide up, frames 0→20
  - Subtítulo: fade in, delay 15 frames
  - Imagem: scale spring de 0→1, delay 10 frames
- **Entrada**: fade in (0→15 frames)
- **Saída**: fade out (últimos 15 frames)

### Cena 2: [NomeDaCena2]
- **Componente**: `Scene02[NomeDaCena2].tsx`
- **Frames**: [inicio] a [fim]
- **Descrição**: [O que acontece]
- **Copy na tela**: "[Texto exato]"
- **Componentes visuais**:
  - [listar]
- **Animações**:
  - [listar animação por componente]
- **Entrada**: [tipo de transição]
- **Saída**: [tipo de transição]

[... repetir para todas as cenas ...]

## Arquivo Principal (MainComposition.tsx)

Criar um arquivo `MainComposition.tsx` que:
1. Importe todas as cenas acima
2. Use `<Series>` para concatenar em ordem
3. Cada `<Series.Sequence>` com a duração exata em frames
4. Exporte a composition com o ID "[NomeDoVideo]"

## Instruções para o Claude Code

1. Criar cada arquivo de cena em `/src/scenes/`
2. Criar o componente principal em `/src/MainComposition.tsx`
3. Garantir que todos os assets referenciados existam em `/public`
4. Cada cena deve ter fade in na entrada e fade out na saída
5. Manter consistência de estilo (fontes, cores, espaçamento) entre todas as cenas
6. Usar `spring()` para animações de entrada (mais suave e natural)
7. Usar `interpolate()` para animações de opacidade e posição linear
8. Comentar o código em português explicando cada animação

## Primeira iteração

Após gerar a V1, revisar:
- [ ] Cena 1: verificar se o timing parece certo no Remotion Studio
- [ ] Cena 2: ajustar velocidade das animações se necessário
- [ ] [... uma checkbox por cena ...]
- [ ] Composição: verificar transições entre cenas
- [ ] Geral: verificar paleta de cores consistente
```

---

## Como o Dev Remotion deve preencher este template

1. Substituir todos os `[placeholders]` com valores reais da arquitetura de cenas
2. Detalhar cada cena ao máximo (quanto mais específico, melhor o resultado no Claude Code)
3. Listar TODOS os assets na seção de assets — o usuário precisa saber o que colocar em `/public`
4. Para cada componente visual, especificar: texto, tamanho, cor, posição, fonte
5. Para cada animação, especificar: frames de início/fim, valores de/para, tipo (spring/interpolate)
6. Incluir a checklist de iteração no final com uma linha por cena

O objetivo é que o usuário possa copiar este prompt literalmente para o Claude Code e obter um vídeo funcional sem precisar adicionar informações extras.
