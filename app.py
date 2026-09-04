def generate_magic(label: str, spell: str, source: str):
    with st.spinner("Casting AI magic from the detected gesture..."):
     st.session_state.spell_text = generate_spell_text(label, spell, source)
     img, err = generate_spell_image(build_image_prompt(spell, label, source))
     if img:
         st.session_state.spell_image = img
     else:
        st.session_state.spell_image = None
        st.error(err or "Could not generate the spell image.")

def prediction_panel(image: Image.Image, source: str):
    st.session_state.input_source = source
    st.image(image, caption="Gesture image", use_container_width=True)
    st.markdown(f'<div class="pill">Source: {source.title()}</div>',
unsafe_allow_html=True)
  try:
     model, labels = get_model()
     pred = predict_gesture_from_image(model, labels, image)
     pred["label"] = normalize(pred["label"])
     for item in pred["top_predictions"]:
         item["label"] = normalize(item["label"])
     st.session_state.prediction = pred
     spell = get_spell_name(pred["label"])
     st.session_state.spell_name = spell 
     st.success(f"Detached gesture: **{pred['label']}**")
     st.progress(float(pred["confidence"]), text=f"Confidence:
{pred['confidence']:.1%}")
        c1, c2 = st.columns(2)
        c1.markdown(f'<div class="card"><b>Detected</b><br><br>{pred["label"]}
</div>', unsafe_allow_html=True)
        c2.markdown(f'<div class="card"><b>Spell</b><br><br>{spell}</div>',
unsafe_allow_html=True)
        key = f"{source}:{pred['label']}:{pred['confidence']:.4f}"
        if st.session_state.last_key != key:
            if st.button("🪄 Generate AI Magic", use_container_width=True):
                generate_magic(pred["label"], spell, source)
                st.session_state.last_key = key
        except Exception as e:
           st.error(f"Model error: {e}\n\nTip: use python 3.10/3.11 and 
tensorflow==2.15.0")

def show_output(): 
    st.markdown('<div class="panel">',
unsafe_allow_html=True)
    st.subheader("🪄 AI Magic Output")
    if st.session_state.spell_name:
        st.markdown(f'<div class="spell-box"><b>Spell
Name</b><br><br>{st.session_state.spell_name}</div>',
unsafe_allow_html=True)
   if st.session_state.spell_image is not None:
       st.image(st.session_state.spell_image, caption="AI-
generated spell scene", use_container_width=True)
    elif not st.session_state.spell_name:
      st.info("Detect a gesture and click Generate AI Magic
to see the output.")
    st.markdown('</div>', unsafe_allow_html=True)

def main():
     render_styles()
     st.markdown(f"""
        <div class="hero">
            <h1 style="margin:0 0 6px 0;">{config.APP_ICON}
{config.APP_TITLE}</h1>
           <p style="margin:0;">Detect a hand gesture, then 
let AI generate a spell narration and a magical scene image. 
</p>
     </div>""", unsafe_allow_html=True)
  left, right = st.columns([1, 1], gap="large")
  with left:
      st.markdown('<div class="panel">',
unsafe_allow_html=True)
        st.subheader("📷 Input")
        tabs = st.tabs(["Webcam Capture", "Upload Image"])
        with tabs[0]:
            cam = st.camera_input("Capture gesture from 
webcam", help=config.CAMERA_HELP)
           if cam:
           
prediction_panel(Image.open(cam).convert("RGB"), "webcam")
            else:
                st.info("Take a photo with your webcam to 
detect a gesture.")
        with tabs[1]:
            up = st.file_uploader("Upload a gesture image",
type=["png", "jpg", "jpeg"])
            if up:
            
prediction_panel(Image.open(up).convert("RGB"), "upload")
            else:
                st.info("Upload a hand gesture image to 
detect a gesture.")
        st.markdown('</div>', unsafe_allow_html=True)
    with right:
        show_output()
def reset_magic_session():
    for k, v in _DEFAULTS.items():
        st.session_state[k] = v

def generate_magic_bundle():
    if not st.session_state.prediction:
        st.warning("Capture or upload an image first.")
        return
    label = st.session_state.prediction["label"]
    spell = st.session_state.spell_name
    st.session_state.spell_prompt = build_hidden_prompt(label, spell,
st.session_state.input_source)
    with st.spinner("Casting AI magic from the detected gesture..."):
        st.session_state.spell_text = generate_magic_response(label, spell,
f"This spell came from a {st.session_state.input_source} hand-gesture image.")
        img, err = generate_magic_visual(st.session_state.spell_prompt)
        if img:
            st.session_state.spell_scene_image = img 
            st.session_state.spell_card_image = create_spell_card(spell, label,
st.session_state.spell_text, img)
       else:
           st.session_state.spell_scene_image =
st.session_state.spell_card_image = None 
           st.error(err or "Could not generate the spell image.")
        st.session_state.spell_log = ([{"gesture": label, "spell": spell, "text": st.session_state.spell_text, "source": st.session_state.input_soruce}]
                                          + st.session_spell_log)
[:config.MAX_SPELL_LOG]

def show_hud():
    c1, c2, c3, c4 = st.columns(4)
    gesture = st.session_state.prediction["label"] if st.session_state.prediction 
else "Waiting"
     spell = st.session_state.spell_name or "No Spell Yet"
     for co1, label, val in [
         (c1, "Supported Gestures", "Palm . Peace . Pointer . Thumbs Up"),
         (c2, "Detected Gesture",gesture),
         (c3, "Active Spell", spell),
         (c4, "Spell Log", len(st.session_state.spell_log)),
     ]:
         co1.markdown(f'<div class="status-card"><b>{label}</b><br>{val}</div>', unsafe_allow_html=True)

         def prediction_panel(current_image: Image.Image, source_name: str):
             st.session_state.captured_image = current_image
             st.session_state.input_source = source_name
             st.image(current_image, caption="Gesture image used for magic casting", use_container_width=True)
                st.markdown(f'<div class="source-pill">Input source: {source_name.title()} </div>', unsafe_allow_html=True) 
                  try:
                     model, labels = get_model_and_labels()
                     pred = predict_gesture_from_image(model, labels,
                current_image)
                       pred["label"] = normalize_label(pred["label"])
                       for item in pred["top_predictions"]:
                           item["label"] = normalize_label(item["label"])
                       st.session_state.prediction = pred
                       spell = get_spell_name_for_gesture(pred["label"],
                st.session_state.prediction = pred
                spell = get_spell_name_for_gesture(pred["label"],
                st.session_state.gesture_mapping)
                   st.session_state.spell_name = spell
                   st.success(f"Detected gesture: {pred['label']}")
                   st.progress(float(pred["confidence"]),
                text=f"Confidence: {pred['confidence']:.1%}")
                        c1, c2 = st.columns(2)
                        c1.markdown(f'<div class="detect-card"><b>Detected</b>
                <br>{pred["label"]}</div>', unsafe_allow_html=True)
                        c2.markdown(f'<div class="detect-card"><b>Mapped
                Spell</b><br>{spell}</div>', unsafe_allow_html=True)
                      with st.expander("See all prediction scores"):
                           for item in pred["top_predictions"]:
                               st.progress(float(item["confidence"]), text=f"
                {item['label']} - {item['confidence']:.1%}")
                     key = f"{source_name}:{pred['label']}:
                {pred['confidence']:.4f}"
                        if st.session_state.last_generated_key != key:
                            if st.button("Generate Magic From This Image ✨", use_container_width=True);
                                generate_magic_bundle()
                                st.session_state.last_generated_key = key
                    except Exception as e: 
                        st.error(f"Could not load or run the local model: {e}\n\nTip: use Python 3.10/3.11 and tensorflow==2.15.0 for Teachable Machine .h5 models.")
                


        