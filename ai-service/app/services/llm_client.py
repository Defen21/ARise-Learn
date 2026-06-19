"""LLM client abstraction supporting Gemini, OpenAI, and mock mode."""

import re
from abc import ABC, abstractmethod
from app.core.config import get_settings


# Regex pattern matching CJK Unified Ideographs + extensions + radicals
_CJK_PATTERN = re.compile(
    r'[\u4e00-\u9fff'       # CJK Unified Ideographs
    r'\u3400-\u4dbf'        # CJK Unified Ideographs Extension A
    r'\u2e80-\u2eff'        # CJK Radicals Supplement
    r'\u3000-\u303f'        # CJK Symbols and Punctuation
    r'\uff00-\uffef'        # Halfwidth and Fullwidth Forms
    r'\u3040-\u309f'        # Hiragana
    r'\u30a0-\u30ff'        # Katakana
    r'\uac00-\ud7af]+',     # Hangul Syllables
    flags=re.UNICODE,
)


def strip_cjk(text: str) -> str:
    """Remove CJK (Chinese/Japanese/Korean) characters that leak from LLM output."""
    return _CJK_PATTERN.sub('', text)


def sanitize_image_url(url: str | None) -> str | None:
    if not url:
        return url
    url = url.strip()
    if not url.startswith(("http://", "https://", "data:")):
        return "https://" + url
    return url



class BaseLLMClient(ABC):
    @abstractmethod
    async def generate(self, prompt: str, image_url: str | None = None) -> str:
        ...


class MockLLMClient(BaseLLMClient):
    """Returns a structured academic response when in mock mode based on keywords."""

    async def generate(self, prompt: str, image_url: str | None = None) -> str:
        image_url = sanitize_image_url(image_url)
        text = (image_url or "").lower()
        prompt_lower = prompt.lower()
        
        # 1. First Call: Vision analysis requests TOPIC, CONTENT, 3D_HINT, CONFIDENCE
        if "you are analyzing a photo" in prompt_lower or "analyze this textbook image" in prompt_lower:
            # First match by explicit image URL keywords
            if "heart" in text or "anatomy" in text or "jantung" in text or "1530026405186" in text:
                return (
                    "TOPIC: Anatomi Jantung Manusia\n"
                    "CONTENT: Struktur internal jantung manusia termasuk atrium kiri/kanan, ventrikel kiri/kanan, katup jantung, dan pembuluh darah utama seperti aorta.\n"
                    "3D_HINT: heart\n"
                    "CONFIDENCE: 0.94"
                )
            elif "dna" in text or "biology" in text or "genetika" in text or "150767979998" in text:
                return (
                    "TOPIC: Genetika - Helix Ganda DNA\n"
                    "CONTENT: Struktur heliks ganda DNA yang terdiri dari gugus fosfat, gula deoksiribosa, dan pasangan basa nitrogen (A-T, C-G).\n"
                    "3D_HINT: dna_helix\n"
                    "CONFIDENCE: 0.92"
                )
            elif "h2o" in text or "chemistry" in text or "water" in text or "1544383835" in text:
                return (
                    "TOPIC: Kimia Molekul - H2O (Air)\n"
                    "CONTENT: Ikatan kovalen polar antara satu atom oksigen dan dua atom hidrogen, membentuk geometri molekul bengkok.\n"
                    "3D_HINT: water_molecule\n"
                    "CONFIDENCE: 0.89"
                )
            elif "atom" in text or "bohr" in text or "1635070041078" in text:
                return (
                    "TOPIC: Struktur Dasar Atom\n"
                    "CONTENT: Model atom Rutherford-Bohr yang menunjukkan inti atom dikelilingi elektron pada tingkat lintasan tertentu.\n"
                    "3D_HINT: atom\n"
                    "CONFIDENCE: 0.96"
                )
            
            # Fallback to check course context
            course_context = ""
            if "additional context:" in prompt_lower:
                course_context = prompt_lower.split("additional context:")[-1]
            
            if "jantung" in course_context or "heart" in course_context or "anatomy" in course_context:
                return (
                    "TOPIC: Anatomi Jantung Manusia\n"
                    "CONTENT: Struktur internal jantung manusia termasuk atrium kiri/kanan, ventrikel kiri/kanan, katup jantung, dan pembuluh darah utama seperti aorta.\n"
                    "3D_HINT: heart\n"
                    "CONFIDENCE: 0.94"
                )
            elif "dna" in course_context or "genetika" in course_context:
                return (
                    "TOPIC: Genetika - Helix Ganda DNA\n"
                    "CONTENT: Struktur heliks ganda DNA yang terdiri dari gugus fosfat, gula deoksiribosa, dan pasangan basa nitrogen (A-T, C-G).\n"
                    "3D_HINT: dna_helix\n"
                    "CONFIDENCE: 0.92"
                )
            elif "h2o" in course_context or "water" in course_context or "kimia" in course_context or "chemistry" in course_context:
                return (
                    "TOPIC: Kimia Molekul - H2O (Air)\n"
                    "CONTENT: Ikatan kovalen polar antara satu atom oksigen dan dua atom hidrogen, membentuk geometri molekul bengkok.\n"
                    "3D_HINT: water_molecule\n"
                    "CONFIDENCE: 0.89"
                )
            elif "atom" in course_context:
                return (
                    "TOPIC: Struktur Dasar Atom\n"
                    "CONTENT: Model atom Rutherford-Bohr yang menunjukkan inti atom dikelilingi elektron pada tingkat lintasan tertentu.\n"
                    "3D_HINT: atom\n"
                    "CONFIDENCE: 0.96"
                )
                
            return (
                "TOPIC: Topik Tidak Dikenal\n"
                "CONTENT: Gambar tidak jelas atau objek di luar data 3D yang didukung (Jantung, DNA, Molekul Air, Atom).\n"
                "3D_HINT: none\n"
                "CONFIDENCE: 0.45"
            )

        # 2. Second Call: Text explanation generation
        if "explain the topic:" in prompt_lower or "explain this science topic thoroughly:" in prompt_lower:
            # Extract subject to avoid matching "heart" or "dna" inside format rules
            subject = ""
            if "explain the topic:" in prompt_lower:
                subject = prompt_lower.split("explain the topic:")[-1].strip()
            elif "explain this science topic thoroughly:" in prompt_lower:
                subject = prompt_lower.split("explain this science topic thoroughly:")[-1].strip()

            subject_lower = subject.lower()
            if "jantung" in subject_lower or "heart" in subject_lower or "anatomy" in subject_lower:
                return (
                    "### Anatomi Jantung Manusia\n\n"
                    "Jantung adalah organ berongga yang tersusun atas otot jantung (miokardium) khusus, "
                    "berukuran kira-kira sebesar kepalan tangan pemiliknya, dan terletak di rongga dada sebelah kiri.\n\n"
                    "**Bagian Utama Jantung:**\n"
                    "1. **Atrium Kanan & Kiri (Serambi):** Menerima darah kembali ke jantung. Atrium kanan menerima darah kotor (kaya CO2) dari seluruh tubuh, sedangkan atrium kiri menerima darah bersih (kaya O2) dari paru-paru.\n"
                    "2. **Ventrikel Kanan & Kiri (Bilik):** Memompa darah keluar dari jantung. Ventrikel kanan memompa darah ke paru-paru (sirkulasi kecil), sedangkan ventrikel kiri memompa darah ke seluruh tubuh (sirkulasi besar) dengan otot dinding yang lebih tebal.\n"
                    "3. **Katup Jantung (Valvula):** Menjaga agar aliran darah tetap searah dan tidak kembali ke bilik sebelumnya (misalnya Katup Trikuspidal dan Bikuspidal).\n\n"
                    "*Gunakan tombol visualisasi 3D AR di atas untuk memproyeksikan potongan melintang anatomi jantung ini langsung di meja belajar Anda!*"
                )
            elif "dna" in subject_lower or "genetika" in subject_lower or "helix" in subject_lower:
                return (
                    "### Struktur Helix Ganda DNA\n\n"
                    "DNA (Deoxyribonucleic Acid) menyimpan informasi genetik seluruh makhluk hidup. "
                    "Molekul ini berbentuk seperti tangga berpilin ganda (*double helix*) berputar ke arah kanan.\n\n"
                    "**Karakteristik Utama DNA:**\n"
                    "1. **Tulang Punggung Gula-Fosfat:** Bagian samping tangga terbuat dari gugus fosfat dan gula pentosa (deoksiribosa) yang saling berikatan kovalen secara berselang-seling.\n"
                    "2. **Pasangan Basa Nitrogen:** Anak tangga dibentuk oleh basa nitrogen yang dihubungkan oleh ikatan hidrogen lemah:\n"
                    "   - **Adenin (A)** berpasangan dengan **Timin (T)** (dihubungkan oleh 2 ikatan hidrogen).\n"
                    "   - **Guanin (G)** berpasangan dengan **Sitosin (C)** (dihubungkan oleh 3 ikatan hidrogen).\n"
                    "3. **Arah Antiparalel:** Kedua rantai DNA berorientasi berlawanan arah (dari ujung 5' ke 3' dan ujung 3' ke 5').\n\n"
                    "*Aktifkan visualisasi AR untuk memutar model heliks DNA, mengamati pasangan basa nitrogen secara mendalam, dan memvisualisasikan replikasi genetik.*"
                )
            elif "h2o" in subject_lower or "molekul" in subject_lower or "air" in subject_lower or "chemistry" in subject_lower or "water" in subject_lower:
                return (
                    "### Struktur & Geometri Molekul Air (H2O)\n\n"
                    "Molekul air terdiri dari satu atom Oksigen (O) dan dua atom Hidrogen (H). "
                    "Sifat fisika-kimia air menjadikannya pelarut universal yang unik.\n\n"
                    "**Karakteristik Molekular:**\n"
                    "1. **Ikatan Kovalen Polar:** Atom Oksigen sangat elektronegatif, menarik pasangan elektron ikatan lebih dekat ke dirinya, menghasilkan kutub parsial negatif (δ-) di Oksigen dan parsial positif (δ+) di Hidrogen.\n"
                    "2. **Geometri Sudut Bengkok (Bent Geometry):** Adanya dua pasang elektron bebas (*lone pairs*) pada atom Oksigen menolak ikatan O-H ke bawah, membentuk sudut ikatan spesifik sebesar **104.5°**.\n"
                    "3. **Ikatan Hidrogen:** Karena kepolarannya, antar-molekul air dapat saling tarik-menarik membentuk jaringan ikatan hidrogen yang memberikan sifat kohesi-adhesi yang kuat dan titik didih tinggi.\n\n"
                    "*Proyeksikan model molekul H2O 3D untuk melihat susunan geometri bengkok serta interaksi tarikan polar antar-molekul secara spasial.*"
                )
            elif "atom" in subject_lower or "bohr" in subject_lower or "proton" in subject_lower:
                return (
                    "### Struktur Dasar Atom (Model Bohr)\n\n"
                    "Atom adalah unit penyusun terkecil dari materi yang mempertahankan sifat kimia dari unsur tersebut.\n\n"
                    "**Komponen Utama Atom:**\n"
                    "1. **Inti Atom (Nukleus):** Berada di bagian tengah atom, terdiri atas **Proton** (bermuatan positif) dan **Neutron** (netral, tidak bermuatan).\n"
                    "2. **Elektron:** Partikel bermuatan negatif yang mengorbit inti atom pada tingkat energi lintasan (kulit atom) tertentu.\n"
                    "3. **Gaya Tarik Coulomb:** Gaya elektrostatik yang mengikat elektron negatif agar tetap berada dalam lintasan orbit mengitari inti positif.\n\n"
                    "*Gunakan penampil AR untuk memproyeksikan visualisasi interaktif perputaran elektron pada lintasan kulit atom Bohr ini.*"
                )
            else:
                return (
                    "### Topik / Objek Tidak Didukung 3D\n\n"
                    f"Asisten akademik mendeteksi topik: **{subject}**.\n\n"
                    "Materi visualisasi 3D interaktif belum tersedia untuk topik ini. Silakan pindai ulang buku teks yang membahas Jantung, DNA, Molekul Air, atau Atom untuk melihat model 3D interaktif."
                )

        # 3. Third Call: Scoped Chat Q&A
        if "strict academic tutor" in prompt_lower:
            topic = "Struktur Dasar Atom"
            if "jantung" in prompt_lower or "heart" in prompt_lower:
                topic = "Anatomi Jantung Manusia"
            elif "dna" in prompt_lower:
                topic = "Genetika - Helix Ganda DNA"
            elif "h2o" in prompt_lower or "air" in prompt_lower:
                topic = "Kimia Molekul - H2O (Air)"
            
            # Check if user message is off-topic
            off_topic_indicators = ["presiden", "politik", "masak", "nasi goreng", "cuaca", "game", "main", "sejarah indonesia", "wisata", "liburan", "offtopic", "outside", "makan", "film", "lagu", "siapa", "dimana"]
            
            user_msg = ""
            if "user:" in prompt_lower:
                user_msg = prompt_lower.split("user:")[-1].split("assistant:")[0].strip()
            
            is_off_topic = any(keyword in user_msg for keyword in off_topic_indicators)
            
            if is_off_topic:
                return (
                    f"Maaf, saya diprogram sebagai asisten akademik khusus untuk topik '{topic}'. "
                    f"Saya tidak dapat menjawab pertanyaan di luar topik tersebut untuk menjaga fokus pembelajaran Anda."
                )
            
            # On-topic mock replies
            if "inti" in user_msg or "nucleus" in user_msg or "nukleus" in user_msg or "proton" in user_msg or "neutron" in user_msg:
                if topic == "Anatomi Jantung Manusia":
                    return "Inti jantung dilindungi oleh perikardium dan tersusun atas otot jantung (miokardium) khusus."
                elif topic == "Genetika - Helix Ganda DNA":
                    return "DNA terletak di dalam nukleus (inti sel) eukariotik dan terikat erat pada protein histon."
                else:
                    return "Inti atom terletak di pusat atom, bermuatan positif, dan berisi proton (+) serta neutron (netral) yang sangat rapat."
            elif "elektron" in user_msg or "orbit" in user_msg or "lintasan" in user_msg:
                return "Elektron bergerak mengelilingi inti atom dalam lintasan stasioner (orbit Bohr) dengan tingkat energi diskret tertentu."
            elif "darah" in user_msg or "katup" in user_msg or "serambi" in user_msg or "bilik" in user_msg:
                return "Katup jantung berfungsi menjaga agar darah bersih dan darah kotor tidak bercampur serta mengalir searah."
            elif "basa" in user_msg or "nitrogen" in user_msg or "pasangan" in user_msg:
                return "Pasangan basa nitrogen pada DNA selalu spesifik: Adenin dengan Timin, dan Guanin dengan Sitosin."
            else:
                return f"Tentu, terkait topik '{topic}', konsep ini sangat penting dalam kurikulum. Apakah ada bagian spesifik seperti komponen, fungsi, atau struktur 3D-nya yang ingin Anda tanyakan?"

        return (
            "[Mock LLM Response] Berdasarkan materi buku teks yang dipindai:\n\n"
            "Topik ini mencakup konsep dasar akademik. Anda dapat mengkonfigurasi "
            "GEMINI_API_KEY atau OPENAI_API_KEY di berkas `.env` untuk analisis real-time."
        )


class GeminiClient(BaseLLMClient):
    """Google Gemini multimodal LLM client."""

    def __init__(self):
        import google.generativeai as genai
        settings = get_settings()
        genai.configure(api_key=settings.gemini_api_key)
        self.model = genai.GenerativeModel(settings.gemini_model)

    async def generate(self, prompt: str, image_url: str | None = None) -> str:
        image_url = sanitize_image_url(image_url)
        content = [prompt]
        if image_url:
            try:
                import httpx
                from PIL import Image
                import io
                async with httpx.AsyncClient() as client:
                    resp = await client.get(image_url, timeout=12.0)
                    if resp.status_code == 200:
                        img = Image.open(io.BytesIO(resp.content))
                        content.append(img)
                    else:
                        content.append(f"[Image reference failed: {image_url}]")
            except Exception as e:
                print(f"Error loading image for Gemini: {e}")
                content.append(f"[Image reference: {image_url}]")
        
        # Run generate_content
        response = self.model.generate_content(content)
        return strip_cjk(response.text)


class OpenAIClient(BaseLLMClient):
    """OpenAI GPT-4o multimodal client."""

    def __init__(self):
        from openai import AsyncOpenAI
        settings = get_settings()
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def generate(self, prompt: str, image_url: str | None = None) -> str:
        image_url = sanitize_image_url(image_url)
        messages = []
        content = [{"type": "text", "text": prompt}]
        if image_url:
            try:
                import httpx
                import base64
                async with httpx.AsyncClient() as client:
                    resp = await client.get(image_url, timeout=12.0)
                    if resp.status_code == 200:
                        mime_type = resp.headers.get("content-type", "image/jpeg")
                        b64_data = base64.b64encode(resp.content).decode("utf-8")
                        image_data_url = f"data:{mime_type};base64,{b64_data}"
                        content.append({"type": "image_url", "image_url": {"url": image_data_url}})
                    else:
                        content.append({"type": "text", "text": f"[Image reference failed: {image_url}]"})
            except Exception as e:
                print(f"Error loading image for OpenAI: {e}")
                content.append({"type": "text", "text": f"[Image reference: {image_url}]"})
        
        messages.append({"role": "user", "content": content})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1024,
        )
        return strip_cjk(response.choices[0].message.content)

class GroqClient(BaseLLMClient):
    """Groq API client (OpenAI-compatible)."""

    def __init__(self):
        from openai import AsyncOpenAI
        settings = get_settings()
        self.client = AsyncOpenAI(
            api_key=settings.groq_api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        self.model = settings.groq_model or "meta-llama/llama-4-scout-17b-16e-instruct"

    async def generate(self, prompt: str, image_url: str | None = None) -> str:
        image_url = sanitize_image_url(image_url)
        messages = []
        content = [{"type": "text", "text": prompt}]
        has_image = False
        if image_url:
            try:
                import httpx
                import base64
                async with httpx.AsyncClient(follow_redirects=True) as client:
                    resp = await client.get(image_url, timeout=15.0)
                    if resp.status_code == 200:
                        raw_mime = resp.headers.get("content-type", "image/jpeg")
                        mime_type = raw_mime.split(";")[0].strip()
                        if not mime_type.startswith("image/"):
                            mime_type = "image/jpeg"
                        b64_data = base64.b64encode(resp.content).decode("utf-8")
                        image_data_url = f"data:{mime_type};base64,{b64_data}"
                        print(f"[Groq Client] Image loaded: mime={mime_type}, size={len(b64_data)} bytes")
                        content.append({"type": "image_url", "image_url": {"url": image_data_url}})
                        has_image = True
                    else:
                        print(f"Groq: image fetch returned {resp.status_code} for {image_url}")
                        content.append({"type": "text", "text": f"[Image could not be loaded from: {image_url}]"})
            except Exception as e:
                print(f"Error loading image for Groq: {e}")
                content.append({"type": "text", "text": f"[Image could not be loaded: {image_url}]"})

        # System message to enforce language discipline
        messages.append({
            "role": "system",
            "content": (
                "You MUST write exclusively in Bahasa Indonesia (or English if asked). "
                "NEVER output Chinese characters (Hanzi/漢字), Japanese (Hiragana/Katakana), "
                "Korean (Hangul), or any CJK script. Use only Latin alphabet characters. "
                "For example, write 'berkontraksi' instead of '收缩', 'mengembang' instead of '膨胀'."
            ),
        })
        # If no image was loaded, simplify content to plain text (avoids Groq vision errors)
        if not has_image:
            messages.append({"role": "user", "content": prompt})
        else:
            messages.append({"role": "user", "content": content})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=1024,
            )
            if response.choices and response.choices[0].message.content:
                return strip_cjk(response.choices[0].message.content)
            return "[Groq returned empty response]"
        except Exception as e:
            print(f"Groq API error: {e}")
            # Retry once with text-only if vision call failed
            if has_image:
                print("Retrying Groq without image...")
                try:
                    response = await self.client.chat.completions.create(
                        model=self.model,
                        messages=[{"role": "user", "content": prompt}],
                        max_tokens=1024,
                    )
                    if response.choices and response.choices[0].message.content:
                        return strip_cjk(response.choices[0].message.content)
                except Exception as retry_e:
                    print(f"Groq retry also failed: {retry_e}")
            raise


def create_llm_client() -> BaseLLMClient:
    """Factory: creates the appropriate LLM client based on config."""
    settings = get_settings()
    provider = settings.llm_provider.lower()

    if provider == "gemini":
        return GeminiClient()
    elif provider == "openai":
        return OpenAIClient()
    elif provider == "groq":
        return GroqClient()
    else:
        return MockLLMClient()
