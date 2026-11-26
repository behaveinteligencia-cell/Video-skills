# Remotion Video Squad

Squad multi-agente que transforma qualquer ideia em um vídeo animado completo com Remotion — do briefing ao código TSX pronto para rodar.

## O que este plugin faz

A partir de um simples prompt ("quero um vídeo sobre X"), o squad executa três agentes em sequência:

1. **Roteirista** — transforma a ideia em roteiro narrativo com cenas definidas
2. **Arquiteto de Cenas** — converte o roteiro em arquitetura técnica Remotion (componentes, animações, timings, assets)
3. **Dev Remotion** — gera o código TSX completo de cada cena + composição principal + prompt estruturado para Claude Code

## Outputs gerados

Ao final, você recebe uma pasta com:

- `roteiro.md` — Roteiro narrativo com descrição de cada cena
- `arquitetura-cenas.md` — Especificação técnica de componentes e animações
- `src/` — Código TSX de cada cena + arquivo de composição principal
- `prompt-remotion-final.md` — Prompt completo e estruturado para usar com Claude Code + Remotion Skills
- `assets-checklist.md` — Lista de todos os assets necessários na pasta `/public`
- `COMO-USAR.md` — Passo a passo para rodar o projeto no Remotion Studio

## Skills

| Skill | Trigger |
|-------|---------|
| `remotion-video` | "criar vídeo remotion", "gerar animação remotion", "squad remotion", "fazer vídeo com remotion" |

## Agentes

| Agente | Função |
|--------|--------|
| `roteirista` | Escreve o roteiro narrativo do vídeo em cenas |
| `arquiteto-cenas` | Projeta a arquitetura técnica Remotion de cada cena |
| `dev-remotion` | Gera o código TSX completo e o prompt final |

## Pré-requisitos para rodar o vídeo

Após usar o squad, você precisará de:

- **Claude Code** (versão paga)
- **Remotion Skills** instalado: `npx skills add remotion-dev/skills`
- **Node.js** instalado na máquina

## Como usar

1. Diga: *"criar vídeo remotion sobre [sua ideia]"*
2. Responda as perguntas do squad (tema, duração, estilo, assets)
3. O squad gera todos os arquivos automaticamente
4. Copie a pasta `src/` para um projeto Remotion
5. Cole o `prompt-remotion-final.md` no Claude Code para gerar/refinar o vídeo
6. Visualize no Remotion Studio (localhost)
7. Itere cena por cena até ficar perfeito
