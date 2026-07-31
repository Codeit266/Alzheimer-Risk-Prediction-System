import re

def parse_cha_file(file_path):
    text_segments = []
    total_duration_ms = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            if line.startswith("*PAR:"):
                cleaned = line.replace("*PAR:", "").strip()
                # Find timestamps enclosed in \x15 (e.g. \x155360_6950\x15)
                match = re.search(r'\x15(\d+)_(\d+)\x15', cleaned)
                if match:
                    start = int(match.group(1))
                    end = int(match.group(2))
                    total_duration_ms += (end - start)
                    cleaned = re.sub(r'\s*\x15\d+_\d+\x15\s*$', '', cleaned)

                # Clean transcription tags
                cleaned = re.sub(r'\[\+\s+\w+\]', '', cleaned)
                cleaned = re.sub(r'\[\/\/\]', '', cleaned)
                cleaned = re.sub(r'&\+\w+', '', cleaned)
                cleaned = re.sub(r'<([^>]+)>', r'\1', cleaned)
                cleaned = re.sub(r'\((\w+)\)', r'\1', cleaned)

                text_segments.append(cleaned.strip())

    combined_text = " ".join(text_segments)
    combined_text = re.sub(r'\s+', ' ', combined_text).strip()

    duration_sec = total_duration_ms / 1000.0
    return combined_text, duration_sec


def extract_participant_text(file_path):
    text, _ = parse_cha_file(file_path)
    return text