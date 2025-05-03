# Ses Dosyasını Metne Çevirme (Whisper API & Streamlit)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://speechtotext-whisper.streamlit.app/) <!-- DEPLOY EDİNCE BU LİNKİ GÜNCELLEYİN -->

Bu proje, kullanıcıların ses dosyalarını (MP3, WAV, M4A vb.) yükleyerek OpenAI'nin güçlü Whisper API'si aracılığıyla metne dönüştürmelerine olanak tanıyan basit bir web uygulamasıdır. Uygulama arayüzü Python'un Streamlit kütüphanesi ile oluşturulmuş ve Streamlit Community Cloud üzerinde ücretsiz olarak yayınlanmıştır (veya yayınlanabilir).

## 🚀 Özellikler

*   **Kolay Dosya Yükleme:** Çeşitli ses formatlarını destekleyen bir dosya yükleme arayüzü.
*   **Ses Önizleme:** Yüklenen ses dosyasını doğrudan tarayıcıda dinleme imkanı.
*   **Yüksek Doğruluklu Transkripsiyon:** Arka planda OpenAI Whisper API (`whisper-1` modeli) kullanarak güvenilir metin çevirisi.
*   **Basit Arayüz:** Streamlit ile oluşturulmuş kullanıcı dostu ve anlaşılır web arayüzü.
*   **Güvenli API Anahtarı Yönetimi:** OpenAI API anahtarı, Streamlit Secrets kullanılarak güvenli bir şekilde saklanır.

## ✨ Demo

<!-- Buraya uygulamanızın çalışan bir GIF'ini veya ekran görüntüsünü ekleyebilirsiniz -->
<!-- Örnek: ![Uygulama Ekran Görüntüsü](screenshot1.png)(screeshot2.png) -->
[Uygulama Ekran Görüntüsü](screenshot1.png)
[Uygulama Ekran Görüntüsü](screenshot2.png)

Uygulamayı canlı denemek için: [https://your-deployed-streamlit-app-url.streamlit.app/](https://speechtotext-whisper.streamlit.app/) <!-- DEPLOY EDİNCE BU LİNKİ GÜNCELLEYİN -->

## 🛠️ Kullanılan Teknolojiler

*   **Python:** Ana programlama dili.
*   **Streamlit:** Web arayüzünü oluşturmak ve yayınlamak için kullanılan framework.
*   **OpenAI API:** Ses tanıma işlemleri için `whisper-1` modeline erişim.
*   **Requests:** OpenAI API'sine HTTP istekleri göndermek için.
*   **ffmpeg:** (Streamlit Cloud ortamında `packages.txt` ile yüklenir) Whisper API'sinin farklı ses formatlarını işleyebilmesi için gereklidir.

## ⚙️ Kurulum ve Çalıştırma (Yerel Makinede)

Projeyi kendi bilgisayarınızda çalıştırmak için aşağıdaki adımları takip edebilirsiniz:

1.  **Depoyu Klonlayın:**
    ```bash
    git clone https://github.com/keremalagoz/speechtotext.git
    cd speechtotext
    ```

2.  **Sanal Ortam Oluşturun (Önerilir):**
    ```bash
    # Linux/macOS
    python -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Gerekli Kütüphaneleri Yükleyin:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **OpenAI API Anahtarını Ayarlayın:**
    *   Proje kök dizininde `.streamlit` adında bir klasör oluşturun.
    *   Bu klasörün içine `secrets.toml` adında bir dosya oluşturun.
    *   `secrets.toml` dosyasının içeriğini aşağıdaki gibi düzenleyin ve `sk-xxxxxxxx` kısmını kendi OpenAI API anahtarınızla değiştirin:
        ```toml
        # .streamlit/secrets.toml
        OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ```
    *   **ÖNEMLİ:** `secrets.toml` dosyasını asla Git reponuza commit etmeyin! `.gitignore` dosyanızda `.streamlit/secrets.toml` satırının bulunduğundan emin olun.

5.  **Streamlit Uygulamasını Başlatın:**
    ```bash
    streamlit run app.py
    ```
    Uygulama varsayılan tarayıcınızda açılacaktır.

## ☁️ Streamlit Community Cloud ile Yayınlama

Bu uygulamayı ücretsiz olarak web'de yayınlamak için:

1.  Projeyi bir GitHub deposuna yükleyin (`app.py`, `requirements.txt`, `packages.txt` dosyaları dahil).
2.  [Streamlit Community Cloud](https://share.streamlit.io/)'a GitHub hesabınızla giriş yapın.
3.  "New app" butonuna tıklayın ve GitHub deponuzu, branch'inizi (genellikle `main` veya `master`) ve ana Python dosyanızın yolunu (`app.py`) seçin.
4.  **`packages.txt` Dosyası:** Deponuzda aşağıdaki içeriğe sahip bir `packages.txt` dosyası olduğundan emin olun. Bu, Streamlit Cloud'un `ffmpeg`'i yüklemesini sağlar:
    ```text
    # packages.txt
    ffmpeg
    ```
5.  **Advanced Settings -> Secrets:** Uygulamanızın Streamlit Cloud ayarlarındaki "Secrets" bölümüne gidin ve OpenAI API anahtarınızı şu formatta ekleyin:
    ```toml
    OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```
6.  "Deploy!" butonuna tıklayın. Uygulamanız birkaç dakika içinde yayında olacaktır.

## 🔑 Yapılandırma (API Anahtarı)

Bu uygulamanın çalışması için bir OpenAI API anahtarına ihtiyacınız vardır.
*   OpenAI hesabınızdan bir API anahtarı oluşturun: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
*   **Kesinlikle API anahtarınızı doğrudan koda yazmayın veya herkese açık yerlerde paylaşmayın!**
*   Yerel çalıştırma için `.streamlit/secrets.toml` dosyasına ekleyin.
*   Streamlit Cloud'da yayınlamak için uygulamanın "Secrets" bölümüne ekleyin. Kod (`st.secrets["OPENAI_API_KEY"]` kullanarak) anahtara güvenli bir şekilde erişecektir.

##  kullanım

1.  Yayınlanan Streamlit uygulamasına gidin.
2.  "Bir ses dosyası seçin..." butonuna tıklayarak bilgisayarınızdan bir ses dosyası yükleyin (örn. MP3, WAV, M4A).
3.  İsteğe bağlı olarak yüklenen sesi dinleyebilirsiniz.
4.  "OpenAI API ile Metne Çevir" (veya benzeri) butonuna tıklayın.
5.  İşlem tamamlandığında, çevrilen metin aşağıdaki metin alanında görünecektir.

## 🤝 Katkıda Bulunma

Katkılarınız memnuniyetle karşılanır! Hata bildirmek veya yeni özellikler önermek için lütfen bir "Issue" açın. Kod katkısı yapmak isterseniz, bir "Pull Request" gönderebilirsiniz.

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için `LICENSE` dosyasına bakınız.

## 🙏 Teşekkürler

*   Harika API'si için [OpenAI](https://openai.com/)'a.
*   Kolay web uygulaması geliştirme ve yayınlama imkanı sunduğu için [Streamlit](https://streamlit.io/)'e.

---
# Speech-to-Text with Whisper API & Streamlit

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://speechtotext-whisper.streamlit.app/) <!-- UPDATE THIS LINK AFTER DEPLOYMENT -->

This project is a simple web application that allows users to upload audio files (MP3, WAV, M4A, etc.) and transcribe them into text using OpenAI's powerful Whisper API. The application interface is built with Python's Streamlit library and can be deployed for free on Streamlit Community Cloud. It features a multi-language interface and allows specifying the language of the audio file for accurate transcription.

## 🚀 Features

*   **Easy File Upload:** Supports various audio formats via a simple upload interface.
*   **Audio Preview:** Listen to the uploaded audio file directly in the browser.
*   **High-Accuracy Transcription:** Utilizes the OpenAI Whisper API (`whisper-1` model) for reliable speech-to-text conversion.
*   **Multi-Language Interface:** Choose the application's display language (English, Turkish, Spanish, French, German, Italian). 🇬🇧🇹🇷🇪🇸🇫🇷🇩🇪🇮🇹
*   **Audio Language Selection:** Specify the language spoken in the audio file for optimal transcription results. 🗣️🌍
*   **Simple UI:** User-friendly and straightforward web interface built with Streamlit.
*   **Secure API Key Management:** The OpenAI API key is securely stored using Streamlit Secrets.

## ✨ Demo

<!-- You can add a GIF or screenshot of your running application here -->
<!-- Example: ![Application Screenshot](screenshot.png) -->
[App Screenshot](screenshot1.png)
[App Screenshot](screenshot2.png)

Try the live application here: [https://your-deployed-streamlit-app-url.streamlit.app/](https://speechtotext-whisper.streamlit.app/) <!-- UPDATE THIS LINK AFTER DEPLOYMENT -->

## 🛠️ Technologies Used

*   **Python:** The primary programming language.
*   **Streamlit:** Framework used to build and deploy the web interface.
*   **OpenAI API:** Access to the `whisper-1` model for speech recognition.
*   **Requests:** To send HTTP requests to the OpenAI API.
*   **ffmpeg:** (Installed via `packages.txt` in the Streamlit Cloud environment) Required by the Whisper API backend to handle various audio formats.

## ⚙️ Setup and Running (Locally)

To run this project on your local machine, follow these steps:

1.  **Clone the Repository:**
    ```bash
    git clone https://github.com/keremalagoz/speechtotext.git
    cd speechtotext
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    # Linux/macOS
    python -m venv venv
    source venv/bin/activate

    # Windows
    python -m venv venv
    .\venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set Up OpenAI API Key:**
    *   Create a folder named `.streamlit` in the project's root directory.
    *   Inside this folder, create a file named `secrets.toml`.
    *   Edit the `secrets.toml` file with the following content, replacing `sk-xxxxxxxx` with your actual OpenAI API key:
        ```toml
        # .streamlit/secrets.toml
        OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        ```
    *   **IMPORTANT:** Never commit your `secrets.toml` file to your Git repository! Ensure your `.gitignore` file includes the line `.streamlit/secrets.toml`.

5.  **Run the Streamlit App:**
    ```bash
    streamlit run app.py
    ```
    The application should open in your default web browser.

## ☁️ Deploying with Streamlit Community Cloud

To deploy this application on the web for free:

1.  Push your project to a GitHub repository (including `app.py`, `requirements.txt`, and `packages.txt`).
2.  Log in to [Streamlit Community Cloud](https://share.streamlit.io/) with your GitHub account.
3.  Click "New app" and choose your GitHub repository, branch (usually `main` or `master`), and the path to your main Python file (`app.py`).
4.  **`packages.txt` File:** Ensure you have a `packages.txt` file in your repository with the following content. This tells Streamlit Cloud to install `ffmpeg`:
    ```text
    # packages.txt
    ffmpeg
    ```
5.  **Advanced Settings -> Secrets:** Go to the "Secrets" section in your application's settings on Streamlit Cloud and add your OpenAI API key in the following format:
    ```toml
    OPENAI_API_KEY = "sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ```
6.  Click "Deploy!". Your application should be live in a few minutes.

## 🔑 Configuration (API Key)

This application requires an OpenAI API key to function.
*   Obtain an API key from your OpenAI account: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
*   **Absolutely do not hardcode your API key directly in the code or share it publicly!**
*   For local execution, add it to the `.streamlit/secrets.toml` file.
*   For deployment on Streamlit Cloud, add it to the "Secrets" section of the application settings. The code (`st.secrets["OPENAI_API_KEY"]`) will securely access the key.

## 💡 Usage

1.  Navigate to the deployed Streamlit application.
2.  Use the sidebar to select your preferred interface language (English, Turkish, etc.).
3.  Click the "Choose an audio file..." button to upload an audio file from your computer (e.g., MP3, WAV, M4A).
4.  Optionally, listen to the uploaded audio using the preview player.
5.  Select the language spoken in the audio file from the "Audio File Language" dropdown.
6.  Click the "Transcribe" (or equivalent) button.
7.  Once processing is complete, the transcribed text will appear in the text area below.

## 🤝 Contributing

Contributions are welcome! Please feel free to open an "Issue" to report bugs or suggest new features. If you'd like to contribute code, please submit a "Pull Request".

## 📄 License

This project is licensed under the MIT License. See the `LICENSE` file for details.

## 🙏 Acknowledgements

*   Thanks to [OpenAI](https://openai.com/) for their powerful Whisper API.
*   Thanks to [Streamlit](https://streamlit.io/) for making web app development and deployment so easy.

---
