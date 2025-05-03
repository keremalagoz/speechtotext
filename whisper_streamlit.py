import streamlit as st
import requests
import io

# --- Dil Tanımlamaları ---

# Arayüz metinleri için sözlük yapısı (Yeni diller eklendi)
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
    },
    'es': {
        'app_title': "☁️ Voz a Texto con la API de Whisper",
        'app_description': "Sube tu archivo de audio y lo transcribiremos usando la API de OpenAI Whisper.",
        'sidebar_lang_select': "Idioma de la Interfaz:",
        'api_key_missing': "¡Clave API de OpenAI no encontrada en Streamlit Secrets! Por favor, agrégala como `OPENAI_API_KEY`.",
        'api_key_needed': "Por favor, agrega tu clave API a Streamlit Secrets para continuar.",
        'upload_label': "Elige un archivo de audio...",
        'audio_preview_error': "No se pudo cargar la vista previa del audio.",
        'audio_lang_select': "Idioma del Archivo de Audio:",
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
    'fr': {
        'app_title': "☁️ Parole en Texte avec l'API Whisper",
        'app_description': "Téléchargez votre fichier audio, et nous le transcrirons à l'aide de l'API OpenAI Whisper.",
        'sidebar_lang_select': "Langue de l'Interface:",
        'api_key_missing': "Clé API OpenAI introuvable dans Streamlit Secrets ! Veuillez l'ajouter en tant que `OPENAI_API_KEY`.",
        'api_key_needed': "Veuillez ajouter votre clé API à Streamlit Secrets pour continuer.",
        'upload_label': "Choisissez un fichier audio...",
        'audio_preview_error': "Impossible de charger l'aperçu audio.",
        'audio_lang_select': "Langue du Fichier Audio:",
        'transcribe_button': "Transcrire",
        'spinner_text': "Envoi de l'audio à l'API et traitement...",
        'api_request_info': "Envoi de la requête à l'API OpenAI Whisper...",
        'api_response_success': "Réponse reçue de l'API.",
        'transcription_success': "Transcrit avec Succès !",
        'output_text_label': "Texte de Sortie:",
        'output_text_area_label': "Texte",
        'transcription_empty_warning': "La transcription a échoué (sortie vide), texte non valide reçu de l'API.",
        'api_request_error': "Erreur lors de la requête API:",
        'api_response_error_details': "Réponse de l'API:",
        'unexpected_error': "Une erreur inattendue s'est produite:",
        'footer_caption': "Cette application a été créée en utilisant l'API OpenAI Whisper et Streamlit.",
        'footer_pricing': "Consultez la tarification OpenAI pour les coûts d'utilisation.",
        'select_file_prompt': "Veuillez télécharger un fichier audio ci-dessus pour transcrire.",
    },
    'de': {
        'app_title': "☁️ Sprache zu Text mit der Whisper API",
        'app_description': "Laden Sie Ihre Audiodatei hoch, und wir transkribieren sie mit der OpenAI Whisper API.",
        'sidebar_lang_select': "Oberflächensprache:",
        'api_key_missing': "OpenAI API-Schlüssel nicht in Streamlit Secrets gefunden! Bitte fügen Sie ihn als `OPENAI_API_KEY` hinzu.",
        'api_key_needed': "Bitte fügen Sie Ihren API-Schlüssel zu Streamlit Secrets hinzu, um fortzufahren.",
        'upload_label': "Wählen Sie eine Audiodatei...",
        'audio_preview_error': "Audiovorschau konnte nicht geladen werden.",
        'audio_lang_select': "Sprache der Audiodatei:",
        'transcribe_button': "Transkribieren",
        'spinner_text': "Audio wird an API gesendet und verarbeitet...",
        'api_request_info': "Anfrage an OpenAI Whisper API wird gesendet...",
        'api_response_success': "Antwort von API erhalten.",
        'transcription_success': "Erfolgreich Transkribiert!",
        'output_text_label': "Ausgabetext:",
        'output_text_area_label': "Text",
        'transcription_empty_warning': "Transkription fehlgeschlagen (Ausgabe leer), kein gültiger Text von API empfangen.",
        'api_request_error': "Fehler während der API-Anfrage:",
        'api_response_error_details': "API-Antwort:",
        'unexpected_error': "Ein unerwarteter Fehler ist aufgetreten:",
        'footer_caption': "Diese Anwendung wurde mit der OpenAI Whisper API und Streamlit erstellt.",
        'footer_pricing': "Überprüfen Sie die OpenAI-Preise für Nutzungskosten.",
        'select_file_prompt': "Bitte laden Sie oben eine Audiodatei zum Transkribieren hoch.",
    },
    'it': {
        'app_title': "☁️ Da Voce a Testo con l'API Whisper",
        'app_description': "Carica il tuo file audio e lo trascriveremo utilizzando l'API OpenAI Whisper.",
        'sidebar_lang_select': "Lingua Interfaccia:",
        'api_key_missing': "Chiave API OpenAI non trovata in Streamlit Secrets! Per favore, aggiungila come `OPENAI_API_KEY`.",
        'api_key_needed': "Per favore, aggiungi la tua chiave API a Streamlit Secrets per procedere.",
        'upload_label': "Scegli un file audio...",
        'audio_preview_error': "Impossibile caricare l'anteprima audio.",
        'audio_lang_select': "Lingua File Audio:",
        'transcribe_button': "Trascrivi",
        'spinner_text': "Invio dell'audio all'API ed elaborazione...",
        'api_request_info': "Invio richiesta all'API OpenAI Whisper...",
        'api_response_success': "Risposta ricevuta dall'API.",
        'transcription_success': "Trascritto con Successo!",
        'output_text_label': "Testo di Output:",
        'output_text_area_label': "Testo",
        'transcription_empty_warning': "Trascrizione fallita (output vuoto), testo non valido ricevuto dall'API.",
        'api_request_error': "Errore durante la richiesta API:",
        'api_response_error_details': "Risposta API:",
        'unexpected_error': "Si è verificato un errore imprevisto:",
        'footer_caption': "Questa applicazione è stata creata utilizzando l'API OpenAI Whisper e Streamlit.",
        'footer_pricing': "Controlla i prezzi di OpenAI per i costi di utilizzo.",
        'select_file_prompt': "Per favore, carica un file audio qui sopra per trascrivere.",
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
    # Session state başlatılmamışsa varsayılan olarak 'tr' kullan
    lang_code = st.session_state.get('lang', 'tr')
    return texts.get(lang_code, texts['en']).get(key, f"Missing text: {key}")

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

# Session state'i başlat (eğer yoksa)
if 'lang' not in st.session_state:
    st.session_state.lang = 'tr' # Varsayılan dil Türkçe

# Sayfa yapılandırması (Başlık artık dinamik olarak ayarlanacak)
st.set_page_config(page_title="Ses Metne Çevirme / Speech-to-Text", layout="centered")


# Arayüz dili seçenekleri ve gösterim adları
interface_languages = {
    'tr': "Türkçe",
    'en': "English",
    'es': "Español",
    'fr': "Français",
    'de': "Deutsch",
    'it': "Italiano",
}

# Sidebar'da arayüz dili seçimi (Güncellendi)
st.sidebar.selectbox(
    get_text('sidebar_lang_select'),
    options=list(interface_languages.keys()), # Dil kodları
    format_func=lambda code: interface_languages[code], # Gösterim adları
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

        # Ses dosyasının dilini seçme (Bu kısım aynı kalabilir çünkü diller zaten destekleniyordu)
        # Ancak gösterim adlarını arayüz diline göre dinamik yapmak GEREKMEZ,
        # çünkü sesin dili arayüz dilinden bağımsızdır. Orijinal adları kullanmak daha iyi.
        audio_lang_display_names = list(supported_audio_languages.keys())
        selected_audio_language_name = st.selectbox(
            get_text('audio_lang_select'),
            options=audio_lang_display_names
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
