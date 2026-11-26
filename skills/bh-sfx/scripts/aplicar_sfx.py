"""Mistura efeitos sonoros por cima do áudio de um vídeo, seguindo uma lista de marcações.

Arquivo de marcações (JSON):
    {"marcacoes": [
        {"t": 0.00, "som": "riser", "volume": 0.5},
        {"t": 1.84, "som": "whoosh", "volume": 0.7, "motivo": "corte para o close"}
    ]}

  t       segundo em que o som começa (para o riser, o pico fica no fim do som:
          use "alinhar": "fim" para o som terminar exatamente em t)
  som     nome do efeito: sons/<som>.wav, sons/<som>.mp3, uma pasta sons/<som>/
          (a skill alterna entre os arquivos dela para não repetir o mesmo) ou um
          arquivo dentro de uma pasta de categoria (sons/gancho-impacto-viral/<som>.wav)
  volume  0 a 1 em relação ao volume original do arquivo (padrão 0.6)

Gera dois arquivos ao lado do vídeo (ou em --saida):
  <video>_sfx.mp4        vídeo com a fala e os efeitos já misturados
  <video>_sfx_faixa.wav  só os efeitos, do segundo 0 até o fim do vídeo, para
                         soltar como uma faixa no CapCut, Premiere ou DaVinci

Uso:
    python aplicar_sfx.py video.mp4 marcacoes.json
"""
import argparse
import itertools
import json
import subprocess
import sys
from pathlib import Path

PASTA_SONS = Path(__file__).resolve().parent.parent / "sons"
EXTENSOES = (".wav", ".mp3", ".m4a", ".aif", ".aiff", ".ogg", ".flac")


def resolver_sons(pasta):
    """Mapeia nome do efeito -> ciclo de arquivos, nesta ordem de prioridade:

    1. Nome de pasta: sons/woosh/ com várias versões responde por "woosh" e
       alterna entre elas, para o vídeo não repetir o mesmo som.
    2. Arquivo dentro de uma pasta de categoria: sons/efeitos-sonoros-diversos/
       riser.wav responde por "riser".
    3. Arquivo solto em sons/: sintetizado, só vale quando nada acima tem o
       mesmo nome. O som real das referências sempre ganha do sintetizado.
    """
    sons = {}
    pastas = []
    for item in sorted(pasta.iterdir()):
        if item.is_dir():
            arquivos = sorted(f for f in item.iterdir() if f.suffix.lower() in EXTENSOES)
            if arquivos:
                sons[item.name.lower()] = itertools.cycle(arquivos)
                pastas.append(arquivos)
    for arquivos in pastas:
        for f in arquivos:
            sons.setdefault(f.stem.lower(), itertools.cycle([f]))
    for item in sorted(pasta.iterdir()):
        if item.is_file() and item.suffix.lower() in EXTENSOES:
            sons.setdefault(item.stem.lower(), itertools.cycle([item]))
    return sons


def duracao(arquivo):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                        "-of", "default=nw=1:nk=1", str(arquivo)], capture_output=True, text=True)
    return float(r.stdout.strip())


def tem_audio(video):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
                        "stream=index", "-of", "csv=p=0", str(video)], capture_output=True, text=True)
    return bool(r.stdout.strip())


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video", type=Path)
    p.add_argument("marcacoes", type=Path)
    p.add_argument("--sons", type=Path, default=PASTA_SONS)
    p.add_argument("--saida", type=Path, help="pasta de saída (padrão: a do vídeo)")
    p.add_argument("--volume-geral", type=float, default=1.0, help="multiplica o volume de todos os efeitos")
    args = p.parse_args()

    marcacoes = json.loads(args.marcacoes.read_text(encoding="utf-8"))["marcacoes"]
    sons = resolver_sons(args.sons)
    dur_video = duracao(args.video)
    saida = args.saida or args.video.parent
    saida.mkdir(parents=True, exist_ok=True)
    video_out = saida / f"{args.video.stem}_sfx.mp4"
    faixa_out = saida / f"{args.video.stem}_sfx_faixa.wav"

    entradas, filtros, rotulos = ["-i", str(args.video)], [], []
    for m in sorted(marcacoes, key=lambda m: m["t"]):
        nome = m["som"].lower()
        if nome not in sons:
            sys.exit(f"efeito '{m['som']}' não existe em {args.sons}. Disponíveis: {', '.join(sorted(sons))}")
        arquivo = next(sons[nome])
        dur_som = duracao(arquivo)
        inicio = m["t"] - dur_som if m.get("alinhar") == "fim" else m["t"]
        if inicio + dur_som <= 0.01 or inicio >= dur_video:
            print(f"aviso: '{m['som']}' em t={m['t']} cai fora do vídeo e foi ignorado", file=sys.stderr)
            continue
        corte_ini = max(0.0, -inicio)  # som que começaria antes do 0 é aparado
        atraso_ms = int(max(0.0, inicio) * 1000)
        vol = m.get("volume", 0.6) * args.volume_geral
        entradas += ["-i", str(arquivo)]
        n = len(rotulos) + 1  # índice da entrada no ffmpeg (0 é o vídeo)
        filtros.append(f"[{n}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                       f"atrim=start={corte_ini:.3f},asetpts=PTS-STARTPTS,"
                       f"volume={vol:.3f},adelay={atraso_ms}:all=1[s{n}]")
        rotulos.append(f"[s{n}]")
    if not rotulos:
        sys.exit("nenhuma marcação cai dentro do vídeo")

    filtros.append(f"{''.join(rotulos)}amix=inputs={len(rotulos)}:normalize=0:duration=longest,"
                   f"apad,atrim=end={dur_video:.3f}[sfx]")
    filtros.append("[sfx]asplit=2[sfx_mix][sfx_faixa]")
    if tem_audio(args.video):
        filtros.append("[0:a]aformat=sample_rates=48000:channel_layouts=stereo[voz]")
        filtros.append("[voz][sfx_mix]amix=inputs=2:normalize=0:duration=first,"
                       "alimiter=limit=0.95:level=disabled[mix]")
    else:
        filtros.append("[sfx_mix]anull[mix]")

    cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *entradas,
           "-filter_complex", ";".join(filtros),
           "-map", "0:v", "-map", "[mix]", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
           "-movflags", "+faststart", str(video_out),
           "-map", "[sfx_faixa]", "-c:a", "pcm_s16le", str(faixa_out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"ffmpeg falhou:\n{r.stderr}")
    print(video_out)
    print(faixa_out)


if __name__ == "__main__":
    main()
