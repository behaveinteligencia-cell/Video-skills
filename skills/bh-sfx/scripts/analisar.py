"""Analisa um vídeo e devolve, em JSON, os momentos onde um efeito sonoro pode entrar.

Saída:
  duracao        duração em segundos
  tem_audio      se o vídeo tem trilha de áudio
  cortes         tempos (s) em que a imagem muda de cena
  pausas         silêncios na fala: [{inicio, fim}]
  palavras       fala com tempo de cada trecho: [{inicio, fim, texto}]
  folhas         (só com --folhas PASTA) imagens com quadros do vídeo e o tempo
                 de cada um, para ver gestos, textos e trocas de tela
  picos          (só com --picos) ataques fortes no áudio; serve para mapear
                 onde um vídeo de referência já usa efeito sonoro

Uso:
    python analisar.py video.mp4 > analise.json
    python analisar.py video.mp4 --transcricao legenda.srt
    python analisar.py video.mp4 --folhas quadros/
    python analisar.py referencia.mp4 --picos
"""
import argparse
import json
import math
import re
import subprocess
import sys

import numpy as np


def rodar(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")


def sondar(video):
    r = rodar(["ffprobe", "-v", "error", "-show_entries", "format=duration:stream=codec_type",
               "-of", "json", video])
    if r.returncode != 0:
        sys.exit(f"ffprobe falhou: {r.stderr.strip()}")
    info = json.loads(r.stdout)
    tipos = {s["codec_type"] for s in info.get("streams", [])}
    return float(info["format"]["duration"]), "audio" in tipos


def cortes(video, limiar):
    r = rodar(["ffmpeg", "-hide_banner", "-i", video, "-an", "-vf",
               f"select='gt(scene,{limiar})',showinfo", "-f", "null", "-"])
    return [round(float(m), 2) for m in re.findall(r"pts_time:([\d.]+)", r.stderr)]


def pausas(video, ruido_db, minimo):
    r = rodar(["ffmpeg", "-hide_banner", "-i", video, "-vn", "-af",
               f"silencedetect=noise={ruido_db}dB:d={minimo}", "-f", "null", "-"])
    inicios = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r.stderr)]
    fins = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r.stderr)]
    return [{"inicio": round(i, 2), "fim": round(f, 2)} for i, f in zip(inicios, fins)]


def ler_srt(caminho):
    def seg(ts):
        h, m, s = ts.replace(",", ".").split(":")
        return int(h) * 3600 + int(m) * 60 + float(s)

    texto = open(caminho, encoding="utf-8-sig").read()
    blocos = re.findall(r"(\d+:\d+:\d+[,.]\d+)\s*-->\s*(\d+:\d+:\d+[,.]\d+)\s*\n(.*?)(?:\n\s*\n|\Z)", texto, re.S)
    return [{"inicio": round(seg(a), 2), "fim": round(seg(b), 2), "texto": " ".join(t.split())}
            for a, b, t in blocos]


def transcrever(video, modelo):
    try:
        from faster_whisper import WhisperModel
    except ImportError:
        return None
    try:
        # device="cpu" fixo: no "auto", uma placa NVIDIA sem cuDNN derruba o processo sem passar pelo except
        segmentos, _ = WhisperModel(modelo, device="cpu", compute_type="int8").transcribe(
            video, language="pt", word_timestamps=True, vad_filter=True)
        segmentos = list(segmentos)
    except Exception as erro:  # modelo sem download, sem memória etc.
        print(f"transcrição falhou: {erro}", file=sys.stderr)
        return None
    return [{"inicio": round(w.start, 2), "fim": round(w.end, 2), "texto": w.word.strip()}
            for s in segmentos for w in (s.words or [])]


def folhas(video, duracao, pasta, por_segundo=2, colunas=8, linhas=4):
    """Monta folhas de quadros (8x4 = 16 s por folha a 2 quadros/s) com o tempo escrito em cada quadro."""
    from pathlib import Path
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    por_folha = colunas * linhas / por_segundo
    geradas = []
    for k in range(math.ceil(duracao / por_folha)):
        inicio = k * por_folha
        destino = pasta / f"folha_{k + 1:02d}.png"
        base = f"fps={por_segundo},scale=180:-1"
        # no Windows o ffmpeg não tem fontconfig: sem fontfile o drawtext falha e a folha sai sem o tempo
        fonte = "fontfile='C\\:/Windows/Fonts/arialbd.ttf':" if sys.platform == "win32" else ""
        rotulo = (f",drawtext={fonte}text='%{{pts\\:hms\\:{inicio}}}':x=4:y=4:fontsize=16:"
                  "fontcolor=yellow:box=1:boxcolor=black@0.7")
        mosaico = f",tile={colunas}x{linhas}"
        for filtro in (base + rotulo + mosaico, base + mosaico):  # sem fonte disponível, vai sem rótulo
            r = rodar(["ffmpeg", "-y", "-v", "error", "-ss", str(inicio), "-t", str(por_folha), "-i", video,
                       "-vf", filtro, "-frames:v", "1", str(destino)])
            if r.returncode == 0:
                break
        geradas.append({"arquivo": str(destino), "inicio": inicio, "passo": 1 / por_segundo, "colunas": colunas})
    return geradas


def picos(video, salto_db, intervalo):
    """Ataques súbitos de energia: o quadro atual fica salto_db acima da mediana do último 0,3 s."""
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "16000",
                        "-f", "s16le", "-"], capture_output=True)
    amostras = np.frombuffer(r.stdout, dtype=np.int16).astype(np.float32) / 32768
    quadro = 160  # 10 ms
    n = len(amostras) // quadro
    if n == 0:
        return []
    energia = 10 * np.log10(np.mean(amostras[:n * quadro].reshape(n, quadro) ** 2, axis=1) + 1e-10)
    achados, ultimo = [], -1e9
    for i in range(30, n):
        base = np.median(energia[i - 30:i])
        subida = energia[i] - base
        if subida > salto_db and energia[i] > -40 and (i - ultimo) * 0.01 >= intervalo:
            achados.append({"t": round(i * 0.01, 2), "subida_db": round(float(subida), 1)})
            ultimo = i
    return achados


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("video")
    p.add_argument("--limiar-corte", type=float, default=0.3, help="0 a 1; menor acha mais cortes (padrão 0.3)")
    p.add_argument("--transcricao", help="arquivo .srt com a fala (CapCut, Premiere, Worxpace...)")
    p.add_argument("--modelo-whisper", default="small")
    p.add_argument("--sem-transcricao", action="store_true", help="pula a transcrição")
    p.add_argument("--folhas", metavar="PASTA", help="gera folhas de quadros com o tempo marcado nessa pasta")
    p.add_argument("--picos", action="store_true", help="lista ataques fortes no áudio (análise de referência)")
    args = p.parse_args()

    duracao, tem_audio = sondar(args.video)
    saida = {"video": args.video, "duracao": round(duracao, 2), "tem_audio": tem_audio,
             "cortes": cortes(args.video, args.limiar_corte), "pausas": [], "palavras": None}
    if args.folhas:
        saida["folhas"] = folhas(args.video, duracao, args.folhas)
    if tem_audio:
        saida["pausas"] = pausas(args.video, -35, 0.35)
        if args.transcricao:
            saida["palavras"] = ler_srt(args.transcricao)
        elif not args.sem_transcricao:
            saida["palavras"] = transcrever(args.video, args.modelo_whisper)
        if saida["palavras"] is None:
            saida["aviso"] = ("sem transcrição: instale faster-whisper (e deixe ele baixar o modelo) "
                              "ou passe --transcricao legenda.srt")
        if args.picos:
            saida["picos"] = picos(args.video, 12, 0.25)
    json.dump(saida, sys.stdout, ensure_ascii=False, indent=2)
    print()


if __name__ == "__main__":
    main()
