# 🔑 Pyrogram Session String Generator

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://www.python.org/)
[![Pyrogram](https://img.shields.io/badge/Pyrogram-2.0+-green.svg)](https://pyrogram.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Channel](https://img.shields.io/badge/Telegram-@samilbots-blue.svg)](https://t.me/samilbots)

> 🚀 Telegram hesapları ve botları için güvenli session string oluşturucu! Hem CLI hem de Telegram Bot desteği ile.

## ✨ Özellikler

### 🎯 **Session Oluşturma**
- 👤 **Kullanıcı Session Stringi** - Kişisel hesaplar için
- 🤖 **Bot Session Stringi** - Bot hesapları için
- 🔄 **Toplu Session Oluşturma** - Birden fazla hesap
- 💾 **Otomatik Backup** - Session güvenliği

### 🛡️ **Güvenlik Özellikleri**
- 🔐 **2FA Desteği** - İki faktörlü doğrulama
- 🧹 **Otomatik Temizlik** - Geçici dosyalar
- 📱 **SMS Doğrulama** - Güvenli kod girişi
- 🔒 **Şifreli Saklama** - Local encryption

### 🤖 **Telegram Bot**
- 📲 **Interaktif Arayüz** - Kolay kullanım
- 🎮 **Inline Buttons** - Modern tasarım
- 📊 **Session Validasyon** - Canlı kontrol
- 📝 **Log Sistemi** - Otomatik kayıtlar

### 📱 **CLI Arayüzü**
- 🎨 **Renkli Çıktılar** - Görsel deneyim
- 📋 **Menü Sistemi** - Kolay navigasyon
- ⚡ **Hızlı İşlemler** - Optimize edilmiş
- 📊 **Progress Bar** - İlerleme göstergesi

## 🚀 Hızlı Başlangıç

### 1. **Kurulum**

```bash
# Repoyu klonlayın
git clone https://github.com/kullanici/pyrogram-session-generator.git
cd pyrogram-session-generator

# Gerekli paketleri yükleyin
pip install -r requirements.txt
```

### 2. **Gereksinimler**

```text
pyrogram>=2.0.0
colorama>=0.4.4
python-dotenv>=0.19.0
tgcrypto>=1.2.3
```

### 3. **API Bilgileri**

[my.telegram.org](https://my.telegram.org/apps) adresinden API bilgilerini alın:

```python
API_ID = "12345678"        # Sayısal değer
API_HASH = "abcd1234..."   # 32+ karakter
```

## 💻 Kullanım

### 🖥️ **CLI Modunda Çalıştırma**

```bash
python main.py
```

### 🤖 **Bot Modunda Çalıştırma**

```bash
# Bot token'ınızı config.py'ye ekleyin
python telegram_session_bot.py
```

## 📚 Kullanım Kılavuzu

### 👤 **Kullanıcı Session Oluşturma**

1. **Ana menüden** "Generate User Session" seçin
2. **API bilgilerini** girin (API ID, API Hash)
3. **Telefon numaranızı** girin (+90 formatında)
4. **SMS kodunu** girin
5. **2FA varsa** şifrenizi girin
6. ✅ **Session hazır!**

### 🤖 **Bot Session Oluşturma**

1. **Ana menüden** "Generate Bot Session" seçin
2. **Bot token'ınızı** girin (@BotFather'dan)
3. ✅ **Bot session hazır!**

### 🔍 **Session Doğrulama**

```python
from session_validator import SessionValidator

async def validate_session():
    validator = SessionValidator()
    result = await validator.validate_session(session_string)
    
    if result['is_valid']:
        print(f"✅ Valid session for: {result['user_info']['first_name']}")
    else:
        print(f"❌ Invalid session: {result['error']}")
```

## 🔧 Konfigürasyon

### 📁 **Config.py**

```python
# API Credentials
PYROGRAM_API_ID = "12345678"
PYROGRAM_API_HASH = "your_api_hash"

# Bot Configuration
BOT_TOKEN = "your_bot_token"
SESSION_LOG_CHAT_ID = "-1001234567890"  # Opsiyonel

# Storage Settings
SESSION_BACKUP_DIR = "./backups"
CREATE_BACKUPS = True
SEND_TO_SAVED_MESSAGES = True

# Security
ENABLE_2FA_WARNING = True
AUTO_DELETE_TEMP_FILES = True
```

### 🌍 **Environment Variables**

```.env
# .env dosyası oluşturun
PYROGRAM_API_ID=12345678
PYROGRAM_API_HASH=your_api_hash
BOT_TOKEN=your_bot_token
```

## 💡 Kod Örnekleri

### 🔐 **Session String Kullanımı**

```python
from pyrogram import Client
import asyncio

async def main():
    # Session string ile client oluştur
    app = Client(
        name="my_session",
        session_string="BQC8s2xYAQABB..."  # Bot'tan alınan string
    )
    
    async with app:
        # Hesap bilgilerini al
        me = await app.get_me()
        print(f"👋 Merhaba {me.first_name}!")
        
        # Kayıtlı mesajlara gönder
        await app.send_message("me", "🎉 Session çalışıyor!")

if __name__ == "__main__":
    asyncio.run(main())
```

### 🤖 **Bot Session Kullanımı**

```python
from pyrogram import Client

async def bot_example():
    # Bot session string ile
    bot = Client(
        name="my_bot",
        session_string="your_bot_session_string"
    )
    
    @bot.on_message()
    async def handle_message(client, message):
        if message.text == "/start":
            await message.reply("🤖 Bot çalışıyor!")
    
    async with bot:
        await bot.idle()
```

### 🔍 **Session Bilgilerini Alma**

```python
from session_validator import SessionValidator

async def get_session_info():
    validator = SessionValidator()
    
    # Session'ı doğrula ve bilgileri al
    info = await validator.get_session_info(session_string)
    
    print(f"📱 Telefon: {info.get('phone', 'N/A')}")
    print(f"👤 İsim: {info.get('first_name', 'N/A')}")
    print(f"🆔 ID: {info.get('id', 'N/A')}")
    print(f"👑 Premium: {'✅' if info.get('is_premium') else '❌'}")
```

## 📂 Proje Yapısı

```
pyrogram-session-generator/
├── 📄 main.py                 # Ana CLI uygulaması
├── 🤖 telegram_session_bot.py # Telegram bot arayüzü  
├── ⚙️ session_manager.py      # Session oluşturma mantığı
├── 🔍 session_validator.py    # Session doğrulama
├── 🛠️ utils.py               # Yardımcı fonksiyonlar
├── ⚙️ config.py              # Konfigürasyon ayarları
├── 📋 examples.py            # Kullanım örnekleri
├── 🎮 demo_usage.py          # Demo script
├── 📄 requirements.txt       # Python bağımlılıkları
├── 📖 README.md              # Bu dosya
├── 📁 backups/               # Session yedekleri
├── 📁 logs/                  # Uygulama logları
└── 📁 exports/               # Dışa aktarılan dosyalar
```

## 🛡️ Güvenlik Önerileri

### 🔐 **Session String Güvenliği**

⚠️ **ÖNEMLİ UYARILAR:**

1. **Asla paylaşmayın** - Session stringler tam erişim sağlar
2. **Güvenli saklayın** - Environment variables kullanın
3. **Düzenli yenileyin** - Şüpheli durumda yeni oluşturun
4. **2FA aktif tutun** - Hesap güvenliği için

### 📱 **Hesap Güvenliği**

```python
# ✅ Güvenli kullanım
import os
from pyrogram import Client

session = os.getenv("PYROGRAM_SESSION")  # Environment'tan al

# ❌ Güvensiz kullanım
session = "BQC8s2xYAQABB..."  # Kodda hardcode etmeyin
```

## 🔧 Sorun Giderme

### ❓ **Yaygın Hatalar**

| Hata | Çözüm |
|------|-------|
| `Invalid API ID` | ✅ my.telegram.org'dan doğru API ID'yi alın |
| `Session Password Needed` | ✅ 2FA şifrenizi girin |
| `Phone Code Invalid` | ✅ SMS'teki 5 haneli kodu girin |
| `Rate Limited` | ✅ Belirtilen süre kadar bekleyin |
| `Auth Key Unregistered` | ✅ Yeni session oluşturun |

### 🔧 **Debug Modu**

```bash
# Detaylı log çıktısı için
python main.py --debug

# Belirli modül için log
python -c "import logging; logging.basicConfig(level=logging.DEBUG)"
```

### 📊 **Session Durumu Kontrol**

```python
from session_validator import SessionValidator

async def health_check():
    validator = SessionValidator()
    
    # Toplu session kontrolü
    sessions = ["session1", "session2", "session3"]
    results = await validator.validate_multiple_sessions(sessions)
    
    for i, result in enumerate(results):
        status = "✅ Çalışıyor" if result['is_valid'] else "❌ Sorunlu"
        print(f"Session {i+1}: {status}")
```

## 🚀 Gelişmiş Özellikler

### 📊 **Session Analytics**

```python
from session_manager import SessionManager

manager = SessionManager()

# Session istatistikleri
stats = await manager.get_session_stats()
print(f"📱 Toplam Session: {stats['total']}")
print(f"✅ Aktif Session: {stats['active']}")
print(f"❌ Sorunlu Session: {stats['invalid']}")
```

### 🔄 **Otomatik Session Yenileme**

```python
# Eski session'ları otomatik yenile
await manager.refresh_expired_sessions()
```

### 📦 **Toplu İşlemler**

```python
# Birden fazla hesap için session
phone_numbers = ["+905551234567", "+905557654321"]
sessions = await manager.create_bulk_sessions(phone_numbers)
```

## 🤝 Katkıda Bulunma

1. **Fork** edin
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. **Commit** edin (`git commit -m 'Add amazing feature'`)
4. **Push** edin (`git push origin feature/amazing-feature`)
5. **Pull Request** oluşturun

## 📞 Destek ve İletişim

### 🆘 **Yardıma mı ihtiyacınız var?**

1. 📢 **Telegram Kanalı**: [@samilbots](https://t.me/samilbots)
2. 🐛 **Bug Report**: GitHub Issues
3. 💡 **Feature Request**: GitHub Discussions
4. 📖 **Dokümantasyon**: Wiki sayfası

### 🏷️ **Etiketler**

- `session-generator` - Session string oluşturucu
- `pyrogram` - Pyrogram tabanlı
- `telegram-bot` - Bot arayüzü
- `security` - Güvenlik odaklı
- `cli-tool` - Komut satırı aracı

## ⚖️ Lisans

Bu proje MIT lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

## 🙏 Teşekkürler

- [Pyrogram](https://pyrogram.org/) - Harika Telegram client library'si
- [Colorama](https://pypi.org/project/colorama/) - Cross-platform colored terminal
- Topluluk - Geri bildirimler ve katkılar için

## 📈 İstatistikler

![GitHub Stars](https://img.shields.io/github/stars/username/repo?style=social)
![GitHub Forks](https://img.shields.io/github/forks/username/repo?style=social)
![GitHub Issues](https://img.shields.io/github/issues/username/repo)
![GitHub Downloads](https://img.shields.io/github/downloads/username/repo/total)

---

<div align="center">

**🌟 Bu projeyi beğendiyseniz star vermeyi unutmayın! 🌟**

[![Telegram](https://img.shields.io/badge/Telegram-@samilbots-blue?style=for-the-badge&logo=telegram)](https://t.me/samilbots)

**Daha fazla projemiz için [@samilbots](https://t.me/samilbots) kanalımızı takip edin!**

*Made with ❤️ by SamilBots Team*

</div>
