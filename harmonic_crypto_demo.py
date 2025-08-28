#!/usr/bin/env python3
import numpy as np, json, math, argparse

PHI   = (1 + np.sqrt(5)) / 2
PSI   = 1.324718
OMEGA = 0.5671432904097838
XI    = np.e
LAMB  = np.pi
ZETA3 = 1.2020569031595942

def fractional(x: float)->float:
    return x - math.floor(x)

def derive_freqs(exps, band_low, band_high, carriers, seed):
    a,b,c,d,e,f = exps
    rng = np.random.default_rng(seed)
    v = np.array([np.log(PHI), np.log(PSI), np.log(OMEGA), np.log(XI), np.log(LAMB), np.log(ZETA3)])
    n = np.array([a,b,c,d,e,f], dtype=float)
    freqs = []
    for k in range(carriers):
        m = rng.integers(1,10,size=6)
        mix = float(np.dot(m + n, v) * (k + 1))
        u = fractional(mix * (PHI + PSI))
        f = band_low + u * (band_high - band_low)
        eps = 0.01 * (band_high - band_low)
        f = min(max(f, band_low + eps), band_high - eps)
        freqs.append(f)
    return np.array(sorted(freqs))

def make_chip_wave(carriers, chips_per_bit, seed, N):
    rng = np.random.default_rng(seed ^ 0xA5A5A5A5)
    pn = rng.integers(0,2,size=(carriers, chips_per_bit))*2 - 1
    samples_per_chip = N // chips_per_bit
    wave = np.repeat(pn, samples_per_chip, axis=1)
    if wave.shape[1] < N:
        pad_cols = N - wave.shape[1]
        pad = np.repeat(wave[:, -1:], pad_cols, axis=1)
        wave = np.concatenate([wave, pad], axis=1)
    elif wave.shape[1] > N:
        wave = wave[:, :N]
    return wave.astype(float)

def awgn(x, snr_db, rng):
    p_signal = np.mean(x**2) + 1e-18
    p_noise = p_signal / (10**(snr_db/10.0))
    return x + rng.normal(0, np.sqrt(p_noise), size=x.shape)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--fs', type=float, default=200000.0)
    ap.add_argument('--tb', type=float, default=0.01)
    ap.add_argument('--nbits', type=int, default=128)
    ap.add_argument('--snr_db', type=float, default=6.0)
    ap.add_argument('--band_low', type=float, default=5000.0)
    ap.add_argument('--band_high', type=float, default=45000.0)
    ap.add_argument('--carriers', type=int, default=32)
    ap.add_argument('--chips_per_bit', type=int, default=64)
    ap.add_argument('--seed_true', type=int, default=20250821)
    ap.add_argument('--seed_wrong', type=int, default=20250822)
    ap.add_argument('--exps_true', type=str, default='4,3,3,1,3,2')
    ap.add_argument('--exps_wrong', type=str, default='4,3,3,1,2,2')
    args = ap.parse_args()

    rng = np.random.default_rng(137)

    fs, tb = args.fs, args.tb
    N = int(round(fs*tb))
    t = np.arange(N)/fs

    exps_true  = tuple(int(x) for x in args.exps_true.split(','))
    exps_wrong = tuple(int(x) for x in args.exps_wrong.split(','))

    freqs_true = derive_freqs(exps_true, args.band_low, args.band_high, args.carriers, args.seed_true)
    phases_true = np.random.default_rng(args.seed_true ^ 0x5A5A5A5A).random(args.carriers) * 2*np.pi
    basis = np.cos(2*np.pi*freqs_true[:,None]*t + phases_true[:,None])
    basis = basis / (np.linalg.norm(basis, axis=1, keepdims=True) + 1e-12)

    freqs_wrong = derive_freqs(exps_wrong, args.band_low, args.band_high, args.carriers, args.seed_wrong)
    phases_wrong = np.random.default_rng(args.seed_wrong ^ 0x5A5A5A5A).random(args.carriers) * 2*np.pi
    basis_w = np.cos(2*np.pi*freqs_wrong[:,None]*t + phases_wrong[:,None])
    basis_w = basis_w / (np.linalg.norm(basis_w, axis=1, keepdims=True) + 1e-12)

    bits = rng.integers(0,2,size=args.nbits).astype(int)
    symbols = 2*bits - 1

    frames = []
    for i, s in enumerate(symbols):
        chips_true = make_chip_wave(args.carriers, args.chips_per_bit, args.seed_true + i*7919, N)
        frame = np.sum(basis * chips_true, axis=0)
        frames.append(s * frame)
    x = np.concatenate(frames)
    x = awgn(x, args.snr_db, rng)

    # Correct reception
    y = np.zeros(args.nbits, dtype=int)
    for i in range(args.nbits):
        seg = x[i*N:(i+1)*N]
        chips_true = make_chip_wave(args.carriers, args.chips_per_bit, args.seed_true + i*7919, N)
        corr = np.dot(basis * chips_true, seg)
        score = np.sum(corr)
        y[i] = 1 if score >= 0 else 0
    ber_correct = float(np.mean(y != bits))

    # Wrong reception
    y2 = np.zeros(args.nbits, dtype=int)
    for i in range(args.nbits):
        seg = x[i*N:(i+1)*N]
        chips_wrong = make_chip_wave(args.carriers, args.chips_per_bit, args.seed_wrong + i*7919, N)
        corr = np.dot(basis_w * chips_wrong, seg)
        score = np.sum(corr)
        y2[i] = 1 if score >= 0 else 0
    ber_wrong = float(np.mean(y2 != bits))

    print(json.dumps({
        "nbits": int(args.nbits),
        "carriers": int(args.carriers),
        "chips_per_bit": int(args.chips_per_bit),
        "snr_db": float(args.snr_db),
        "ber_correct": ber_correct,
        "ber_wrong": ber_wrong
    }, indent=2))

if __name__ == "__main__":
    main()
