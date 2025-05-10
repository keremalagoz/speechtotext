import streamlit as st
import requests
import io

# YENİ IMPORT: Mikrofon kaydı için
from streamlit_mic_recorder import mic_recorder

# Metinler sözlüğüne yeni anahtarlar eklendi
texts = {
    'tr': {
        'app_title': "☁️ Whisper API ile Ses Dosyasını Metne Çevirme",
        'app_description': "Ses dosyanızı yükleyin veya mikrofondan kaydedin, OpenAI Whisper API'si ile metne çevirelim.",
        'sidebar_lang_select': "Arayüz Dili:",
        'api_key_missing': "OpenAI API Anahtarı Streamlit Secrets'ta bulunamadı! Lütfen `OPENAI_API_KEY` adıyla ekleyin.",
        'api_key_needed': "Devam etmek için lütfen API anahtarınızı Streamlit Secrets'a ekleyin.",
        # Dosya Yükleme Sekmesi
        'file_upload_tab': "Dosya Yükle",
        'file_upload_header': "Dosyadan Metne Çevir",
        'upload_label': "Bir ses dosyası seçin...",
        'audio_preview_error': "Ses önizlemesi yüklenemedi.",
        'select_file_prompt': "Lütfen yukarıdan çevrilecek bir ses dosyası yükleyin.",
        # Mikrofon Kayıt Sekmesi
        'mic_record_tab': "Mikrofonla Kayıt",
        'mic_record_header': "Mikrofondan Metne Çevir",
        'mic_instruction': "Aşağıdaki butona basarak ses kaydı yapın. Kaydı bitirmek için tekrar basın.",
        'start_recording_button': "⏺️ Kaydı Başlat",
        'stop_recording_button': "⏹️ Kaydı Durdur",
        'recording_successful': "Ses başarıyla kaydedildi! Önizlemesini aşağıda görebilirsiniz.",
        'mic_prompt_to_record': "Lütfen metne çevirmek için bir ses kaydedin.",
        'recorded_audio_preview': "Kaydedilen Ses:",
        # Ortak Metinler
        'audio_lang_select': "Sesin Dili:",
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
    },
    'en': {
        'app_title': "☁️ Speech-to-Text with Whisper API",
        'app_description': "Upload your audio file or record from microphone, and we'll transcribe it using the OpenAI Whisper API.",
        'sidebar_lang_select': "Interface Language:",
        'api_key_missing': "OpenAI API Key not found in Streamlit Secrets! Please add it as `OPENAI_API_KEY`.",
        'api_key_needed': "Please add your API key to Streamlit Secrets to proceed.",
        # File Upload Tab
        'file_upload_tab': "Upload File",
        'file_upload_header': "Transcribe from File",
        'upload_label': "Choose an audio file...",
        'audio_preview_error': "Could not load audio preview.",
        'select_file_prompt': "Please upload an audio file above to transcribe.",
        # Microphone Record Tab
        'mic_record_tab': "Record via Microphone",
        'mic_record_header': "Transcribe from Microphone",
        'mic_instruction': "Press the button below to start recording. Press again to stop.",
        'start_recording_button': "⏺️ Start Recording",
        'stop_recording_button': "⏹️ Stop Recording",
        'recording_successful': "Audio recorded successfully! You can preview it below.",
        'mic_prompt_to_record': "Please record audio to transcribe.",
        'recorded_audio_preview': "Recorded Audio:",
        # Common Texts
        'audio_lang_select': "Audio Language:",
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
    },
    # Diğer diller için de benzer güncellemeler yapılmalı...
    # Örnek olarak İspanyolca için birkaçını ekleyelim:
    'es': {
        'app_title': "☁️ Voz a Texto con la API de Whisper",
        'app_description': "Sube tu archivo de audio o graba desde el micrófono y lo transcribiremos usando la API de OpenAI Whisper.",
        'sidebar_lang_select': "Idioma de la Interfaz:",
        'api_key_missing': "¡Clave API de OpenAI no encontrada en Streamlit Secrets! Por favor, agrégala como `OPENAI_API_KEY`.",
        'api_key_needed': "Por favor, agrega tu clave API a Streamlit Secrets para continuar.",
        'file_upload_tab': "Subir Archivo",
        'file_upload_header': "Transcribir desde Archivo",
        'upload_label': "Elige un archivo de audio...",
        'audio_preview_error': "No se pudo cargar la vista previa del audio.",
        'mic_record_tab': "Grabar con Micrófono",
        'mic_record_header': "Transcribir desde Micrófono",
        'mic_instruction': "Presiona el botón de abajo para comenzar a grabar. Presiona de nuevo para detener.",
        'start_recording_button': "⏺️ Iniciar Grabación",
        'stop_recording_button': "⏹️ Detener Grabación",
        'recording_successful': "¡Audio grabado con éxito! Puedes previsualizarlo abajo.",
        'mic_prompt_to_record': "Por favor, graba audio para transcribir.",
        'recorded_audio_preview': "Audio Grabado:",
        'audio_lang_select': "Idioma del Audio:",
        'transcribe_button': "Transcribir",
        'spinner_text': "Enviando audio a la API y procesando...",
        'api_request_info': "Enviando solicitud a la API de OpenAI Whisper...",
        'api_response_success': "Respuesta recibida de la API.",
        'transcription_success': "¡Transcrito Exitosamente!",
        'output_text_label': "Texto de Salida:",
        'output_text_area_label': "Texto",
        'transcription_empty_warning': "La transcripción falló (salida vacía), no se recibió texto válido de la API.",
        'api_request_error': "Error durante la solicitud a la API:",
        'api_response_error_details': "Respuesta de la API:",
        'unexpected_error': "Ocurrió un error inesperado:",
        'footer_caption': "Esta aplicación fue creada usando la API de OpenAI Whisper y Streamlit.",
        'footer_pricing': "Consulta los precios de OpenAI para los costos de uso.",
        'select_file_prompt': "Por favor, sube un archivo de audio arriba para transcribir.",
    },
    # 'fr', 'de', 'it' için de benzer güncellemeler yapılmalıdır.
    # Basitlik adına, şimdilik sadece 'tr', 'en' ve 'es' kısımlarını güncelledim.
}


supported_audio_languages = {
    "Türkçe": "tr",
    "English": "en",
    "Español": "es",
    "Français": "fr",
    "Deutsch": "de",
    "Italiano": "it",
    # Daha fazla dil eklenebilir
}

def get_text(key):
    lang_code = st.session_state.get('lang', 'tr')
    # Eğer anahtar o dilde yoksa, İngilizce'ye fallback yap, o da yoksa hata mesajı
    return texts.get(lang_code, texts['en']).get(key, texts['en'].get(key, f"Missing text for key: {key} in lang: {lang_code}"))


def transcribe_audio_openai_api(api_key, audio_bytes, filename, audio_language_code):
    files = {'file': (filename, audio_bytes, "audio/wav")} # Dosya türünü belirtmek iyi bir pratik
    headers = {'Authorization': f'Bearer {api_key}'}
    data = {'model': 'whisper-1', 'language': audio_language_code}

    st.info(get_text('api_request_info'))
    try:
        response = requests.post(
            "https://api.openai.com/v1/audio/transcriptions",
            headers=headers,
            files=files,
            data=data
        )
        response.raise_for_status()
        result = response.json()
        st.success(get_text('api_response_success'))
        return result.get("text"), None
    except requests.exceptions.RequestException as e:
        error_message = f"{get_text('api_request_error')} {e}"
        try:
            error_details = response.json() # Hata detaylarını JSON olarak almaya çalış
            error_message += f"\n{get_text('api_response_error_details')} {error_details}"
        except ValueError: # Yanıt JSON değilse
             error_message += f"\n{get_text('api_response_error_details')} {response.text}"
        except Exception: # Diğer JSON ayrıştırma hataları
            pass
        return None, error_message
    except Exception as e:
        return None, f"{get_text('unexpected_error')} {e}"

# Session state anahtarlarını başlatma
if 'lang' not in st.session_state:
    st.session_state.lang = 'tr'
if 'recorded_audio_bytes' not in st.session_state:
    st.session_state.recorded_audio_bytes = None
if 'transcribed_text_file' not in st.session_state:
    st.session_state.transcribed_text_file = None
if 'transcribed_text_mic' not in st.session_state:
    st.session_state.transcribed_text_mic = None


st.set_page_config(page_title="Ses Metne Çevirme / Speech-to-Text", layout="centered")

interface_languages = {
    'tr': "Türkçe",
    'en': "English",
    'es': "Español",
    'fr': "Français",
    'de': "Deutsch",
    'it': "Italiano",
}

st.sidebar.selectbox(
    get_text('sidebar_lang_select'),
    options=list(interface_languages.keys()),
    format_func=lambda code: interface_languages[code],
    key='lang'
)

st.title(get_text('app_title'))
st.write(get_text('app_description'))

try:
    openai_api_key = st.secrets["OPENAI_API_KEY"]
except KeyError:
    st.error(get_text('api_key_missing'))
    openai_api_key = None


if openai_api_key:
    # İki giriş yöntemi için sekmeler
    tab_keys = [get_text('file_upload_tab'), get_text('mic_record_tab')]
    tab1, tab2 = st.tabs(tab_keys)

    with tab1: # Dosya Yükleme Sekmesi
        st.header(get_text('file_upload_header'))
        uploaded_file = st.file_uploader(
            get_text('upload_label'),
            type=["wav", "mp3", "ogg", "flac", "m4a", "aac", "mpeg", "mpga", "webm"],
            key="file_uploader"
        )

        if uploaded_file is not None:
            audio_bytes_file = uploaded_file.read()
            file_extension = uploaded_file.name.split('.')[-1].lower()
            
            audio_format_for_player = f"audio/{file_extension}"
            if file_extension == 'm4a': audio_format_for_player = "audio/mp4"
            elif file_extension == 'mpga': audio_format_for_player = "audio/mpeg"
            
            try:
                st.audio(audio_bytes_file, format=audio_format_for_player)
            except Exception:
                st.warning(get_text('audio_preview_error'))

            audio_lang_display_names_file = list(supported_audio_languages.keys())
            selected_audio_language_name_file = st.selectbox(
                get_text('audio_lang_select'),
                options=audio_lang_display_names_file,
                key='file_audio_lang'
            )
            selected_audio_language_code_file = supported_audio_languages[selected_audio_language_name_file]

            if st.button(get_text('transcribe_button'), key='transcribe_file'):
                with st.spinner(get_text('spinner_text')):
                    transcribed_text, error = transcribe_audio_openai_api(
                        openai_api_key,
                        audio_bytes_file,
                        uploaded_file.name,
                        selected_audio_language_code_file
                    )
                if error:
                    st.error(error)
                    st.session_state.transcribed_text_file = None
                elif transcribed_text:
                    st.success(get_text('transcription_success'))
                    st.session_state.transcribed_text_file = transcribed_text
                else:
                    st.warning(get_text('transcription_empty_warning'))
                    st.session_state.transcribed_text_file = None
            
            if st.session_state.transcribed_text_file:
                st.markdown(f"### {get_text('output_text_label')}")
                st.text_area(get_text('output_text_area_label'), st.session_state.transcribed_text_file, height=250, key='file_output_text_area')

        else:
            st.info(get_text('select_file_prompt'))
            st.session_state.transcribed_text_file = None


    with tab2: # Mikrofonla Kayıt Sekmesi
        st.header(get_text('mic_record_header'))
        st.write(get_text('mic_instruction'))

        # streamlit-mic-recorder'dan gelen ses verisi
        # `format="wav"` varsayılan ve Whisper için uygun
        audio_data = mic_recorder(
            start_prompt=get_text('start_recording_button'),
            stop_prompt=get_text('stop_recording_button'),
            key='mic_recorder_component',
            use_container_width=True
        )

        if audio_data and audio_data['bytes']:
            st.session_state.recorded_audio_bytes = audio_data['bytes']
            st.success(get_text('recording_successful'))
        
        if st.session_state.recorded_audio_bytes:
            st.markdown(f"#### {get_text('recorded_audio_preview')}")
            st.audio(st.session_state.recorded_audio_bytes, format="audio/wav")

            audio_lang_display_names_mic = list(supported_audio_languages.keys())
            selected_audio_language_name_mic = st.selectbox(
                get_text('audio_lang_select'),
                options=audio_lang_display_names_mic,
                key='mic_audio_lang'
            )
            selected_audio_language_code_mic = supported_audio_languages[selected_audio_language_name_mic]

            if st.button(get_text('transcribe_button'), key='transcribe_mic'):
                with st.spinner(get_text('spinner_text')):
                    filename_mic = "microphone_recording.wav"
                    transcribed_text, error = transcribe_audio_openai_api(
                        openai_api_key,
                        st.session_state.recorded_audio_bytes,
                        filename_mic,
                        selected_audio_language_code_mic
                    )
                if error:
                    st.error(error)
                    st.session_state.transcribed_text_mic = None
                elif transcribed_text:
                    st.success(get_text('transcription_success'))
                    st.session_state.transcribed_text_mic = transcribed_text
                else:
                    st.warning(get_text('transcription_empty_warning'))
                    st.session_state.transcribed_text_mic = None
            
            if st.session_state.transcribed_text_mic:
                st.markdown(f"### {get_text('output_text_label')}")
                st.text_area(get_text('output_text_area_label'), st.session_state.transcribed_text_mic, height=250, key='mic_output_text_area')
        
        else:
            st.info(get_text('mic_prompt_to_record'))
            st.session_state.transcribed_text_mic = None

else:
    st.warning(get_text('api_key_needed'))

st.markdown("---")
st.caption(get_text('footer_caption'))
st.caption(get_text('footer_pricing'))
