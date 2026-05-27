from __future__ import annotations

import json
import subprocess
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

import imageio_ffmpeg
from faster_whisper import WhisperModel


VIDEO_EXTENSIONS = {
    ".mp4",
    ".mkv",
    ".mov",
    ".avi",
    ".webm",
    ".m4v",
    ".wmv",
    ".flv",
}


@dataclass(frozen=True)
class TranscriptSegment:
    start: float
    end: float
    text: str


@dataclass(frozen=True)
class TranscriptResult:
    text: str
    language: str | None
    duration: float | None
    segments: list[TranscriptSegment]
    output_dir: Path
    text_path: Path
    srt_path: Path
    json_path: Path


def list_video_files(base_dir: Path) -> list[Path]:
    ignored_dirs = {"uploads", "transcricoes", ".venv", "__pycache__"}
    videos: list[Path] = []

    for path in base_dir.iterdir():
        if path.is_dir() and path.name in ignored_dirs:
            continue
        if path.is_file() and path.suffix.lower() in VIDEO_EXTENSIONS:
            videos.append(path)

    return sorted(videos, key=lambda item: item.name.lower())


def extract_audio(video_path: Path, audio_path: Path) -> None:
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    command = [
        ffmpeg,
        "-y",
        "-i",
        str(video_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "16000",
        "-c:a",
        "pcm_s16le",
        str(audio_path),
    ]

    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        detail = completed.stderr.strip() or completed.stdout.strip()
        raise RuntimeError(f"Falha ao extrair audio do video: {detail}")


def load_whisper_model(
    model_size: str,
    device: str = "cpu",
    compute_type: str = "int8",
) -> WhisperModel:
    return WhisperModel(model_size, device=device, compute_type=compute_type)


def transcribe_video(
    video_path: Path,
    output_root: Path,
    model: WhisperModel,
    language: str | None = "pt",
    beam_size: int = 5,
    vad_filter: bool = True,
) -> TranscriptResult:
    video_path = video_path.resolve()
    output_root.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = output_root / f"{video_path.stem}_{stamp}"
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_path = output_dir / "audio_16khz.wav"
    extract_audio(video_path, audio_path)

    segments_iter, info = model.transcribe(
        str(audio_path),
        language=language,
        beam_size=beam_size,
        vad_filter=vad_filter,
    )
    segments = [
        TranscriptSegment(start=segment.start, end=segment.end, text=segment.text.strip())
        for segment in segments_iter
    ]
    text = "\n".join(segment.text for segment in segments if segment.text).strip()

    text_path = output_dir / "transcricao.txt"
    srt_path = output_dir / "transcricao.srt"
    json_path = output_dir / "segmentos.json"

    text_path.write_text(text, encoding="utf-8")
    srt_path.write_text(to_srt(segments), encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "source": str(video_path),
                "language": getattr(info, "language", None),
                "language_probability": getattr(info, "language_probability", None),
                "duration": getattr(info, "duration", None),
                "segments": [asdict(segment) for segment in segments],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return TranscriptResult(
        text=text,
        language=getattr(info, "language", None),
        duration=getattr(info, "duration", None),
        segments=segments,
        output_dir=output_dir,
        text_path=text_path,
        srt_path=srt_path,
        json_path=json_path,
    )


def to_srt(segments: Iterable[TranscriptSegment]) -> str:
    blocks = []
    for index, segment in enumerate(segments, start=1):
        if not segment.text:
            continue
        blocks.append(
            "\n".join(
                [
                    str(index),
                    f"{format_timestamp(segment.start)} --> {format_timestamp(segment.end)}",
                    segment.text,
                ]
            )
        )

    return "\n\n".join(blocks).strip() + "\n"


def format_timestamp(seconds: float) -> str:
    milliseconds = int(round(seconds * 1000))
    hours, remainder = divmod(milliseconds, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{millis:03}"
