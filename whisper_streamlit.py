import streamlit as st
import requests
import io

# --- API ile Transkripsiyon Fonksiyonu ---
def transcribe_audio_openai_api(api_key, audio_bytes, filename):
    """OpenAI Whisper API'sini kullanarak sesi metne çevirir."""
    files = {'file': (filename, audio_bytes)}
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'model': 'whisper-1', 'language': 'tr'} # Türkçe için 'tr'

    st.info("OpenAI Whisper API'sine gönderiliyor...")
    try:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            files=files,
            data=data
        )
        response.raise_for_status() # HTTP hatalarını kontrol et (4xx, 5xx)
        result = response.json()
        st.success("API'den yanıt alındı.")
        return result.get("text"), None
    except requests.exceptions.RequestException as e:
        error_message = f"API isteği sırasında hata: {e}"
        # Yanıttan daha fazla detay almaya çalış (varsa)
        try:
            error_details = response.json()
            error_message += f"\nAPI Yanıtı: {error_details}"
        except:
            pass # JSON okunamıyorsa veya response yoksa geç
        return "", error_message
    except Exception as e:
        return "", f"Beklenmedik bir hata oluştu: {e}"

# --- Streamlit Arayüzü ---
st.set_page_config(page_title="Whisper API ile Ses Metne Çevirme", layout="centered")
st.title("☁️ Whisper API ile Ses Dosyasını Metne Çevirme")
st.write("Ses dosyanızı yükleyin, OpenAI Whisper API'si ile metne çevirelim.")

# API Anahtarını Güvenli Şekilde Alma (Streamlit Secrets)
# Streamlit Cloud'da uygulamanızın ayarlarından 'Secrets' bölümüne ekleyin:
# OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error("OpenAI API Anahtarı Streamlit Secrets'ta bulunamadı! Lütfen `OPENAI_API_KEY` adıyla ekleyin.")
    openai_api_key = None # Hata durumunda None ata

uploaded_file = st.file_uploader(
    "Bir ses dosyası seçin...",
    type=["wav", "mp3", "ogg", "flac", "m4a", "aac", "mpeg", "mpga", "webm"]
)

if uploaded_file is not None and openai_api_key:
    audio_bytes = uploaded_file.read()
    file_extension = uploaded_file.name.split('.')[-1]
    # st.audio için format
    audio_format_for_player = f"audio/{file_extension}"
    # ... (önceki koddaki st.audio format düzeltmeleri eklenebilir) ...
    try:
        st.audio(audio_bytes, format=audio_format_for_player)
    except Exception as e:
        st.warning(f"Ses önizlemesi yüklenemedi.")


    if st.button("OpenAI API ile Metne Çevir"):
        with st.spinner('Ses API\'ye gönderiliyor ve işleniyor...'):
            transcribed_text, error = transcribe_audio_openai_api(
                openai_api_key,
                audio_bytes,
                uploaded_file.name # API'ye dosya adı vermek iyi olabilir
            )

        if error:
            st.error(error)
        elif transcribed_text:
            st.success("Başarıyla Metne Çevrildi!")
            st.markdown("### Çıktı Metni:")
            st.text_area("Metin", transcribed_text, height=250)
        else:
             st.warning("Metin çevrilemedi (çıktı boş), API'den geçerli bir metin dönmedi.")

elif not openai_api_key:
     st.warning("Devam etmek için lütfen API anahtarınızı Streamlit Secrets'a ekleyin.")
else:
    st.info("Lütfen yukarıdan çevrilecek bir ses dosyası yükleyin.")

st.markdown("---")
st.caption("Bu uygulama OpenAI Whisper API ve Streamlit kullanılarak oluşturulmuştur.")
st.caption("Kullanım maliyetleri için OpenAI fiyatlandırmasını kontrol edin.")

# Gerekli Kütüphaneler (requirements.txt için):
# streamlit
# requests
