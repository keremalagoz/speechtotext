import streamlit as st
import whisper
import torch # Whisper için gerekli
from pydub import AudioSegment # Farklı formatları desteklemek için
import io # Bellek içi dosya işlemleri için
import os
import tempfile # Geçici dosya oluşturmak için
import numpy as np # Whisper'a array vermek için (alternatif yöntem)

# --- Whisper Modelini Yükleme Fonksiyonu (Cache ile) ---
# @st.cache_resource, modelin sadece bir kez yüklenmesini sağlar,
# böylece her istekte tekrar indirilip yüklenmez. Bu, kaynakları korur.
@st.cache_resource
def load_whisper_model(model_size="base"):
    """Seçilen boyuttaki Whisper modelini yükler ve cache'ler."""
    # CUDA (GPU) varsa kullan, yoksa CPU kullan.
    # Streamlit Community Cloud'da genellikle sadece CPU olur.
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    device = "cpu" # Ücretsiz katmanda genellikle sadece CPU var, zorlayalım.
    # fp16=False CPU üzerinde daha stabil çalışır.
    fp16_setting = False # torch.cuda.is_available()

    st.info(f"Whisper modeli yükleniyor ({model_size})... Cihaz: {device}. Bu işlem biraz zaman alabilir.")
    try:
        model = whisper.load_model(model_size, device=device)
        st.success(f"Whisper modeli ({model_size}) başarıyla yüklendi.")
        return model, fp16_setting
    except Exception as e:
        st.error(f"Model yüklenirken hata oluştu ({model_size}): {e}")
        st.error("Streamlit Cloud'un ücretsiz katmanında büyük modeller (medium, large) hafıza sorunlarına yol açabilir. 'base' veya 'small' modelini deneyin.")
        return None, False

# --- Transkripsiyon Fonksiyonu (Whisper ile) ---
def transcribe_audio_whisper(model, fp16_setting, audio_file_content, file_extension):
    """
    Whisper modelini kullanarak ses dosyası içeriğini metne çevirir.
    pydub ile sesi yükler ve geçici dosyaya yazarak Whisper'a verir.
    """
    if model is None:
        return "", "Hata: Whisper modeli yüklenemedi."

    text = ""
    error_message = None
    temp_audio_path = None

    try:
        # 1. Ses içeriğini pydub ile yükle
        audio_io = io.BytesIO(audio_file_content)
        audio_segment = AudioSegment.from_file(audio_io, format=file_extension.lower())

        # 2. Whisper'ın işleyebileceği geçici bir dosyaya kaydet (örn: mp3 veya wav)
        #    Whisper ffmpeg kullanarak birçok formatı okuyabilir.
        with tempfile.NamedTemporaryFile(suffix=f".{file_extension.lower()}", delete=False) as temp_audio:
            # pydub ile sesi dışa aktar
            audio_segment.export(temp_audio.name, format=file_extension.lower())
            temp_audio_path = temp_audio.name

        # 3. Whisper ile transkripsiyon yap
        st.info("Whisper transkripsiyonu başlıyor...")
        # Transcribe fonksiyonuna dosya yolunu ver
        result = model.transcribe(temp_audio_path, fp16=fp16_setting) # fp16=False CPU için
        text = result["text"]
        st.success("Transkripsiyon tamamlandı.")

    except Exception as e:
        error_message = f"Transkripsiyon sırasında bir hata oluştu: {e}"
        st.warning("Not: Ses formatı işlenirken veya Whisper transkripsiyonunda sorun olabilir. 'ffmpeg' sisteminizde veya ortamda kurulu olmalıdır (Streamlit Cloud'da genellikle vardır).")
    finally:
        # 4. Geçici dosyayı sil
        if temp_audio_path and os.path.exists(temp_audio_path):
            try:
                os.remove(temp_audio_path)
            except Exception as e:
                st.warning(f"Geçici dosya silinirken hata: {e}")

    return text, error_message

# --- Streamlit Arayüzü ---
st.set_page_config(page_title="Whisper ile Ses Metne Çevirme", layout="centered")
st.title("🎤 Whisper ile Ses Dosyasını Metne Çevirme")
st.write("OpenAI Whisper modelini kullanarak ses dosyanızı (WAV, MP3, OGG, M4A vb.) metne çevirin.")

# Model Seçimi
# Streamlit Cloud ücretsiz katmanı için 'tiny' veya 'base' en uygunudur.
# 'small' bazen çalışabilir, 'medium' ve 'large' genellikle hafıza hatası verir.
model_options = ["tiny", "base", "small", "medium", "large"]
# Varsayılan olarak 'base' seçelim
default_model_index = model_options.index("base") if "base" in model_options else 0
selected_model_size = st.selectbox(
    "Kullanılacak Whisper Modelini Seçin:",
    model_options,
    index=default_model_index,
    help="Daha büyük modeller daha doğrudur ancak daha fazla kaynak gerektirir ve yavaştır. Ücretsiz hosting için 'tiny' veya 'base' önerilir."
)

# Modeli yükle (cache sayesinde sadece gerektiğinde yüklenir)
whisper_model, fp16_ready = load_whisper_model(selected_model_size)

st.markdown("---")

# Dosya Yükleme Alanı
uploaded_file = st.file_uploader(
    "Bir ses dosyası seçin...",
    type=["wav", "mp3", "ogg", "flac", "m4a", "aac"] # Whisper'ın desteklediği formatlar
)

if uploaded_file is not None and whisper_model is not None:
    # Yüklenen dosyanın içeriğini oku
    audio_bytes = uploaded_file.read()
    file_extension = uploaded_file.name.split('.')[-1]

    st.audio(audio_bytes, format=f'audio/{file_extension}') # Yüklenen sesi dinlet

    # Transkripsiyonu başlat butonu
    if st.button(f"'{selected_model_size}' Modeli ile Metne Çevir"):
        with st.spinner('Ses işleniyor ve metne çevriliyor... Bu işlem dosya boyutuna ve model büyüklüğüne göre zaman alabilir.'):
            # Transkripsiyon fonksiyonunu çağır
            transcribed_text, error = transcribe_audio_whisper(
                whisper_model, fp16_ready, audio_bytes, file_extension
            )

        if error:
            st.error(error)
        elif transcribed_text:
            st.success("Başarıyla Metne Çevrildi!")
            st.markdown("### Çıktı Metni:")
            st.text_area("Metin", transcribed_text, height=250)
        else:
            st.warning("Metin çevrilemedi (çıktı boş), ancak bir hata da oluşmadı. Dosya içeriğini kontrol edin.")

elif whisper_model is None:
    st.error("Model yüklenemediği için devam edilemiyor. Lütfen sayfayı yenileyin veya farklı bir model seçin.")
else:
    st.info("Lütfen yukarıdan çevrilecek bir ses dosyası yükleyin.")

st.markdown("---")
st.caption("Bu uygulama Streamlit ve OpenAI Whisper kullanılarak oluşturulmuştur.")
st.caption("Uyarı: Streamlit Community Cloud'un ücretsiz kaynakları (özellikle RAM) büyük Whisper modelleri için yetersiz kalabilir.")