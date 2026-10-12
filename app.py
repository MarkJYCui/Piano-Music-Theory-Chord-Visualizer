import pandas as pd
import streamlit as st
import itertools

# MUST be the first Streamlit command executed
st.set_page_config(page_title="Piano Theory Visualizer", layout="wide")

# --- Custom Minimalist Piano Icon ---
piano_icon = """
<svg width="38" height="38" viewBox="0 0 100 100" fill="currentColor" xmlns="http://www.w3.org/2000/svg" style="vertical-align: -10px; margin-right: 8px;">
  <rect x="10" y="20" width="80" height="60" rx="4" fill="none" stroke="currentColor" stroke-width="4"/>
  <!-- White keys -->
  <line x1="26" y1="20" x2="26" y2="80" stroke="currentColor" stroke-width="3"/>
  <line x1="42" y1="20" x2="42" y2="80" stroke="currentColor" stroke-width="3"/>
  <line x1="58" y1="20" x2="58" y2="80" stroke="currentColor" stroke-width="3"/>
  <line x1="74" y1="20" x2="74" y2="80" stroke="currentColor" stroke-width="3"/>
  <!-- Black keys -->
  <rect x="18" y="20" width="12" height="35" fill="currentColor" />
  <rect x="34" y="20" width="12" height="35" fill="currentColor" />
  <rect x="66" y="20" width="12" height="35" fill="currentColor" />
</svg>
""".replace('\n', '')

# --- Translation Dictionary ---
texts = {
    'en': {
        'app_title': "Piano Music Theory & Chord Visualizer",
        'about': "About This App",
        'about_desc': "Welcome to the **Piano Music Theory & Chord Visualizer**! \n\nThis tool is designed to help pianists and producers explore scales, map out the keyboard across octaves, and dynamically generate chord voicings and inversions.",
        'created_by': "**Adapted by:** AI (Gemini)",
        'co_created_by': "**Original framework by:** Mark Cui",
        'powered_by': (
            "**Powered by:**\n"
            "- 🐍 Python (Core Logic)\n"
            "- 🐼 Pandas (Data Grids)\n"
            "- 🎈 Streamlit (UI Framework)\n"
            "- :streamlit: Streamlit Community Cloud (Hosting)"
        ),
        'display_mode': "Display Mode:",
        'notes': "Notes (C, E, G)",
        'intervals': "Intervals (1, 3, 5)",
        'choose_root': "Choose a Root Note / Key:",
        'choose_scale': "Choose a Scale / Mode Type:",
        'show_sevenths': "Show 7th Chords",
        'prac_seventh': "Practical 7th (Replace Major vii° with V7)",
        'inversion_explorer': "Enable Inversion Explorer",
        'inversion_help': "Explore Root Position, 1st Inversion, and 2nd Inversion voicings on the keyboard.",
        'inversion_expander': "Explore Inversions for {0} ⮟",
        'highlight_degree': "Highlight Keyboard for Chord Degree:",
        'results_for': "Results for",
        'highlighting_degree': "Highlighting Degree",
        'practical': "Practical",
        'scale_notes': "Scale Notes:",
        'octave_range': "Keyboard Octave Range:",
        'full_keyboard': "1. Full Keyboard Map",
        'diatonic_chords': "2. Diatonic Chords & Progressions",
        'progression': "Select Progression:",
        'prog_all': "All 7 Diatonic Chords",
        'prog_pop': "Pop / Modern (I - V - vi - IV)",
        'prog_rock': "Classic Rock (I - IV - V)",
        'prog_jazz': "Jazz / R&B (ii - V - I)",
        'degree': "Degree",
        'interval_clarification_title': "💡 Key vs. Chord Root Interval Clarification",
        'interval_clarification_body': (
            "• **Full Keyboard Map:** Intervals are displayed relative to the **Key Root ({key})** "
            "(e.g., in C Major: C=1, D=2, E=3, F=4, G=5, A=6, B=7).\n"
            "• **Chord Voicings & Inversions:** Intervals are displayed relative to each **Chord's Root** "
            "(e.g., for a D minor chord, D=1, F=b3, A=5)."
        ),
        'scale_types': {
            'Major': 'Major (Ionian)', 
            'Natural Minor': 'Natural Minor (Aeolian)',
            'Harmonic Minor': 'Harmonic Minor',
            'Melodic Minor': 'Melodic Minor',
            'Dorian': 'Dorian Mode',
            'Phrygian': 'Phrygian Mode',
            'Lydian': 'Lydian Mode',
            'Mixolydian': 'Mixolydian Mode',
            'Locrian': 'Locrian Mode',
            'Major Pentatonic': 'Major Pentatonic',
            'Minor Pentatonic': 'Minor Pentatonic'
        }
    },
    'zh': {
        'app_title': "钢琴乐理与和弦可视化工具",
        'about': "关于本应用",
        'about_desc': "欢迎使用**钢琴乐理与和弦可视化工具**！\n\n本工具旨在帮助键盘手和制作人探索音阶，映射键盘音区，并动态生成和弦指法与转位。",
        'created_by': "**改编者：** AI (Gemini)",
        'co_created_by': "**原框架作者：** Mark Cui",
        'powered_by': (
            "**技术支持：**\n"
            "- 🐍 Python (核心逻辑)\n"
            "- 🐼 Pandas (数据网格)\n"
            "- 🎈 Streamlit (界面框架)\n"
            "- :streamlit: Streamlit Community Cloud (云端托管与部署)"
        ),
        'display_mode': "显示模式 (Display Mode):",
        'notes': "音名 (Notes)",
        'intervals': "级数/音程 (Intervals)",
        'choose_root': "选择根音 / 调 (Root Note / Key):",
        'choose_scale': "选择音阶/调式类型 (Scale Type):",
        'show_sevenths': "显示七和弦",
        'prac_seventh': "实用七级 (大调中将 vii° 替换为 V7)",
        'inversion_explorer': "启用和弦转位探索",
        'inversion_help': "在键盘上探索原位、第一转位和第二转位和弦。",
        'inversion_expander': "探索 {0} 的所有转位 ⮟",
        'highlight_degree': "在键盘上高亮显示和弦级数 (Chord Degree):",
        'results_for': "分析结果：",
        'highlighting_degree': "当前高亮级数",
        'practical': "实用替换",
        'scale_notes': "音阶包含音 (Scale Notes):",
        'octave_range': "键盘音区范围 (Octave Range):",
        'full_keyboard': "1. 完整键盘音名分布图",
        'diatonic_chords': "2. 顺阶和弦与常见进行",
        'progression': "选择和弦进行 (Select Progression):",
        'prog_all': "所有7个顺阶和弦 (I - VII)",
        'prog_pop': "流行乐 (I - V - vi - IV)",
        'prog_rock': "经典摇滚 (I - IV - V)",
        'prog_jazz': "爵士/R&B (ii - V - I)",
        'degree': "级数",
        'interval_clarification_title': "💡 调性根音 vs 和弦根音音程说明",
        'interval_clarification_body': (
            "• **完整键盘分布图：** 音程相对于**调性根音 (Key Root: {key})** 计算"
            "（例如在 C 大调中：C=1, D=2, E=3, F=4, G=5, A=6, B=7）。\n"
            "• **和弦指法与转位：** 音程相对于**该和弦自身的根音 (Chord Root)** 计算"
            "（例如在 D minor (ii) 和弦中：D=1, F=b3, A=5）。"
        ),
        'scale_types': {
            'Major': '大调 (Major / Ionian)', 
            'Natural Minor': '自然小调 (Natural Minor / Aeolian)',
            'Harmonic Minor': '和声小调 (Harmonic Minor)',
            'Melodic Minor': '旋律小调 (Melodic Minor)',
            'Dorian': '多利亚调式 (Dorian)',
            'Phrygian': '弗里吉亚调式 (Phrygian)',
            'Lydian': '利底亚调式 (Lydian)',
            'Mixolydian': '混合利底亚调式 (Mixolydian)',
            'Locrian': '洛克里亚调式 (Locrian)',
            'Major Pentatonic': '大调五声音阶 (Major Pentatonic)',
            'Minor Pentatonic': '小调五声音阶 (Minor Pentatonic)'
        }
    },
    'fr': {
        'app_title': "Visualiseur de Théorie Musicale et Piano",
        'about': "À Propos de cette Application",
        'about_desc': "Bienvenue dans le **Visualiseur de Théorie Musicale pour Piano** ! \n\nCet outil est conçu pour aider les pianistes à explorer les gammes, à cartographier le clavier sur plusieurs octaves et à générer dynamiquement des renversements d'accords.",
        'created_by': "**Adapté par :** IA (Gemini)",
        'co_created_by': "**Cadre original par :** Mark Cui",
        'powered_by': (
            "**Propulsé par :**\n"
            "- 🐍 Python (Logique de base)\n"
            "- 🐼 Pandas (Grilles de données)\n"
            "- 🎈 Streamlit (Interface utilisateur)\n"
            "- :streamlit: Streamlit Community Cloud (Hébergement)"
        ),
        'display_mode': "Mode d'affichage :",
        'notes': "Notes (Do, Mi, Sol)",
        'intervals': "Intervalles (1, 3, 5)",
        'choose_root': "Choisissez une Fondamentale / Tonalité :",
        'choose_scale': "Choisissez un Type de Gamme / Mode :",
        'show_sevenths': "Afficher les Accords de 7ème",
        'prac_seventh': "7ème Pratique (Remplace vii° Majeur par V7)",
        'inversion_explorer': "Activer l'Explorateur de Renversements",
        'inversion_help': "Explorez l'état fondamental, le 1er et le 2ème renversement sur le clavier.",
        'inversion_expander': "Explorer les Renversements pour {0} ⮟",
        'highlight_degree': "Mettre en évidence le Degré de l'Accord sur le clavier :",
        'results_for': "Résultats pour",
        'highlighting_degree': "Mise en évidence du Degré",
        'practical': "Pratique",
        'scale_notes': "Notes de la Gamme :",
        'octave_range': "Plage d'Octaves du Clavier :",
        'full_keyboard': "1. Carte Complète du Clavier",
        'diatonic_chords': "2. Accords Diatoniques et Progressions",
        'progression': "Sélectionnez une Progression :",
        'prog_all': "Les 7 Accords Diatoniques",
        'prog_pop': "Pop / Moderne (I - V - vi - IV)",
        'prog_rock': "Rock Classique (I - IV - V)",
        'prog_jazz': "Jazz / R&B (ii - V - I)",
        'degree': "Degré",
        'interval_clarification_title': "💡 Précision sur les Intervalles",
        'interval_clarification_body': (
            "• **Carte Complète du Clavier :** Les intervalles sont affichés par rapport à la **Fondamentale de la Tonalité ({key})**.\n"
            "• **Voicings et Renversements :** Les intervalles sont affichés par rapport à la **Fondamentale de chaque accord**."
        ),
        'scale_types': {
            'Major': 'Majeure (Ionien)', 
            'Natural Minor': 'Mineure Naturelle (Éolien)',
            'Harmonic Minor': 'Mineure Harmonique',
            'Melodic Minor': 'Mineure Mélodique',
            'Dorian': 'Mode Dorien',
            'Phrygian': 'Mode Phrygien',
            'Lydian': 'Mode Lydien',
            'Mixolydian': 'Mode Mixolydien',
            'Locrian': 'Mode Locrien',
            'Major Pentatonic': 'Pentatonique Majeure',
            'Minor Pentatonic': 'Pentatonique Mineure'
        }
    }
}

interval_names = {
    0: '1', 1: 'b2', 2: '2', 3: 'b3', 4: '3', 
    5: '4', 6: 'b5', 7: '5', 8: 'b6', 9: '6', 
    10: 'b7', 11: '7'
}

# --- 1. Music Theory Logic ---

chromatic_sharps = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
chromatic_flats = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
piano_columns = ['C', 'C#/Db', 'D', 'D#/Eb', 'E', 'F', 'F#/Gb', 'G', 'G#/Ab', 'A', 'A#/Bb', 'B']

def get_chromatic_list(root_note, scale_type='Major'):
    major_flat_keys = ['F', 'Bb', 'Eb', 'Ab', 'Db', 'Gb', 'Cb']
    minor_flat_keys = ['D', 'G', 'C', 'F', 'Bb', 'Eb', 'Ab']

    if 'Minor' in scale_type and root_note in minor_flat_keys:
        return chromatic_flats
    elif 'Major' in scale_type and root_note in major_flat_keys:
        return chromatic_flats
    elif scale_type in ['Dorian', 'Phrygian', 'Locrian'] and root_note in minor_flat_keys:
        return chromatic_flats
    elif scale_type in ['Lydian', 'Mixolydian'] and root_note in major_flat_keys:
        return chromatic_flats
    else:
        return chromatic_sharps

def get_pitch(note_str):
    if not note_str: return -1
    base = note_str[0]
    val = {'C':0, 'D':2, 'E':4, 'F':5, 'G':7, 'A':9, 'B':11}.get(base, 0)
    for acc in note_str[1:]:
        if acc == '#': val += 1
        elif acc == 'x': val += 2 
        elif acc == 'b': val -= 1
    return val % 12

def enforce_diatonic_spelling(scale, root_note):
    if len(scale) != 7:
        return scale
        
    base_letters = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
    start_idx = base_letters.index(root_note[0])
    expected_letters = [base_letters[(start_idx + i) % 7] for i in range(7)]
    
    corrected_scale = []
    for i, note in enumerate(scale):
        actual_pitch = get_pitch(note)
        exp_letter = expected_letters[i]
        exp_pitch = get_pitch(exp_letter)
        
        diff = (actual_pitch - exp_pitch) % 12
        
        if diff == 0:
            corrected_scale.append(exp_letter)
        elif diff == 1:
            corrected_scale.append(exp_letter + '#')
        elif diff == 2:
            corrected_scale.append(exp_letter + 'x')
        elif diff == 11:
            corrected_scale.append(exp_letter + 'b')
        elif diff == 10:
            corrected_scale.append(exp_letter + 'bb')
        else:
            corrected_scale.append(note)
            
    return corrected_scale

scale_intervals = {
    'Major': [0, 2, 4, 5, 7, 9, 11],
    'Natural Minor': [0, 2, 3, 5, 7, 8, 10],
    'Harmonic Minor': [0, 2, 3, 5, 7, 8, 11],
    'Melodic Minor': [0, 2, 3, 5, 7, 9, 11],
    'Dorian': [0, 2, 3, 5, 7, 9, 10],
    'Phrygian': [0, 1, 3, 5, 7, 8, 10],
    'Lydian': [0, 2, 4, 6, 7, 9, 11],
    'Mixolydian': [0, 2, 4, 5, 7, 9, 10],
    'Locrian': [0, 1, 3, 5, 6, 8, 10],
    'Major Pentatonic': [0, 2, 4, 7, 9],
    'Minor Pentatonic': [0, 3, 5, 7, 10],
}

def get_scale(root_note, scale_type):
    chromatic = get_chromatic_list(root_note, scale_type)
    start_index = get_pitch(root_note)
    intervals = scale_intervals[scale_type]
    raw_scale = [chromatic[(start_index + interval) % 12] for interval in intervals]
    
    if len(intervals) == 7:
        return enforce_diatonic_spelling(raw_scale, root_note)
    return raw_scale

def get_chord_from_scale(scale, degree, include_seventh=False):
    scale_length = len(scale)
    root_idx = (degree - 1) % scale_length
    third_idx = (root_idx + 2) % scale_length
    fifth_idx = (root_idx + 4) % scale_length
    
    chord = [scale[root_idx], scale[third_idx], scale[fifth_idx]]
    
    if include_seventh:
        seventh_idx = (root_idx + 6) % scale_length
        chord.append(scale[seventh_idx])
        
    return chord

def get_spelled_note_if_in_chord(pitch, chord_notes):
    for cn in chord_notes:
        if get_pitch(cn) == pitch:
            return cn
    return None

def get_chord_name(chord_notes, root_key, scale_type='Major'):
    root_pitch = get_pitch(chord_notes[0])
    third_pitch = get_pitch(chord_notes[1])
    fifth_pitch = get_pitch(chord_notes[2])

    third_dist = (third_pitch - root_pitch) % 12
    fifth_dist = (fifth_pitch - root_pitch) % 12
    
    if len(chord_notes) == 4:
        seventh_pitch = get_pitch(chord_notes[3])
        seventh_dist = (seventh_pitch - root_pitch) % 12
        
        if third_dist == 4 and fifth_dist == 7 and seventh_dist == 11:
            return f"{chord_notes[0]} maj7"
        elif third_dist == 4 and fifth_dist == 7 and seventh_dist == 10:
            return f"{chord_notes[0]} 7"
        elif third_dist == 3 and fifth_dist == 7 and seventh_dist == 11:
            return f"{chord_notes[0]} m(maj7)" 
        elif third_dist == 3 and fifth_dist == 7 and seventh_dist == 10:
            return f"{chord_notes[0]} m7"
        elif third_dist == 3 and fifth_dist == 6 and seventh_dist == 10:
            return f"{chord_notes[0]} m7b5"
        elif third_dist == 3 and fifth_dist == 6 and seventh_dist == 9:
            return f"{chord_notes[0]} dim7"
        elif third_dist == 4 and fifth_dist == 8 and seventh_dist == 11:
            return f"{chord_notes[0]} maj7#5" 
        elif third_dist == 4 and fifth_dist == 8 and seventh_dist == 10:
            return f"{chord_notes[0]} aug7"   

    if third_dist == 4 and fifth_dist == 7:
        return f"{chord_notes[0]} Major"
    elif third_dist == 3 and fifth_dist == 7:
        return f"{chord_notes[0]} minor"
    elif third_dist == 3 and fifth_dist == 6:
        return f"{chord_notes[0]} dim"
    elif third_dist == 4 and fifth_dist == 8:
        return f"{chord_notes[0]} aug"
        
    return f"{chord_notes[0]}"

# --- PIANO KEYBOARD & INVERSION LOGIC ---

def get_inversions(chord_notes):
    inversions = {}
    inversions['Root Position'] = chord_notes
    inversions['1st Inversion'] = chord_notes[1:] + [chord_notes[0]]
    inversions['2nd Inversion'] = chord_notes[2:] + chord_notes[:2]
    if len(chord_notes) == 4:
        inversions['3rd Inversion'] = chord_notes[3:] + chord_notes[:3]
    return inversions

def get_keyboard_dataframe(target_notes, reference_note=None, display_mode='Notes', num_octaves=2, start_octave=3, specific_voicing=None):
    grid = []
    row_labels = []
    ref_pitch = get_pitch(reference_note) if reference_note else get_pitch(target_notes[0])
    
    if specific_voicing:
        active_absolute_pitches = []
        current_octave = start_octave
        last_pitch = -1
        for note in specific_voicing:
            p = get_pitch(note)
            if p < last_pitch:
                current_octave += 1
            active_absolute_pitches.append((p, current_octave))
            last_pitch = p

    for oct in range(start_octave + num_octaves - 1, start_octave - 1, -1):
        row_labels.append(f"Octave {oct}")
        row_data = []
        for p in range(12):
            spelled_note = get_spelled_note_if_in_chord(p, target_notes)
            
            is_active = False
            if specific_voicing:
                is_active = (p, oct) in active_absolute_pitches
            else:
                is_active = spelled_note is not None

            if is_active and spelled_note:
                if display_mode == 'Intervals':
                    display_val = interval_names[(p - ref_pitch) % 12]
                else:
                    display_val = spelled_note
                    
                marker = "○" if p == ref_pitch else "●"
                row_data.append(f"{marker} {display_val}")
            else:
                row_data.append("—")
        grid.append(row_data)

    return pd.DataFrame(grid, index=row_labels, columns=piano_columns)

def style_keyboard_cells(val):
    if not isinstance(val, str):
        return ""
    if '●' in val:
        return "background-color: #1f77b4; color: white; font-weight: bold; text-align: center; border-radius: 4px;"
    elif '○' in val:
        return "background-color: #2ca02c; color: white; font-weight: bold; text-align: center; border-radius: 4px;"
    elif val != '—' and val != "":
        return "background-color: #9467bd; color: white; font-weight: bold; text-align: center; border-radius: 4px;"
    else:
        return "color: #aaaaaa; text-align: center;"

def apply_styler(df):
    if hasattr(df.style, 'map'):
        return df.style.map(style_keyboard_cells)
    else:
        return df.style.applymap(style_keyboard_cells)

# --- 2. User Interface ---

lang_choice = st.sidebar.selectbox("Language / 语言 / Langue", ["English", "中文", "Français"])
if lang_choice == "English":
    lang = 'en'
elif lang_choice == "中文":
    lang = 'zh'
else:
    lang = 'fr'

t = texts[lang]

with st.sidebar:
    st.markdown(f"# {piano_icon} {t['about']}", unsafe_allow_html=True)
    st.markdown(t['about_desc'])
    
    st.markdown("---")
    st.markdown(t['created_by'])
    st.markdown(t['co_created_by'])
    st.write("") 
    st.markdown(t['powered_by'], unsafe_allow_html=True) 

st.markdown(f"# {piano_icon} {t['app_title']}", unsafe_allow_html=True)

all_keys = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'Gb', 'Db', 'C#', 'Ab', 'Eb', 'Bb', 'F']
selected_root = st.selectbox(t['choose_root'], all_keys)

selected_scale_type = st.selectbox(
    t['choose_scale'], 
    list(scale_intervals.keys()), 
    format_func=lambda x: t['scale_types'][x]
)

st.markdown("---")
display_mode_choice = st.radio(
    t['display_mode'],
    ["Notes", "Intervals"],
    format_func=lambda x: t['notes'] if x == "Notes" else t['intervals'],
    horizontal=True
)

if display_mode_choice == "Intervals":
    st.info(t['interval_clarification_body'].format(key=selected_root), icon="ℹ️")

col1, col2, col3 = st.columns(3)
with col1:
    show_sevenths = st.checkbox(t['show_sevenths'], value=False)
with col2:
    use_practical_seventh = st.checkbox(t['prac_seventh'], value=False)
with col3:
    enable_inversions = st.checkbox(
        t['inversion_explorer'], 
        value=False, 
        help=t['inversion_help']
    )
    
num_octaves = st.slider(t['octave_range'], min_value=1, max_value=4, value=2)

scale = get_scale(selected_root, selected_scale_type)
is_seven_note = len(scale_intervals[selected_scale_type]) == 7

if is_seven_note:
    chord_degree = st.selectbox(t['highlight_degree'], [1, 2, 3, 4, 5, 6, 7])
    
    is_practical_selection = (chord_degree == 7 and use_practical_seventh and selected_scale_type == 'Major')
    
    if is_practical_selection:
        target_notes = get_chord_from_scale(scale, 5, include_seventh=True)
        chord_name = get_chord_name(target_notes, selected_root, selected_scale_type) + f" ({t['practical']} V7)"
    else:
        target_notes = get_chord_from_scale(scale, chord_degree, include_seventh=show_sevenths)
        chord_name = get_chord_name(target_notes, selected_root, selected_scale_type)
        
    st.subheader(f"{t['results_for']} {selected_root} {t['scale_types'][selected_scale_type]} ({t['highlighting_degree']} {chord_degree}: {chord_name})")
else:
    target_notes = scale
    st.subheader(f"{t['results_for']} {selected_root} {t['scale_types'][selected_scale_type]}")

st.write(f"**{t['scale_notes']}** {', '.join(scale)}")

# --- 3. Displays ---
st.subheader(t['full_keyboard'])

keyboard_df = get_keyboard_dataframe(
    target_notes, 
    reference_note=selected_root, 
    display_mode=display_mode_choice,
    num_octaves=num_octaves
)

styled_keyboard = apply_styler(keyboard_df)
st.dataframe(styled_keyboard, use_container_width=True)

if is_seven_note:
    st.subheader(t['diatonic_chords'])
    
    prog_options = {
        t['prog_all']: [1, 2, 3, 4, 5, 6, 7],
        t['prog_pop']: [1, 5, 6, 4],
        t['prog_rock']: [1, 4, 5],
        t['prog_jazz']: [2, 5, 1]
    }
    
    selected_progression = st.selectbox(t['progression'], list(prog_options.keys()))
    degrees_to_show = prog_options[selected_progression]
    
    if show_sevenths:
        scale_roman_numerals = {
            'Major': ["Imaj7", "ii7", "iii7", "IVmaj7", "V7", "vi7", "viiø7"],
            'Natural Minor': ["i7", "iiø7", "IIImaj7", "iv7", "v7", "VImaj7", "VII7"],
            'Harmonic Minor': ["i(maj7)", "iiø7", "IIImaj7#5", "iv7", "V7", "VImaj7", "vii°7"],
            'Melodic Minor': ["i(maj7)", "ii7", "IIImaj7#5", "IV7", "V7", "viø7", "viiø7"],
            'Dorian': ["i7", "ii7", "IIImaj7", "IV7", "v7", "viø7", "VIImaj7"],
            'Phrygian': ["i7", "IImaj7", "III7", "iv7", "vø7", "VImaj7", "vii7"],
            'Lydian': ["Imaj7", "II7", "iii7", "ivø7", "Vmaj7", "vi7", "vii7"],
            'Mixolydian': ["I7", "ii7", "iiiø7", "IVmaj7", "v7", "vi7", "VIImaj7"],
            'Locrian': ["iø7", "IImaj7", "iii7", "iv7", "Vmaj7", "VI7", "vii7"]
        }
    else:
        scale_roman_numerals = {
            'Major': ["I", "ii", "iii", "IV", "V", "vi", "vii°"],
            'Natural Minor': ["i", "ii°", "III", "iv", "v", "VI", "VII"],
            'Harmonic Minor': ["i", "ii°", "III+", "iv", "V", "VI", "vii°"],
            'Melodic Minor': ["i", "ii", "III+", "IV", "V", "vi°", "vii°"],
            'Dorian': ["i", "ii", "III", "IV", "v", "vi°", "VII"],
            'Phrygian': ["i", "II", "III", "iv", "v°", "VI", "vii"],
            'Lydian': ["I", "II", "iii", "iv°", "V", "vi", "vii"],
            'Mixolydian': ["I", "ii", "iii°", "IV", "v", "vi", "VII"],
            'Locrian': ["i°", "II", "iii", "iv", "V", "VI", "vii"]
        }
        
    roman_numerals = list(scale_roman_numerals.get(selected_scale_type, ["1", "2", "3", "4", "5", "6", "7"]))

    if use_practical_seventh and selected_scale_type == 'Major':
        roman_numerals[6] = f"V7 ({t['practical']})"

    # Render chords vertically to prevent horizontal scrolling
    for idx, degree in enumerate(degrees_to_show):
        is_loop_practical = (degree == 7 and use_practical_seventh and selected_scale_type == 'Major')
        
        if is_loop_practical:
            deg_notes = get_chord_from_scale(scale, 5, include_seventh=True)
            deg_name = get_chord_name(deg_notes, selected_root, selected_scale_type) + " (V7)"
        else:
            deg_notes = get_chord_from_scale(scale, degree, include_seventh=show_sevenths)
            deg_name = get_chord_name(deg_notes, selected_root, selected_scale_type)

        st.markdown(f"### **{t['degree']} {degree} ({roman_numerals[degree-1]})**")
        st.write(f"**{deg_name}**")
        st.caption(f"{deg_notes}")

        # Show default root position
        root_voicing_df = get_keyboard_dataframe(
            deg_notes, 
            reference_note=deg_notes[0], 
            display_mode=display_mode_choice,
            num_octaves=2,
            start_octave=3,
            specific_voicing=deg_notes
        )
        
        styled_voicing = apply_styler(root_voicing_df)
        st.dataframe(styled_voicing, use_container_width=True)
            
        if enable_inversions:
            inv_toggle_key = f"inv_toggle_{selected_progression}_{idx}"
            show_invs = st.checkbox(t['inversion_expander'].format(deg_name.split(' (')[0]), key=inv_toggle_key)
            
            if show_invs:
                inversions = get_inversions(deg_notes)
                for inv_name, inv_notes in inversions.items():
                    if inv_name == 'Root Position': 
                        continue 
                        
                    st.markdown(f"*{inv_name}*")
                    inv_df = get_keyboard_dataframe(
                        deg_notes, 
                        reference_note=deg_notes[0], 
                        display_mode=display_mode_choice,
                        num_octaves=2,
                        start_octave=3,
                        specific_voicing=inv_notes
                    )
                    st.dataframe(apply_styler(inv_df), use_container_width=True)
        st.markdown("---")
