"""
Module for handling translations and language support in the Author's AI Assistant.
"""

# Dictionary of available languages and their display names
AVAILABLE_LANGUAGES = {
    "english": "English",
    "spanish": "Español",
    "french": "Français",
    "german": "Deutsch",
    "italian": "Italiano",
    "portuguese": "Português",
    "russian": "Русский",
    "japanese": "日本語",
    "chinese": "中文",
    "hindi": "हिन्दी",
    "arabic": "العربية"
}

# UI text translations
TRANSLATIONS = {
    # Sidebar
    "app_title": {
        "english": "Author's AI Assistant",
        "spanish": "Asistente de IA para Autores",
        "french": "Assistant IA pour Auteurs",
        "german": "KI-Assistent für Autoren",
        "italian": "Assistente IA per Autori",
        "portuguese": "Assistente de IA para Autores",
        "russian": "ИИ-помощник для авторов",
        "japanese": "作家のためのAIアシスタント",
        "chinese": "作家AI助手",
        "hindi": "लेखक के लिए AI सहायक",
        "arabic": "مساعد الذكاء الاصطناعي للمؤلفين"
    },
    "api_key_label": {
        "english": "Google API Key",
        "spanish": "Clave API de Google",
        "french": "Clé API Google",
        "german": "Google API-Schlüssel",
        "italian": "Chiave API di Google",
        "portuguese": "Chave de API do Google",
        "russian": "API-ключ Google",
        "japanese": "Google APIキー",
        "chinese": "Google API密钥",
        "hindi": "Google API कुंजी",
        "arabic": "مفتاح واجهة برمجة تطبيقات Google"
    },
    "navigate": {
        "english": "Navigate",
        "spanish": "Navegar",
        "french": "Naviguer",
        "german": "Navigieren",
        "italian": "Navigare",
        "portuguese": "Navegar",
        "russian": "Навигация",
        "japanese": "ナビゲート",
        "chinese": "导航",
        "hindi": "नेविगेट करें",
        "arabic": "تصفح"
    },
    "story_status": {
        "english": "Story Status",
        "spanish": "Estado de la Historia",
        "french": "Statut de l'Histoire",
        "german": "Story-Status",
        "italian": "Stato della Storia",
        "portuguese": "Status da História",
        "russian": "Статус истории",
        "japanese": "ストーリーステータス",
        "chinese": "故事状态",
        "hindi": "कहानी की स्थिति",
        "arabic": "حالة القصة"
    },
    "start_setup": {
        "english": "Start by setting up your story on the Story Setup page",
        "spanish": "Comience configurando su historia en la página de Configuración de Historia",
        "french": "Commencez par configurer votre histoire sur la page Configuration de l'Histoire",
        "german": "Beginnen Sie mit der Einrichtung Ihrer Geschichte auf der Seite Story-Einrichtung",
        "italian": "Inizia configurando la tua storia nella pagina Configurazione Storia",
        "portuguese": "Comece configurando sua história na página Configuração da História",
        "russian": "Начните с настройки вашей истории на странице Настройка истории",
        "japanese": "ストーリー設定ページでストーリーのセットアップから始めてください",
        "chinese": "从故事设置页面开始设置您的故事",
        "hindi": "कहानी सेटअप पेज पर अपनी कहानी को सेट करके शुरू करें",
        "arabic": "ابدأ بإعداد قصتك في صفحة إعداد القصة"
    },
    
    # Navigation menu items
    "nav_story_setup": {
        "english": "Story Setup",
        "spanish": "Configuración de Historia",
        "french": "Configuration de l'Histoire",
        "german": "Story-Einrichtung",
        "italian": "Configurazione Storia",
        "portuguese": "Configuração da História",
        "russian": "Настройка истории",
        "japanese": "ストーリー設定",
        "chinese": "故事设置",
        "hindi": "कहानी सेटअप",
        "arabic": "إعداد القصة"
    },
    "nav_characters": {
        "english": "Characters",
        "spanish": "Personajes",
        "french": "Personnages",
        "german": "Charaktere",
        "italian": "Personaggi",
        "portuguese": "Personagens",
        "russian": "Персонажи",
        "japanese": "キャラクター",
        "chinese": "角色",
        "hindi": "पात्र",
        "arabic": "الشخصيات"
    },
    "nav_settings": {
        "english": "Settings",
        "spanish": "Escenarios",
        "french": "Paramètres",
        "german": "Einstellungen",
        "italian": "Ambientazioni",
        "portuguese": "Configurações",
        "russian": "Настройки",
        "japanese": "設定",
        "chinese": "设置",
        "hindi": "सेटिंग्स",
        "arabic": "الإعدادات"
    },
    "nav_plot_elements": {
        "english": "Plot Elements",
        "spanish": "Elementos de Trama",
        "french": "Éléments d'Intrigue",
        "german": "Handlungselemente",
        "italian": "Elementi della Trama",
        "portuguese": "Elementos do Enredo",
        "russian": "Элементы сюжета",
        "japanese": "プロット要素",
        "chinese": "情节元素",
        "hindi": "प्लॉट तत्व",
        "arabic": "عناصر الحبكة"
    },
    "nav_chapter_generator": {
        "english": "Chapter Generator",
        "spanish": "Generador de Capítulos",
        "french": "Générateur de Chapitres",
        "german": "Kapitel-Generator",
        "italian": "Generatore di Capitoli",
        "portuguese": "Gerador de Capítulos",
        "russian": "Генератор глав",
        "japanese": "チャプター生成器",
        "chinese": "章节生成器",
        "hindi": "अध्याय जनरेटर",
        "arabic": "مولد الفصول"
    },
    "nav_plot_analysis": {
        "english": "Plot Analysis",
        "spanish": "Análisis de Trama",
        "french": "Analyse d'Intrigue",
        "german": "Handlungsanalyse",
        "italian": "Analisi della Trama",
        "portuguese": "Análise do Enredo",
        "russian": "Анализ сюжета",
        "japanese": "プロット分析",
        "chinese": "情节分析",
        "hindi": "प्लॉट विश्लेषण",
        "arabic": "تحليل الحبكة"
    },
    "nav_creative_branches": {
        "english": "Creative Branches",
        "spanish": "Ramas Creativas",
        "french": "Branches Créatives",
        "german": "Kreative Verzweigungen",
        "italian": "Rami Creativi",
        "portuguese": "Ramificações Criativas",
        "russian": "Творческие ветви",
        "japanese": "創造的な分岐",
        "chinese": "创意分支",
        "hindi": "क्रिएटिव ब्रांचेस",
        "arabic": "فروع إبداعية"
    },
    "nav_character_arcs": {
        "english": "Character Arcs",
        "spanish": "Arcos de Personaje",
        "french": "Arcs de Personnage",
        "german": "Charakterbögen",
        "italian": "Archi dei Personaggi",
        "portuguese": "Arcos de Personagem",
        "russian": "Арки персонажей",
        "japanese": "キャラクターアーク",
        "chinese": "角色弧",
        "hindi": "पात्र आर्क",
        "arabic": "أقواس الشخصية"
    },
    "nav_plot_outline": {
        "english": "Plot Outline",
        "spanish": "Esquema de Trama",
        "french": "Aperçu de l'Intrigue",
        "german": "Handlungsumriss",
        "italian": "Schema della Trama",
        "portuguese": "Esboço do Enredo",
        "russian": "Структура сюжета",
        "japanese": "プロット概要",
        "chinese": "情节大纲",
        "hindi": "प्लॉट आउटलाइन",
        "arabic": "مخطط الحبكة"
    },
    "nav_dialogue_generator": {
        "english": "Dialogue Generator",
        "spanish": "Generador de Diálogos",
        "french": "Générateur de Dialogues",
        "german": "Dialog-Generator",
        "italian": "Generatore di Dialoghi",
        "portuguese": "Gerador de Diálogos",
        "russian": "Генератор диалогов",
        "japanese": "ダイアログ生成器",
        "chinese": "对话生成器",
        "hindi": "संवाद जनरेटर",
        "arabic": "مولد الحوار"
    },
    "nav_plot_problem_solver": {
        "english": "Plot Problem Solver",
        "spanish": "Solucionador de Problemas de Trama",
        "french": "Résolveur de Problèmes d'Intrigue",
        "german": "Handlungsproblem-Löser",
        "italian": "Risolutore di Problemi della Trama",
        "portuguese": "Solucionador de Problemas de Enredo",
        "russian": "Решение проблем сюжета",
        "japanese": "プロット問題ソルバー",
        "chinese": "情节问题解决器",
        "hindi": "प्लॉट समस्या समाधानकर्ता",
        "arabic": "حلال مشاكل الحبكة"
    },
    "nav_export_import": {
        "english": "Export/Import",
        "spanish": "Exportar/Importar",
        "french": "Exporter/Importer",
        "german": "Exportieren/Importieren",
        "italian": "Esporta/Importa",
        "portuguese": "Exportar/Importar",
        "russian": "Экспорт/Импорт",
        "japanese": "エクスポート/インポート",
        "chinese": "导出/导入",
        "hindi": "निर्यात/आयात",
        "arabic": "تصدير/استيراد"
    },
    
    # Story setup page
    "story_setup_header": {
        "english": "Story Setup",
        "spanish": "Configuración de Historia",
        "french": "Configuration de l'Histoire",
        "german": "Story-Einrichtung",
        "italian": "Configurazione Storia",
        "portuguese": "Configuração da História",
        "russian": "Настройка истории",
        "japanese": "ストーリー設定",
        "chinese": "故事设置",
        "hindi": "कहानी सेटअप",
        "arabic": "إعداد القصة"
    },
    "story_title_label": {
        "english": "Story Title",
        "spanish": "Título de la Historia",
        "french": "Titre de l'Histoire",
        "german": "Titel der Geschichte",
        "italian": "Titolo della Storia",
        "portuguese": "Título da História",
        "russian": "Название истории",
        "japanese": "ストーリータイトル",
        "chinese": "故事标题",
        "hindi": "कहानी का शीर्षक",
        "arabic": "عنوان القصة"
    },
    "genre_label": {
        "english": "Genre",
        "spanish": "Género",
        "french": "Genre",
        "german": "Genre",
        "italian": "Genere",
        "portuguese": "Gênero",
        "russian": "Жанр",
        "japanese": "ジャンル",
        "chinese": "类型",
        "hindi": "शैली",
        "arabic": "النوع الأدبي"
    },
    "language_label": {
        "english": "Language",
        "spanish": "Idioma",
        "french": "Langue",
        "german": "Sprache",
        "italian": "Lingua",
        "portuguese": "Idioma",
        "russian": "Язык",
        "japanese": "言語",
        "chinese": "语言",
        "hindi": "भाषा",
        "arabic": "اللغة"
    },
    "target_age_group_label": {
        "english": "Target Age Group",
        "spanish": "Grupo de Edad Objetivo",
        "french": "Groupe d'Âge Cible",
        "german": "Zielgruppe nach Alter",
        "italian": "Gruppo di Età Target",
        "portuguese": "Faixa Etária Alvo",
        "russian": "Целевая возрастная группа",
        "japanese": "ターゲット年齢層",
        "chinese": "目标年龄组",
        "hindi": "लक्षित आयु समूह",
        "arabic": "الفئة العمرية المستهدفة"
    },
    "save_story_settings_button": {
        "english": "Save Story Settings",
        "spanish": "Guardar Configuración de Historia",
        "french": "Enregistrer les Paramètres de l'Histoire",
        "german": "Story-Einstellungen speichern",
        "italian": "Salva Impostazioni Storia",
        "portuguese": "Salvar Configurações da História",
        "russian": "Сохранить настройки истории",
        "japanese": "ストーリー設定を保存",
        "chinese": "保存故事设置",
        "hindi": "कहानी सेटिंग्स सहेजें",
        "arabic": "حفظ إعدادات القصة"
    },
    "story_saved_success": {
        "english": "Story setup saved successfully!",
        "spanish": "¡Configuración de historia guardada con éxito!",
        "french": "Configuration de l'histoire enregistrée avec succès !",
        "german": "Story-Einrichtung erfolgreich gespeichert!",
        "italian": "Configurazione della storia salvata con successo!",
        "portuguese": "Configuração da história salva com sucesso!",
        "russian": "Настройка истории успешно сохранена!",
        "japanese": "ストーリー設定が正常に保存されました！",
        "chinese": "故事设置保存成功！",
        "hindi": "कहानी सेटअप सफलतापूर्वक सहेजा गया!",
        "arabic": "تم حفظ إعداد القصة بنجاح!"
    },
    "writing_guidelines_header": {
        "english": "Writing Guidelines for Target Audience",
        "spanish": "Pautas de Escritura para el Público Objetivo",
        "french": "Directives d'Écriture pour le Public Cible",
        "german": "Schreibrichtlinien für die Zielgruppe",
        "italian": "Linee Guida di Scrittura per il Pubblico Target",
        "portuguese": "Diretrizes de Escrita para o Público-Alvo",
        "russian": "Рекомендации по написанию для целевой аудитории",
        "japanese": "ターゲットオーディエンスの執筆ガイドライン",
        "chinese": "目标受众写作指南",
        "hindi": "लक्षित दर्शकों के लिए लेखन दिशानिर्देश",
        "arabic": "إرشادات الكتابة للجمهور المستهدف"
    },
    
    # Common terms
    "vocabulary_level": {
        "english": "Vocabulary Level",
        "spanish": "Nivel de Vocabulario",
        "french": "Niveau de Vocabulaire",
        "german": "Vokabelniveau",
        "italian": "Livello di Vocabolario",
        "portuguese": "Nível de Vocabulário",
        "russian": "Уровень словарного запаса",
        "japanese": "語彙レベル",
        "chinese": "词汇水平",
        "hindi": "शब्दावली स्तर",
        "arabic": "مستوى المفردات"
    },
    "sentence_structure": {
        "english": "Sentence Structure",
        "spanish": "Estructura de Oraciones",
        "french": "Structure des Phrases",
        "german": "Satzstruktur",
        "italian": "Struttura della Frase",
        "portuguese": "Estrutura de Frases",
        "russian": "Структура предложений",
        "japanese": "文章構造",
        "chinese": "句子结构",
        "hindi": "वाक्य संरचना",
        "arabic": "بنية الجملة"
    },
    "thematic_elements": {
        "english": "Thematic Elements",
        "spanish": "Elementos Temáticos",
        "french": "Éléments Thématiques",
        "german": "Thematische Elemente",
        "italian": "Elementi Tematici",
        "portuguese": "Elementos Temáticos",
        "russian": "Тематические элементы",
        "japanese": "テーマ要素",
        "chinese": "主题元素",
        "hindi": "थीमेटिक तत्व",
        "arabic": "العناصر الموضوعية"
    },
    "content_boundaries": {
        "english": "Content Boundaries",
        "spanish": "Límites de Contenido",
        "french": "Limites de Contenu",
        "german": "Inhaltliche Grenzen",
        "italian": "Limiti di Contenuto",
        "portuguese": "Limites de Conteúdo",
        "russian": "Границы содержания",
        "japanese": "コンテンツの境界",
        "chinese": "内容边界",
        "hindi": "सामग्री सीमाएँ",
        "arabic": "حدود المحتوى"
    },
    "narrative_style": {
        "english": "Narrative Style",
        "spanish": "Estilo Narrativo",
        "french": "Style Narratif",
        "german": "Erzählstil",
        "italian": "Stile Narrativo",
        "portuguese": "Estilo Narrativo",
        "russian": "Стиль повествования",
        "japanese": "ナラティブスタイル",
        "chinese": "叙事风格",
        "hindi": "कथात्मक शैली",
        "arabic": "أسلوب السرد"
    },
    # Add these entries to your existing TRANSLATIONS dictionary
"session_management": {
    "english": "Session Management",
    "spanish": "Gestión de Sesión",
    "french": "Gestion de Session",
    "german": "Sitzungsverwaltung",
    "italian": "Gestione Sessione",
    "portuguese": "Gerenciamento de Sessão",
    "russian": "Управление сессией",
    "japanese": "セッション管理",
    "chinese": "会话管理",
    "hindi": "सत्र प्रबंधन",
    "arabic": "إدارة الجلسة"
},
"save_button": {
    "english": "Save",
    "spanish": "Guardar",
    "french": "Sauvegarder",
    "german": "Speichern",
    "italian": "Salva",
    "portuguese": "Salvar",
    "russian": "Сохранить",
    "japanese": "保存",
    "chinese": "保存",
    "hindi": "सहेजें",
    "arabic": "حفظ"
},
"load_button": {
    "english": "Load",
    "spanish": "Cargar",
    "french": "Charger",
    "german": "Laden",
    "italian": "Carica",
    "portuguese": "Carregar",
    "russian": "Загрузить",
    "japanese": "読み込み",
    "chinese": "加载",
    "hindi": "लोड",
    "arabic": "تحميل"
},
"refresh_warning": {
    "english": "Important: Streamlit sessions clear when you refresh. Use the Save/Load buttons to preserve your work.",
    "spanish": "Importante: Las sesiones de Streamlit se borran al actualizar. Use los botones Guardar/Cargar para conservar su trabajo.",
    "french": "Important: Les sessions Streamlit s'effacent lors de l'actualisation. Utilisez les boutons Sauvegarder/Charger pour préserver votre travail.",
    "german": "Wichtig: Streamlit-Sitzungen werden beim Aktualisieren gelöscht. Verwenden Sie die Speichern/Laden-Schaltflächen, um Ihre Arbeit zu erhalten.",
    "italian": "Importante: le sessioni Streamlit si cancellano quando si aggiorna. Usa i pulsanti Salva/Carica per preservare il tuo lavoro.",
    "portuguese": "Importante: as sessões do Streamlit são apagadas ao atualizar. Use os botões Salvar/Carregar para preservar seu trabalho.",
    "russian": "Важно: сессии Streamlit очищаются при обновлении. Используйте кнопки Сохранить/Загрузить, чтобы сохранить вашу работу.",
    "japanese": "重要：Streamlitセッションは更新時にクリアされます。作業を保存するには保存/読み込みボタンを使用してください。",
    "chinese": "重要提示：刷新时Streamlit会话将被清除。使用保存/加载按钮来保存您的工作。",
    "hindi": "महत्वपूर्ण: रीफ्रेश करने पर Streamlit सत्र साफ हो जाते हैं। अपने काम को संरक्षित करने के लिए सहेजें/लोड बटन का उपयोग करें।",
    "arabic": "مهم: تمسح جلسات Streamlit عند التحديث. استخدم أزرار الحفظ/التحميل للحفاظ على عملك."
}
}

def get_translations(language="english"):
    """
    Get the translations for the specified language.
    
    Args:
        language (str): The language to get translations for. Defaults to "english".
        
    Returns:
        dict: A dictionary of UI text translations for the specified language.
    """
    # If invalid language is provided, default to English
    if language not in AVAILABLE_LANGUAGES:
        language = "english"
    
    # Construct a dictionary with all translation keys
    translations = {}
    for key, trans_dict in TRANSLATIONS.items():
        translations[key] = trans_dict.get(language, trans_dict["english"])
    
    return translations