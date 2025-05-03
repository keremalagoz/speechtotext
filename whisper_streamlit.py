import streamlit as st
import requests
import io

# --- Dil Tanımlamaları ---

# Arayüz metinleri için sözlük yapısı
texts = {
    'tr': {
        'app_title': "☁️ Whisper API ile Ses Dosyasını Metne Çevirme",
        'app_description': "Ses dosyanızı yükleyin, OpenAI Whisper API'si ile metne çevirelim.",
        'sidebar_lang_select': "Arayüz Dili:",
        'api_key_missing': "OpenAI API Anahtarı Streamlit Secrets'ta bulunamadı! Lütfen `OPENAI_API_KEY` adıyla ekleyin.",
        'api_key_needed': "Devam etmek için lütfen API anahtarınızı Streamlit Secrets'a ekleyin.",
        'upload_label': "Bir ses dosyası seçin...",
        'audio_preview_error': "Ses önizlemesi yüklenemedi.",
        'audio_lang_select': "Ses Dosyasının Dili:",
        'transcribe_button': "Metne Çevir",
        'spinner_text': "Ses API'ye gönderiliyor ve işleniyor...",
        'api_request_info': "OpenAI Whisper API'sine gönderiliyor...",
        'api_response_success': "API'den yanıt alındı.",
        'transcription_success': "Başarıyla Metne Çevrildi!",
        'output_text_label': "Çıktı Metni:",
        'output_text_area_label': "Metin",
        'transcription_empty_warning': "Metin çevrilemedi (çıktı boş), API'den geçerli bir metin dönmedi.",
        'api_request_error': "API isteği sırasında hata:",
        'api_response_error_details': "API Yanıtı:",
        'unexpected_error': "Beklenmedik bir hata oluştu:",
        'footer_caption': "Bu uygulama OpenAI Whisper API ve Streamlit kullanılarak oluşturulmuştur.",
        'footer_pricing': "Kullanım maliyetleri için OpenAI fiyatlandırmasını kontrol edin.",
        'select_file_prompt': "Lütfen yukarıdan çevrilecek bir ses dosyası yükleyin.",
    },
    'en': {
        'app_title': "☁️ Speech-to-Text with Whisper API",
        'app_description': "Upload your audio file, and we'll transcribe it using the OpenAI Whisper API.",
        'sidebar_lang_select': "Interface Language:",
        'api_key_missing': "OpenAI API Key not found in Streamlit Secrets! Please add it as `OPENAI_API_KEY`.",
        'api_key_needed': "Please add your API key to Streamlit Secrets to proceed.",
        'upload_label': "Choose an audio file...",
        'audio_preview_error': "Could not load audio preview.",
        'audio_lang_select': "Audio File Language:",
        'transcribe_button': "Transcribe",
        'spinner_text': "Sending audio to API and processing...",
        'api_request_info': "Sending request to OpenAI Whisper API...",
        'api_response_success': "Received response from API.",
        'transcription_success': "Successfully Transcribed!",
        'output_text_label': "Output Text:",
        'output_text_area_label': "Text",
        'transcription_empty_warning': "Transcription failed (output empty), did not receive valid text from API.",
        'api_request_error': "Error during API request:",
        'api_response_error_details': "API Response:",
        'unexpected_error': "An unexpected error occurred:",
        'footer_caption': "This application was created using OpenAI Whisper API and Streamlit.",
        'footer_pricing': "Check OpenAI pricing for usage costs.",
        'select_file_prompt': "Please upload an audio file above to transcribe.",
    }
}

# Whisper API'si için desteklenen diller (ISO 639-1 kodları) ve gösterim adları
# Daha fazla dil ekleyebilirsiniz: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
supported_audio_languages = {
    "Türkçe": "tr",
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    # İhtiyacınıza göre daha fazla dil ekleyin
}

# --- Yardımcı Fonksiyonlar ---
def get_text(key):
    """Mevcut arayüz diline göre metni döndürür."""
    return texts[st.session_state.lang].get(key, f"Missing text: {key}")

# --- API ile Transkripsiyon Fonksiyonu ---
def transcribe_audio_openai_api(api_key, audio_bytes, filename, audio_language_code):
    """OpenAI Whisper API'sini kullanarak sesi metne çevirir."""
    files = {'file': (filename, audio_bytes)}
    headers = {'Authorization': f'Bearer {api_key}'}
    # Seçilen ses dili kodunu API'ye gönder
    data = {'model': 'whisper-1', 'language': audio_language_code}

    st.info(get_text('api_request_info'))
    try:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            files=files,
            data=data # Dil parametresi eklendi
        )
        response.raise_for_status() # HTTP hatalarını kontrol et (4xx, 5xx)
        result = response.json()
        st.success(get_text('api_response_success'))
        return result.get("text"), None
    except requests.exceptions.RequestException as e:
        error_message = f"{get_text('api_request_error')} {e}"
        # Yanıttan daha fazla detay almaya çalış (varsa)
        try:
            error_details = response.json()
            error_message += f"\n{get_text('api_response_error_details')} {error_details}"
        except:
            pass # JSON okunamıyorsa veya response yoksa geç
        return "", error_message
    except Exception as e:
        return "", f"{get_text('unexpected_error')} {e}"

# --- Streamlit Arayüzü ---

# Sayfa yapılandırması (Başlık artık dinamik olarak ayarlanacak)
st.set_page_config(page_title="Ses Metne Çevirme", layout="centered")

# Arayüz dilini session state'de sakla ve başlat
if 'lang' not in st.session_state:
    st.session_state.lang = 'tr' # Varsayılan dil Türkçe

# Sidebar'da arayüz dili seçimi
st.sidebar.selectbox(
    get_text('sidebar_lang_select'),
    options=['tr', 'en'],
    format_func=lambda x: "Türkçe" if x == 'tr' else "English",
    key='lang' # Bu key sayesinde seçilen değer doğrudan st.session_state.lang'a atanır
)

# Ana başlık ve açıklama (get_text ile)
st.title(get_text('app_title'))
st.write(get_text('app_description'))

# API Anahtarını Güvenli Şekilde Alma
try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error(get_text('api_key_missing'))
    openai_api_key = None

# --- Ana Uygulama Alanı ---
if openai_api_key: # Sadece API anahtarı varsa devam et
    uploaded_file = st.file_uploader(
        get_text('upload_label'),
        type=["wav", "mp3", "ogg", "flac", "m4a", "aac", "mpeg", "mpga", "webm"]
    )

    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        file_extension = uploaded_file.name.split('.')[-1]

        # Ses önizlemesi
        audio_format_for_player = f"audio/{file_extension}"
        if file_extension.lower() == 'm4a': audio_format_for_player = "audio/mp4"
        try:
            st.audio(audio_bytes, format=audio_format_for_player)
        except Exception as e:
            st.warning(f"{get_text('audio_preview_error')}")

        # Ses dosyasının dilini seçme
        selected_audio_language_name = st.selectbox(
            get_text('audio_lang_select'),
            options=list(supported_audio_languages.keys()) # Gösterilecek dil adları
        )
        # Seçilen ad'a karşılık gelen ISO kodunu al
        selected_audio_language_code = supported_audio_languages[selected_audio_language_name]

        # Transkripsiyon butonu
        if st.button(get_text('transcribe_button')):
            with st.spinner(get_text('spinner_text')):
                transcribed_text, error = transcribe_audio_openai_api(
                    openai_api_key,
                    audio_bytes,
                    uploaded_file.name,
                    selected_audio_language_code # Seçilen ses dili kodunu gönder
                )

            if error:
                st.error(error)
            elif transcribed_text:
                st.success(get_text('transcription_success'))
                st.markdown(f"### {get_text('output_text_label')}")
                st.text_area(get_text('output_text_area_label'), transcribed_text, height=250)
            else:
                 st.warning(get_text('transcription_empty_warning'))

    else:
        st.info(get_text('select_file_prompt'))

else: # API anahtarı yoksa uyarı göster
    st.warning(get_text('api_key_needed'))

# Altbilgi
st.markdown("---")
st.caption(get_text('footer_caption'))
st.caption(get_text('footer_pricing'))
