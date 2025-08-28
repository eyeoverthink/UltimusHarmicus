#!/usr/bin/env python3
"""
End-to-end helper orchestrator (non-core):
- Runs tools/reproduce_alpha_minimal.py
- Runs tools/verify_appendix_A_derivation.py
- Runs tools/run_suite_validate_alpha.py
- Runs tools/sensitivity_alpha_analysis.py
- Runs tools/monte_carlo_alpha_robustness.py
- Runs tools/independent_backend_alpha_check.py
- Runs tools/crypto_artifact_chain_verify.py
- Verifies that expected artifacts exist and success==true
- Emits:
  * concise E2E JSON result
  * consolidated master report with pointers to all artifacts
  * consolidated index (plus reuse of QR images from sub-steps)
"""
import json
import subprocess
import sys
import os
from datetime import datetime, timezone
from pathlib import Path

# Non-core signer utility
from artifact_signer import sign_file

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"

ALPHA_TXT = ROOT / "alpha_reproduction.txt"
APPENDIX_JSON = ROOT / "appendix_A_exponent_derivation_proof.json"
SUITE_INDEX = ROOT / "scientific_suite_alpha_index.json"
SENS_PATTERN = "sensitivity_alpha_analysis_"
MC_PATTERN = "monte_carlo_alpha_robustness_"
DEC_PATTERN = "independent_backend_alpha_check_"
CRYPTO_PATTERN = "crypto_artifact_chain_verify_"
COH_PATTERN = "coherence_monitor_result_"
ISS_WRAP_PATTERN = "iss_validation_wrapper_result_"
MD_WRAP_PATTERN = "multidim_teleportation_wrapper_result_"
CHSH_PATTERN = "entanglement_chsh_result_"
RECURSIVE_PATTERN = "recursive_improvement_result_"


def run(cmd, cwd: Path):
    res = subprocess.run(cmd, cwd=str(cwd), capture_output=True, text=True)
    return res.returncode, res.stdout, res.stderr


def main():
    steps = []

    # 1) Minimal alpha reproduction
    rc, out, err = run([sys.executable, str(TOOLS / "reproduce_alpha_minimal.py")], ROOT)
    steps.append({
        "step": "reproduce_alpha_minimal",
        "rc": rc,
        "stdout": out[-2000:],
        "stderr": err[-2000:]
    })

    # 2) Appendix A derivation verification
    rc2, out2, err2 = run([sys.executable, str(TOOLS / "verify_appendix_A_derivation.py")], ROOT)
    steps.append({
        "step": "verify_appendix_A_derivation",
        "rc": rc2,
        "stdout": out2[-2000:],
        "stderr": err2[-2000:]
    })

    # 3) Suite validation runner (produces index/report + QRs)
    rc3, out3, err3 = run([sys.executable, str(TOOLS / "run_suite_validate_alpha.py")], ROOT)
    steps.append({
        "step": "run_suite_validate_alpha",
        "rc": rc3,
        "stdout": out3[-4000:],
        "stderr": err3[-2000:]
    })

    # 4) Sensitivity analysis
    rc4, out4, err4 = run([sys.executable, str(TOOLS / "sensitivity_alpha_analysis.py")], ROOT)
    steps.append({
        "step": "sensitivity_alpha_analysis",
        "rc": rc4,
        "stdout": out4[-2000:],
        "stderr": err4[-2000:]
    })

    # 5) Monte Carlo robustness
    rc5, out5, err5 = run([sys.executable, str(TOOLS / "monte_carlo_alpha_robustness.py")], ROOT)
    steps.append({
        "step": "monte_carlo_alpha_robustness",
        "rc": rc5,
        "stdout": out5[-2000:],
        "stderr": err5[-2000:]
    })

    # 6) Independent backend (Decimal)
    rc6, out6, err6 = run([sys.executable, str(TOOLS / "independent_backend_alpha_check.py")], ROOT)
    steps.append({
        "step": "independent_backend_alpha_check",
        "rc": rc6,
        "stdout": out6[-2000:],
        "stderr": err6[-2000:]
    })

    # 7) Crypto artifact chain verify
    rc7, out7, err7 = run([sys.executable, str(TOOLS / "crypto_artifact_chain_verify.py")], ROOT)
    steps.append({
        "step": "crypto_artifact_chain_verify",
        "rc": rc7,
        "stdout": out7[-2000:],
        "stderr": err7[-2000:]
    })

    # 8) Quantum coherence monitor wrapper
    rc8, out8, err8 = run([sys.executable, str(TOOLS / "wrap_quantum_coherence_monitor.py")], ROOT)
    steps.append({
        "step": "wrap_quantum_coherence_monitor",
        "rc": rc8,
        "stdout": out8[-2000:],
        "stderr": err8[-2000:]
    })

    # 9) ISS atom teleportation validation wrapper
    rc9, out9, err9 = run([sys.executable, str(TOOLS / "wrap_iss_atom_validation.py")], ROOT)
    steps.append({
        "step": "wrap_iss_atom_validation",
        "rc": rc9,
        "stdout": out9[-2000:],
        "stderr": err9[-2000:]
    })

    # 10) Multidimensional teleportation experiment wrapper
    rc10, out10, err10 = run([sys.executable, str(TOOLS / "wrap_multidimensional_teleportation.py")], ROOT)
    steps.append({
        "step": "wrap_multidimensional_teleportation",
        "rc": rc10,
        "stdout": out10[-2000:],
        "stderr": err10[-2000:]
    })

    # 11) CHSH φ-bridge entanglement witness
    rc11, out11, err11 = run([sys.executable, str(TOOLS / "entanglement_chsh_phi_bridge.py")], ROOT)
    steps.append({
        "step": "entanglement_chsh_phi_bridge",
        "rc": rc11,
        "stdout": out11[-2000:],
        "stderr": err11[-2000:]
    })

    # 12) Recursive improvement system wrapper
    rc12, out12, err12 = run([sys.executable, str(TOOLS / "wrap_recursive_improvement_system.py")], ROOT)
    steps.append({
        "step": "wrap_recursive_improvement_system",
        "rc": rc12,
        "stdout": out12[-2000:],
        "stderr": err12[-2000:]
    })

    # Collect artifacts
    artifacts = {
        "alpha_reproduction_txt_exists": ALPHA_TXT.exists(),
        "appendix_A_json_exists": APPENDIX_JSON.exists(),
        "suite_index_exists": SUITE_INDEX.exists(),
    }

    report_path = None
    suite_qrs = {}
    suite_success = None
    phi_improved = None
    sens_file = None
    mc_file = None
    dec_file = None
    crypto_file = None

    if SUITE_INDEX.exists():
        try:
            idx = json.loads(SUITE_INDEX.read_text(encoding="utf-8"))
            report_path = ROOT / idx.get("report", "")
            suite_qrs = idx.get("qr", {})
            if report_path and report_path.exists():
                rep = json.loads(report_path.read_text(encoding="utf-8"))
                suite_success = bool(rep.get("success"))
                phi_improved = bool(rep.get("phi_enhancement"))
        except Exception as e:
            steps.append({"step": "parse_index_error", "error": str(e)})

    # Find latest generated files for sensitivity/MC/Decimal/Crypto reports
    def latest_with_prefix(prefix: str):
        candidates = sorted(ROOT.glob(f"{prefix}*.json"))
        return str(candidates[-1]) if candidates else None

    sens_file = latest_with_prefix(SENS_PATTERN)
    mc_file = latest_with_prefix(MC_PATTERN)
    dec_file = latest_with_prefix(DEC_PATTERN)
    crypto_file = latest_with_prefix(CRYPTO_PATTERN)
    coh_file = latest_with_prefix(COH_PATTERN)
    iss_wrap_file = latest_with_prefix(ISS_WRAP_PATTERN)
    md_wrap_file = latest_with_prefix(MD_WRAP_PATTERN)
    chsh_file = latest_with_prefix(CHSH_PATTERN)
    recursive_file = latest_with_prefix(RECURSIVE_PATTERN)

    overall_ok = (
        steps[0]["rc"] == 0
        and steps[1]["rc"] == 0
        and steps[2]["rc"] == 0
        and steps[3]["rc"] == 0
        and steps[4]["rc"] == 0
        and steps[5]["rc"] == 0
        and steps[6]["rc"] == 0
        and steps[7]["rc"] == 0
        and steps[8]["rc"] == 0
        and steps[9]["rc"] == 0
        and steps[10]["rc"] == 0
        and steps[11]["rc"] == 0
        and artifacts["alpha_reproduction_txt_exists"]
        and artifacts["appendix_A_json_exists"]
        and artifacts["suite_index_exists"]
        and suite_success is True
    )

    result = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "overall_success": overall_ok,
        "phi_enhancement": phi_improved,
        "report_path": str(report_path) if report_path else None,
        "suite_qrs": suite_qrs,
        "artifacts": artifacts,
        "steps": steps,
        "additional_reports": {
            "sensitivity": sens_file,
            "monte_carlo": mc_file,
            "independent_backend": dec_file,
            "crypto_chain_verify": crypto_file,
            "coherence_monitor": coh_file,
            "iss_validation_wrapper": iss_wrap_file,
            "multidimensional_teleportation_wrapper": md_wrap_file,
            "entanglement_chsh_phi_bridge": chsh_file,
            "recursive_improvement_wrapper": recursive_file,
        }
    }

    ts = int(datetime.now(timezone.utc).timestamp())
    out_file = ROOT / f"scientific_validation_e2e_result_{ts}.json"
    master_report = ROOT / f"scientific_validation_master_report_{ts}.json"
    master_index = ROOT / f"scientific_validation_master_index.json"

    out_file.write_text(json.dumps(result, indent=2), encoding="utf-8")
    # Sign E2E result JSON
    try:
        sign_file(out_file)
    except Exception:
        pass

    # Build consolidated master report and index
    master = {
        "timestamp": result["timestamp"],
        "overall_success": overall_ok,
        "suite_report": result["report_path"],
        "suite_qrs": suite_qrs,
        "sensitivity_report": sens_file,
        "monte_carlo_report": mc_file,
        "independent_backend_report": dec_file,
        "crypto_chain_verify_report": crypto_file,
        "coherence_monitor_report": coh_file,
        "iss_validation_wrapper_report": iss_wrap_file,
        "multidimensional_teleportation_wrapper_report": md_wrap_file,
        "entanglement_chsh_phi_bridge_report": chsh_file,
        "recursive_improvement_wrapper_report": recursive_file,
        "e2e_result": str(out_file),
    }
    master_report.write_text(json.dumps(master, indent=2), encoding="utf-8")
    try:
        sign_file(master_report)
    except Exception:
        pass

    index = {
        "suite_index": str(SUITE_INDEX),
        "master_report": str(master_report),
        "e2e_result": str(out_file),
        "qrs": suite_qrs,
    }
    master_index.write_text(json.dumps(index, indent=2), encoding="utf-8")
    try:
        sign_file(master_index)
    except Exception:
        pass

    print("E2E Validation Summary:")
    print(f"- Overall Success: {overall_ok}")
    print(f"- Report: {report_path}")
    print(f"- Suite Index: {SUITE_INDEX}")
    if suite_qrs:
        for k, v in suite_qrs.items():
            print(f"- {k}: {v}")
    print(f"- E2E Result JSON: {out_file}")
    print(f"- Master Report: {master_report}")
    print(f"- Master Index: {master_index}")


if __name__ == "__main__":
    main()
