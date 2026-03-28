const HOME_LABELS = {
  tagline:   {en:'Fun Education for Ages 4–6', hi:'मज़ेदार शिक्षा · आयु 4–6', gu:'મઝેદાર શિક્ષા · ઉંમર 4–6'},
  voiceBadge:{en:'With voice!', hi:'आवाज़ के साथ!', gu:'અવાજ સાથે!'},
  totalLbl:  {en:'stars earned', hi:'सितारे कमाए', gu:'સ્ટાર મેળવ્યા'},
  greeting:  {en:"Hello! What do you want to play?", hi:'नमस्ते! क्या खेलना है?', gu:'નમસ્તે! શું રમવું છે?'},
  footer:    {en:"Made with ❤️ for little learners · Keep trying!", hi:"छोटे सीखने वालों के लिए ❤️ · कोशिश करते रहो!", gu:"નાના શીખનારાઓ માટે ❤️ · પ્રયત્ન કરતા રહો!"},
  age4:      {en:'Age 4+', hi:'आयु 4+', gu:'ઉંમર 4+'},
  age5:      {en:'Age 5+', hi:'आयु 5+', gu:'ઉંમર 5+'},
  age56:     {en:'Age 5–6', hi:'आयु 5–6', gu:'ઉંમર 5–6'},
  catBrain:  {en:'Brain Games', hi:'दिमाग के खेल', gu:'દિમાગની રમત'},
  catCreate: {en:'Creative', hi:'क्रिएटिव', gu:'સર્જનાત્મક'},
  catWorld:  {en:'Real World', hi:'असली दुनिया', gu:'વાસ્તવિક દુનિયા'},
  catListen: {en:'Listen & Learn', hi:'सुनो और सीखो', gu:'સાંભળો અને શીખો'},
  catPhonics:{en:'Phonics & Reading', hi:'फोनिक्स और पढ़ाई', gu:'ફોનિક્સ અને વાંચન'},
  catSkills: {en:'Skill Builders', hi:'कौशल निर्माता', gu:'કૌશલ્ય નિર્માતા'},
};

function renderHomeLanguage() {
  const taglineEl = document.getElementById('hero-tagline');
  const voiceBadgeEl = document.getElementById('voice-badge-text');
  const totalStarsLabelEl = document.getElementById('total-stars-label');
  const footerTextEl = document.getElementById('footer-text');

  if (taglineEl) taglineEl.textContent = t(HOME_LABELS.tagline);
  if (voiceBadgeEl) voiceBadgeEl.textContent = t(HOME_LABELS.voiceBadge);
  if (totalStarsLabelEl) totalStarsLabelEl.textContent = t(HOME_LABELS.totalLbl);
  if (footerTextEl) footerTextEl.textContent = t(HOME_LABELS.footer);

  document.querySelectorAll('.lbl-age4').forEach(el => el.textContent = t(HOME_LABELS.age4));
  document.querySelectorAll('.lbl-age5').forEach(el => el.textContent = t(HOME_LABELS.age5));
  document.querySelectorAll('.lbl-age56').forEach(el => el.textContent = t(HOME_LABELS.age56));
  document.querySelectorAll('.lbl-cat-brain').forEach(el => el.textContent = t(HOME_LABELS.catBrain));
  document.querySelectorAll('.lbl-cat-creative').forEach(el => el.textContent = t(HOME_LABELS.catCreate));
  document.querySelectorAll('.lbl-cat-world').forEach(el => el.textContent = t(HOME_LABELS.catWorld));
  document.querySelectorAll('.lbl-cat-listen').forEach(el => el.textContent = t(HOME_LABELS.catListen));
  document.querySelectorAll('.lbl-cat-phonics').forEach(el => el.textContent = t(HOME_LABELS.catPhonics));
  document.querySelectorAll('.lbl-cat-skills').forEach(el => el.textContent = t(HOME_LABELS.catSkills));
}

function countTotalStars() {
  try {
    const data = JSON.parse(localStorage.getItem('kfl_scores') || '{}');
    const total = Object.values(data).reduce((s, v) => s + (Number(v) || 0), 0);
    const countEl = document.getElementById('total-stars-count');
    if (countEl) countEl.textContent = total;
  } catch (e) {
    console.error('Error counting total stars:', e);
  }
}

function onLanguageChange() {
  renderHomeLanguage();
  speak(HOME_LABELS.greeting);
}

document.addEventListener('DOMContentLoaded', () => {
  initLanguageSelector();
  renderHomeLanguage();
  loadHomeStars();
  countTotalStars();
  speak(HOME_LABELS.greeting);

  // Register Service Worker
  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('service-worker.js').catch(err => console.log('SW registration failed:', err));
  }
});
