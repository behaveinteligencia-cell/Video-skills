"""Gera a biblioteca base de efeitos sonoros da skill bh-sfx.

Os sons são sintetizados do zero (sem direitos autorais de terceiros) e servem
de ponto de partida. Para trocar por sons melhores, coloque arquivos .wav/.mp3
na pasta sons/ com o mesmo nome, ou numa subpasta com o nome do efeito
(sons/whoosh/qualquer-nome.wav) para a skill alternar entre eles.

Uso:
    python gerar_sons_base.py            # grava em ../sons
    python gerar_sons_base.py --saida pasta
"""
import argparse
import wave
from pathlib import Path

import numpy as np

SR = 48000
rng = np.random.default_rng(7)


def t(dur):
    return np.arange(int(SR * dur)) / SR


def lowpass_variavel(x, cortes_hz):
    """Passa-baixa de um polo com frequência de corte que muda a cada amostra."""
    a = np.exp(-2 * np.pi * np.asarray(cortes_hz) / SR)
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc = (1 - a[i]) * x[i] + a[i] * acc
        y[i] = acc
    return y


def envelope(n, ataque, queda):
    env = np.ones(n)
    na, nq = int(n * ataque), int(n * queda)
    if na:
        env[:na] = np.linspace(0, 1, na) ** 2
    if nq:
        env[-nq:] = np.linspace(1, 0, nq) ** 2
    return env


def whoosh(dur=0.45):
    n = int(SR * dur)
    ruido = rng.standard_normal(n)
    sweep = np.concatenate([np.geomspace(300, 6000, n // 2), np.geomspace(6000, 400, n - n // 2)])
    som = lowpass_variavel(ruido, sweep) - lowpass_variavel(ruido, sweep * 0.25)
    return som * envelope(n, 0.5, 0.5)


def pop(dur=0.09):
    x = t(dur)
    freq = np.geomspace(900, 180, len(x))
    fase = 2 * np.pi * np.cumsum(freq) / SR
    return np.sin(fase) * np.exp(-x * 45)


def ding(dur=1.4):
    x = t(dur)
    base = 1318.5  # Mi6
    som = (np.sin(2 * np.pi * base * x)
           + 0.4 * np.sin(2 * np.pi * base * 2.01 * x) * np.exp(-x * 3)
           + 0.2 * np.sin(2 * np.pi * base * 3.02 * x) * np.exp(-x * 6))
    ataque = np.minimum(x / 0.003, 1)
    return som * np.exp(-x * 3.2) * ataque


def boom(dur=1.6):
    x = t(dur)
    freq = np.geomspace(110, 38, len(x))
    fase = 2 * np.pi * np.cumsum(freq) / SR
    grave = np.tanh(2.2 * np.sin(fase)) * np.exp(-x * 2.4)
    estalo = rng.standard_normal(len(x)) * np.exp(-x * 120) * 0.5
    return grave + estalo


def click(dur=0.025):
    x = t(dur)
    ruido = rng.standard_normal(len(x))
    ruido = ruido - lowpass_variavel(ruido, np.full(len(x), 2500.0))
    return ruido * np.exp(-x * 300)


def riser(dur=2.2):
    n = int(SR * dur)
    x = t(dur)
    freq = np.geomspace(180, 2400, n)
    tom = np.sin(2 * np.pi * np.cumsum(freq) / SR) * 0.35
    ruido = lowpass_variavel(rng.standard_normal(n), np.geomspace(500, 9000, n)) * 0.9
    env = (x / dur) ** 2.5
    env[-int(SR * 0.02):] *= np.linspace(1, 0, int(SR * 0.02))
    return (tom + ruido) * env


def tom(freq, dur, queda, forma="seno"):
    x = t(dur)
    fase = 2 * np.pi * freq * x
    onda = np.sin(fase) if forma == "seno" else np.sign(np.sin(fase)) * 0.6
    return onda * np.exp(-x * queda) * np.minimum(x / 0.003, 1)


def juntar(*partes):
    """partes: (inicio_s, sinal). Soma tudo numa linha do tempo."""
    fim = max(int(SR * ini) + len(sig) for ini, sig in partes)
    out = np.zeros(fim)
    for ini, sig in partes:
        i = int(SR * ini)
        out[i:i + len(sig)] += sig
    return out


def camera():
    def estalo(dur, corte):
        n = int(SR * dur)
        r = rng.standard_normal(n)
        r = r - lowpass_variavel(r, np.full(n, corte))
        return r * np.exp(-t(dur) * 90)
    clunk = tom(180, 0.06, 60) * 0.6
    return juntar((0, estalo(0.05, 1800)), (0.004, clunk), (0.09, estalo(0.06, 1200) * 0.8))


def counter(dur=0.9, passo=0.055):
    partes, n = [], int(dur / passo)
    for k in range(n):
        partes.append((k * passo, tom(1400 + 900 * k / n, 0.03, 120) * 0.8))
    return juntar(*partes)


def glitch(dur=0.5):
    n, out, i = int(SR * dur), [], 0
    while i < n:
        bloco = int(SR * rng.uniform(0.015, 0.06))
        tipo = rng.integers(3)
        x = t(bloco / SR)
        if tipo == 0:
            sig = np.sign(np.sin(2 * np.pi * rng.uniform(80, 900) * x)) * 0.7
        elif tipo == 1:
            sig = rng.standard_normal(bloco) * 0.5
        else:
            sig = np.zeros(bloco)
        out.append(np.tile(sig[: max(1, bloco // 3)], 3)[:bloco] if rng.random() < 0.4 else sig)
        i += bloco
    return np.concatenate(out)[:n]


def money():
    gaveta = rng.standard_normal(int(SR * 0.05)) * np.exp(-t(0.05) * 80) * 0.6
    sino = juntar((0, tom(2093, 1.0, 4)), (0, tom(2637, 1.0, 4) * 0.7), (0, tom(4186, 0.6, 8) * 0.3))
    moedas = juntar(*[(0.15 + k * 0.045, tom(rng.uniform(5000, 7500), 0.12, 40) * 0.25) for k in range(8)])
    return juntar((0, gaveta), (0.06, sino), (0, moedas))


def error():
    return juntar((0, tom(392, 0.16, 6, "quadrada")), (0.18, tom(277, 0.32, 5, "quadrada")))


def correct():
    return juntar((0, tom(880, 0.14, 10) + tom(1760, 0.14, 14) * 0.3),
                  (0.12, tom(1318.5, 0.7, 5) + tom(2637, 0.7, 8) * 0.3))


def punch(dur=0.3):
    x = t(dur)
    freq = np.geomspace(160, 50, len(x))
    grave = np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-x * 18)
    n = int(SR * 0.04)
    estalo = lowpass_variavel(rng.standard_normal(n), np.full(n, 3000.0)) * np.exp(-t(0.04) * 90) * 3
    return juntar((0, grave), (0, estalo))


def crack(dur=0.45):
    partes = []
    for ini in np.sort(rng.uniform(0, dur - 0.05, 7)):
        n = int(SR * rng.uniform(0.004, 0.012))
        r = rng.standard_normal(n)
        partes.append((ini, (r - lowpass_variavel(r, np.full(n, 1500.0))) * rng.uniform(0.5, 1)))
    return juntar(*partes)


def gravar(caminho, sinal, pico_db=-1.0):
    sinal = sinal / (np.max(np.abs(sinal)) + 1e-9) * 10 ** (pico_db / 20)
    pcm = (sinal * 32767).astype(np.int16)
    estereo = np.repeat(pcm[:, None], 2, axis=1)
    with wave.open(str(caminho), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(estereo.tobytes())


SONS = {"whoosh": whoosh, "pop": pop, "ding": ding, "boom": boom, "click": click, "riser": riser,
        "camera": camera, "counter": counter, "glitch": glitch, "money": money, "error": error,
        "correct": correct, "punch": punch, "crack": crack}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--saida", default=Path(__file__).resolve().parent.parent / "sons", type=Path)
    args = p.parse_args()
    args.saida.mkdir(parents=True, exist_ok=True)
    for nome, gerar in SONS.items():
        destino = args.saida / f"{nome}.wav"
        gravar(destino, gerar())
        print(destino)


if __name__ == "__main__":
    main()
