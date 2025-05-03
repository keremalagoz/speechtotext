import streamlit as st
import whisper
import torch
# from pydub import AudioSegment # Artık gerekli değil (sadece transkripsiyon için)
import io
import os
import tempfile

# --- Whisper Modelini Yükleme Fonksiyonu (Cache ile) ---
@st.cache_resource
def load_whisper_model(model_size="base"):
    # ... (Bu fonksiyon aynı kalıyor) ...
    device = "cpu"
    fp16_setting = False
    st.info(f"Whisper modeli yükleniyor ({model_size})... Cihaz: {device}. Bu işlem biraz zaman alabilir.")
    try:
        model = whisper.load_model(model_size, device=device)
        st.success(f"Whisper modeli ({model_size}) başarıyla yüklendi.")
        return model, fp16_setting
    except Exception as e:
        st.error(f"Model yüklenirken hata oluştu ({model_size}): {e}")
        st.error("Streamlit Cloud'un ücretsiz katmanında büyük modeller (medium, large) hafıza sorunlarına yol açabilir. 'base' veya 'small' modelini deneyin.")
        return None, False

# --- Transkripsiyon Fonksiyonu (Whisper ile - Güncellenmiş) ---
def transcribe_audio_whisper(model, fp16_setting, audio_bytes_content, original_file_extension):
    """
    Whisper modelini kullanarak ses baytlarını metne çevirir.
    Ses baytlarını geçici bir dosyaya yazar ve bu dosyayı Whisper'a verir.
    pydub ile ön işleme/dönüştürme yapmaz.
    """
    if model is None:
        return "", "Hata: Whisper modeli yüklenemedi."

    text = ""
    error_message = None
    temp_audio_path = None

    try:
        # 1. Yüklenen orijinal ses baytlarını geçici bir dosyaya yaz.
        #    Dosya uzantısını korumak, Whisper'ın formatı tanımasına yardımcı olabilir.
        with tempfile.NamedTemporaryFile(suffix=f".{original_file_extension.lower()}", delete=False) as temp_audio:
            temp_audio.write(audio_bytes_content) # Ham baytları yaz
            temp_audio_path = temp_audio.name

        # 2. Whisper ile transkripsiyon yap (geçici dosya yolunu kullanarak)
        st.info("Whisper transkripsiyonu başlıyor...")
        # Transcribe fonksiyonuna dosya yolunu ver
        result = model.transcribe(temp_audio_path, fp16=fp16_setting) # fp16=False CPU için
        text = result["text"]
        st.success("Transkripsiyon tamamlandı.")

    except Exception as e:
        error_message = f"Transkripsiyon sırasında bir hata oluştu: {e}"
        # Hatanın ffmpeg ile ilgili olup olmadığını kontrol etmek için ek bilgi
        if "ffmpeg" in str(e).lower() or "ffprobe" in str(e).lower():
             error_message += "\nffmpeg/ffprobe hatası olabilir. 'packages.txt' dosyasının 'ffmpeg' içerdiğinden ve uygulamanın yeniden başlatıldığından emin olun."
        st.warning(f"Hata oluştu. Orijinal dosya formatı: {original_file_extension}. Geçici dosya: {temp_audio_path}")

    finally:
        # 3. Geçici dosyayı sil
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
model_options = ["tiny", "base", "small"] # Ücretsiz katman için daha güvenli seçenekler
default_model_index = model_options.index("base") if "base" in model_options else 0
selected_model_size = st.selectbox(
    "Kullanılacak Whisper Modelini Seçin:",
    model_options,
    index=default_model_index,
    help="Daha büyük modeller daha doğrudur ancak daha fazla kaynak gerektirir ve yavaştır. Ücretsiz hosting için 'tiny' veya 'base' önerilir."
)

# Modeli yükle
whisper_model, fp16_ready = load_whisper_model(selected_model_size)

st.markdown("---")

# Dosya Yükleme Alanı
uploaded_file = st.file_uploader(
    "Bir ses dosyası seçin...",
    type=["wav", "mp3", "ogg", "flac", "m4a", "aac", "mpeg"] # Whisper'ın desteklediği formatlar
)

if uploaded_file is not None and whisper_model is not None:
    # Yüklenen dosyanın içeriğini oku
    audio_bytes = uploaded_file.read()
    # Dosya uzantısını al (nokta dahil olmadan)
    file_extension = uploaded_file.name.split('.')[-1]
    # Ses formatını belirle (st.audio için)
    audio_format_for_player = f"audio/{file_extension}"
    # Bilinmeyen veya yaygın olmayan uzantılar için fallback
    if file_extension.lower() in ['m4a']:
         audio_format_for_player = "audio/mp4" # Tarayıcılar genellikle m4a'yı mp4 container'ı olarak tanır
    elif file_extension.lower() in ['aac']:
        audio_format_for_player = "audio/aac"


    try:
        st.audio(audio_bytes, format=audio_format_for_player) # Yüklenen sesi dinlet
    except Exception as e:
        st.warning(f"Ses önizlemesi yüklenemedi (Format: {audio_format_for_player}). Tarayıcı bu formatı desteklemiyor olabilir, ancak çevirme işlemi denenebilir. Hata: {e}")


    # Transkripsiyonu başlat butonu
    if st.button(f"'{selected_model_size}' Modeli ile Metne Çevir"):
        with st.spinner('Ses işleniyor ve metne çevriliyor... Bu işlem dosya boyutuna ve model büyüklüğüne göre zaman alabilir.'):
            # Güncellenmiş Transkripsiyon fonksiyonunu çağır
            transcribed_text, error = transcribe_audio_whisper(
                whisper_model,
                fp16_ready,
                audio_bytes,          # Ham ses baytlarını ver
                file_extension        # Orijinal dosya uzantısını ver
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
