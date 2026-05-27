from __future__ import annotations

from pathlib import Path

import streamlit as st

from transcriber import list_video_files, load_whisper_model, transcribe_video


BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "transcricoes"


st.set_page_config(
    page_title="Extracao de texto de video",
    page_icon="video",
    layout="wide",
)

st.markdown(
    """
    <style>
    [data-testid="stSidebar"]::after {
        content: "Desenvolvido por Henrique Ortiz";
        position: fixed;
        left: 30px;
        bottom: 18px;
        z-index: 999999;
        color: #475467;
        font-size: 0.85rem;
        font-weight: 500;
        pointer-events: none;
    }

    @media (max-width: 640px) {
        [data-testid="stSidebar"]::after {
            left: 18px;
            bottom: 12px;
            font-size: 0.78rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_resource(show_spinner=False)
def cached_model(model_size: str, device: str, compute_type: str):
    return load_whisper_model(model_size, device=device, compute_type=compute_type)


def save_upload(uploaded_file) -> Path:
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = Path(uploaded_file.name).name
    destination = UPLOAD_DIR / safe_name

    with destination.open("wb") as file:
        file.write(uploaded_file.getbuffer())

    return destination


def format_duration(seconds: float | None) -> str:
    if seconds is None:
        return "-"
    minutes, secs = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    if hours:
        return f"{hours}h {minutes:02}min {secs:02}s"
    return f"{minutes}min {secs:02}s"


st.title("Extracao de texto de video")
st.caption("Selecione um video da pasta do projeto ou envie um arquivo novo.")

with st.sidebar:
    st.header("Configuracao")
    model_size = st.selectbox(
        "Modelo Whisper",
        ["tiny", "base", "small", "medium", "large-v3"],
        index=1,
        help="Modelos maiores tendem a acertar mais, mas demoram mais.",
    )
    language_choice = st.selectbox(
        "Idioma",
        ["pt", "auto", "en", "es", "fr"],
        index=0,
        help="Use auto para deteccao automatica.",
    )
    device = st.selectbox(
        "Dispositivo",
        ["cpu", "cuda"],
        index=0,
        help="Use cuda apenas se tiver GPU NVIDIA configurada.",
    )
    compute_type = st.selectbox(
        "Precisao",
        ["int8", "float16", "float32"],
        index=0,
        help="int8 costuma ser a melhor escolha para CPU.",
    )
    vad_filter = st.toggle("Filtrar silencio", value=True)

local_videos = list_video_files(BASE_DIR)
local_options = ["Enviar arquivo"] + [path.name for path in local_videos]

source = st.radio(
    "Origem do video",
    local_options,
    horizontal=True if len(local_options) <= 3 else False,
)

video_path: Path | None = None
uploaded_file = None

if source == "Enviar arquivo":
    uploaded_file = st.file_uploader(
        "Video",
        type=["mp4", "mkv", "mov", "avi", "webm", "m4v", "wmv", "flv"],
    )
    if uploaded_file is not None:
        video_path = save_upload(uploaded_file)
else:
    video_path = BASE_DIR / source

if video_path is not None:
    st.info(f"Arquivo selecionado: {video_path.name}")

transcribe = st.button("Transcrever", type="primary", disabled=video_path is None)

if transcribe and video_path is not None:
    language = None if language_choice == "auto" else language_choice

    try:
        with st.status("Carregando modelo Whisper...", expanded=True) as status:
            model = cached_model(model_size, device, compute_type)
            status.update(label="Extraindo audio e transcrevendo...", state="running")
            result = transcribe_video(
                video_path=video_path,
                output_root=OUTPUT_DIR,
                model=model,
                language=language,
                vad_filter=vad_filter,
            )
            status.update(label="Transcricao concluida.", state="complete")

        metrics = st.columns(3)
        metrics[0].metric("Idioma", result.language or "-")
        metrics[1].metric("Duracao", format_duration(result.duration))
        metrics[2].metric("Trechos", str(len(result.segments)))

        st.subheader("Texto extraido")
        st.text_area("Transcricao", result.text, height=360)

        download_cols = st.columns(3)
        download_cols[0].download_button(
            "Baixar TXT",
            data=result.text_path.read_bytes(),
            file_name=result.text_path.name,
            mime="text/plain",
        )
        download_cols[1].download_button(
            "Baixar SRT",
            data=result.srt_path.read_bytes(),
            file_name=result.srt_path.name,
            mime="application/x-subrip",
        )
        download_cols[2].download_button(
            "Baixar JSON",
            data=result.json_path.read_bytes(),
            file_name=result.json_path.name,
            mime="application/json",
        )

        st.success(f"Arquivos salvos em: {result.output_dir}")

    except Exception as error:
        st.error(str(error))
        st.exception(error)
elif not local_videos:
    st.warning("Coloque um video nesta pasta ou envie um arquivo para comecar.")
