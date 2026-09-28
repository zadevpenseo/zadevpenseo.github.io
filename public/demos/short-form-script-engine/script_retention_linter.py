#!/usr/bin/env python3
"""
Short-Form Video Script Retention Linter & Telemetry Engine
Author: Muhammad Khoiruzzadittaqwa (Zadit) - PT Prisma Digital Kreatif
Analyzes vertical video scripts against cognitive load limits and 60-second retention models.
"""

import sys
import json
import re
from typing import Dict, List, Any

# Banned dead-openers that kill first-3-second retention
DEAD_OPENERS = [
    r"halo\s+guys",
    r"kembali\s+lagi",
    r"balik\s+lagi",
    r"di\s+video\s+kali\s+ini",
    r"hari\s+ini\s+aku\s+mau",
    r"jangan\s+lupa\s+like",
    r"tonton\s+sampai\s+habis"
]

def analyze_script(script_text: str, target_seconds: int = 60, visual_cue_count_override: int = None) -> Dict[str, Any]:
    # Extract words
    clean_words = re.findall(r"\b[\w'-]+\b", script_text)
    word_count = len(clean_words)
    
    # Calculate WPM assuming target_seconds
    minutes = target_seconds / 60.0
    wpm = round(word_count / minutes, 1)
    
    # Pace Assessment (Optimal Indonesian conversational tempo: 130 - 155 WPM)
    if wpm < 115:
        pace_status = "DELIBERATE"
        pace_note = "Tempo artikulatif, ideal untuk visual b-roll intensif dengan ruang nafas audio."
    elif 115 <= wpm <= 155:
        pace_status = "OPTIMAL"
        pace_note = "Kecepatan ideal untuk bahasa Indonesia lisan dengan ruang jeda nafas, sound effect, dan transisi layar."
    elif 155 < wpm <= 170:
        pace_status = "ELEVATED"
        pace_note = "Tempo cepat. Talent wajib terlatih artikulasi tanpa jeda gagap."
    else:
        pace_status = "OVER_BUDGET"
        pace_note = "Melebihi batas toleransi kognitif 60 detik. Pangkas kata agar tidak terburu-buru."

    # Check dead openers
    first_sentence = script_text.split(".")[0] if "." in script_text else script_text[:80]
    dead_opener_found = False
    for pattern in DEAD_OPENERS:
        if re.search(pattern, first_sentence, re.IGNORECASE):
            dead_opener_found = True
            break
            
    # Check visual cues
    if visual_cue_count_override is not None:
        visual_cue_count = visual_cue_count_override
    else:
        visual_cues = re.findall(r"(?:visual|b-roll|cut|angle|screen|layar):", script_text, re.IGNORECASE)
        visual_cue_count = len(visual_cues)
        
    avg_cue_interval = round(target_seconds / max(1, visual_cue_count), 1) if visual_cue_count > 0 else target_seconds

    # Retention Score (0 - 100)
    score = 100
    deductions = []
    
    if dead_opener_found:
        score -= 30
        deductions.append("Dead opener detected in hook (-30 pts)")
    if pace_status == "OVER_BUDGET":
        score -= 25
        deductions.append("Word count over budget (>155 WPM) (-25 pts)")
        
    if visual_cue_count < 8:
        score -= 10
        deductions.append(f"Low visual cuts density ({visual_cue_count} detected) (-10 pts)")
        
    score = max(10, score)

    return {
        "target_seconds": target_seconds,
        "word_count": word_count,
        "wpm": wpm,
        "pace_status": pace_status,
        "pace_note": pace_note,
        "visual_cues_detected": visual_cue_count,
        "avg_visual_cut_interval_seconds": avg_cue_interval,
        "retention_score": score,
        "deductions": deductions
    }

def main():
    if len(sys.argv) > 1 and sys.argv[1].endswith(".json"):
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            data = json.load(f)
            for sc in data.get("scripts", []):
                spoken = " ".join([b["audio_spoken"] for b in sc.get("beats", [])])
                cuts = sc.get("visual_cuts_count", len(sc.get("beats", [])))
                res = analyze_script(spoken, sc.get("target_duration", 60), visual_cue_count_override=cuts)
                print(f"=== Script: {sc.get('title')} ===")
                print(json.dumps(res, indent=2, ensure_ascii=False))
                print()
    else:
        sample = ("90% video pendek gagal bukan karena visualnya buram, tapi karena scriptnya kelamaan basa-basi di 3 detik awal. "
                  "Begitu lo buka dengan kalimat yang klise, penonton langsung geser ke video lain. "
                  "Rahasianya ada di aturan 4 detik. Otak manusia butuh kejutan visual baru setiap 4 detik sebelum dopaminnya turun. "
                  "Bagi naskah lo jadi dua kolom: apa yang didengar talent, dan apa yang dilihat editor. "
                  "Jangan biarkan talent ngomong tanpa ada B-roll pendukung atau teks penegas di layar. "
                  "Dengan format ini, video 60 detik lo bukan cuma ditonton sampai tuntas, tapi memandu editor motong klip dengan presisi frame. "
                  "Simpan video ini buat acuan syuting lo besok!")
        res = analyze_script(sample, 60)
        print("=== Sample 60-Second Script Audit ===")
        print(json.dumps(res, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
