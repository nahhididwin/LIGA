#!/usr/bin/env python3
# liga_demo.py
# Demo LIGA packing + mask-add rotation vs baseline vectorized update
# Requires: Python 3.8+, numpy

import time
import numpy as np
from typing import List, Tuple

# ---------------------------
# Layout / parameters (configurable)
# ---------------------------
W = 64               # bits per PFE (choose >= sum of fields)
phi_bits = 10        # width of phase field (phi)
rho_bits = 12        # width of radius field (rho)
state_bits = 6       # width for state
guard_bits = W - (phi_bits + rho_bits + state_bits)  # remaining bits as guard
o_phi = 0            # offset of phi inside PFE (LSB position) -> we'll put phi in LSB zone

MASK_phi = (1 << phi_bits) - 1

# Check guard-safety helper
def is_guard_safe(max_stack_additions: int) -> bool:
    # Condition (simplified): guard_bits > floor(log2(max_stack_additions))
    import math
    if max_stack_additions <= 0:
        return True
    return guard_bits > math.floor(math.log2(max_stack_additions))

# ---------------------------
# Pack / Unpack
# ---------------------------
def pack_frames(frames: List[Tuple[int,int,int]]) -> int:
    """
    frames: list of tuples (phi, rho, state) with widths as above
    returns big-int L which packs PFE_0 at least significant W bits, PFE_1 next, ...
    """
    L = 0
    for k, (phi, rho, state) in enumerate(frames):
        # clamp
        phi &= MASK_phi
        rho &= ((1 << rho_bits) - 1)
        state &= ((1 << state_bits) - 1)
        pfe = ( ( ( (state << (rho_bits + phi_bits)) |
                   (rho << phi_bits) ) |
                   phi ) )
        L |= (pfe << (k * W))
    return L

def unpack_frames(L: int, N: int) -> List[Tuple[int,int,int]]:
    frames = []
    mask_pfe = (1 << W) - 1
    for k in range(N):
        pfe = (L >> (k * W)) & mask_pfe
        phi = pfe & MASK_phi
        rho = (pfe >> phi_bits) & ((1 << rho_bits) - 1)
        state = (pfe >> (phi_bits + rho_bits)) & ((1 << state_bits) - 1)
        frames.append((phi, rho, state))
    return frames

# ---------------------------
# LIGA rotation via mask-add
# ---------------------------
def build_phase_mask(N: int, v: int) -> int:
    """Build M(v) = sum_k (v << (k*W + o_phi)). Precompute once."""
    v &= MASK_phi
    M = 0
    # efficient loop; still O(N) to build mask, but reused across iterations
    for k in range(N):
        M |= (v << (k * W + o_phi))
    return M

def apply_rotation_mask(L: int, M: int, total_bits: int) -> int:
    """Perform (L + M) mod 2^(total_bits). total_bits = N*W"""
    mod = 1 << total_bits
    return (L + M) % mod

# ---------------------------
# Baseline: per-frame vectorized update (numpy)
# ---------------------------
def baseline_vectorized(phi_array: np.ndarray, v: int) -> None:
    # phi_array is numpy array of dtype uint32 or similar
    phi_array[:] = (phi_array + np.uint32(v)) & np.uint32(MASK_phi)

# ---------------------------
# Micro-benchmark harness
# ---------------------------
def benchmark(N=2000, iterations=200, show_unpacked_check=False):
    print(f"\n--- LIGA demo: N={N}, W={W}, phi_bits={phi_bits}, iterations={iterations}")
    print(f"Guard bits = {guard_bits}. Guard-safe for stacking 1e6 additions? {is_guard_safe(10**6)}")

    # Random synthetic frames
    rng = np.random.default_rng(12345)
    phi_vals = rng.integers(low=0, high=(1<<phi_bits), size=N, dtype=np.uint32)
    rho_vals = rng.integers(low=0, high=(1<<rho_bits), size=N, dtype=np.uint32)
    state_vals = rng.integers(low=0, high=(1<<state_bits), size=N, dtype=np.uint32)
    frames = list(zip(map(int, phi_vals), map(int, rho_vals), map(int, state_vals)))

    # pack
    t0 = time.perf_counter()
    L = pack_frames(frames)
    t1 = time.perf_counter()
    build_M_v = 7  # chosen rotation delta
    M = build_phase_mask(N, build_M_v)
    t2 = time.perf_counter()
    pack_time = t1 - t0
    mask_build_time = t2 - t1
    print(f"pack time: {pack_time:.6f}s, build_mask time: {mask_build_time:.6f}s")

    # Warm up baseline arrays
    phi_array = phi_vals.copy()

    # Benchmark LIGA add (single big-int add per iteration)
    total_bits = N * W
    start = time.perf_counter()
    L2 = L
    for i in range(iterations):
        L2 = apply_rotation_mask(L2, M, total_bits)
    end = time.perf_counter()
    liga_time = end - start
    print(f"LIGA mask-add: total {iterations} iterations -> {liga_time:.6f}s ; avg {liga_time/iterations:.9f}s per add")

    # Benchmark baseline vectorized
    start = time.perf_counter()
    phi_copy = phi_array.copy()
    for i in range(iterations):
        baseline_vectorized(phi_copy, build_M_v)
    end = time.perf_counter()
    base_time = end - start
    print(f"Baseline vectorized (numpy) {iterations} iterations -> {base_time:.6f}s ; avg {base_time/iterations:.9f}s per step")

    # For fairness: include a pure Python loop baseline (per-frame loop) to show huge difference
    start = time.perf_counter()
    phi_py = list(map(int, phi_vals))
    for i in range(iterations):
        for j in range(N):
            phi_py[j] = (phi_py[j] + build_M_v) & MASK_phi
    end = time.perf_counter()
    py_loop_time = end - start
    print(f"Baseline pure-Python loop {iterations} iterations -> {py_loop_time:.6f}s ; avg {py_loop_time/iterations:.9f}s per step")

    # Optional: verify correctness (unpack L2 and compare phi fields to baseline result)
    if show_unpacked_check:
        unpacked = unpack_frames(L2, N)
        phi_unpacked = np.array([p for (p,_,_) in unpacked], dtype=np.uint32)
        # expected phi after iterations
        expected_phi = (phi_vals + iterations * np.uint32(build_M_v)) & np.uint32(MASK_phi)
        eq = np.all(phi_unpacked == expected_phi)
        print(f"Correctness check (LIGA vs expected): {eq}")
        if not eq:
            print("Example mismatch (first 10):")
            print("unpacked:", phi_unpacked[:10])
            print("expected:", expected_phi[:10])

if __name__ == "__main__":
    # Example runs with different sizes; uncomment the one you want:
    benchmark(N=2000, iterations=500, show_unpacked_check=True)
    # benchmark(N=10000, iterations=200, show_unpacked_check=False)
