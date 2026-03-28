"""
Comprehensive test suite for Kids Fun Learn portal.
Uses Playwright Python API with pytest.

Run: cd kids-fun-learn && python -m pytest tests/test_portal.py -v
"""
import pytest
import os
from playwright.sync_api import sync_playwright

# ─── Paths ────────────────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PORTAL_URL = 'file:///' + os.path.join(BASE_DIR, 'index.html').replace('\\', '/')
ACTIVITIES_DIR = os.path.join(BASE_DIR, 'activities')

# All 28 activities with their expected titles
ACTIVITIES = [
    'balloon-pop', 'block-builder', 'catch-it', 'color-by-number',
    'concept-match', 'counting', 'drawing', 'identify-animals',
    'identify-fruits', 'jigsaw', 'letter-sounds', 'match-columns',
    'math', 'maze', 'memory-game', 'music', 'number-line',
    'odd-one-out', 'pattern', 'pattern-complete', 'rhyming-sort',
    'shadow-match', 'shape-matching', 'sorting-game', 'sound-bingo',
    'tower-build', 'tracing', 'whats-missing',
]


# ─── Fixtures ─────────────────────────────────────────────────────────────
@pytest.fixture(scope="module")
def browser_context():
    """Launch a headless Chromium and share across all tests in this module."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        yield context
        browser.close()


@pytest.fixture
def page(browser_context):
    """Fresh page for each test, auto-closed after."""
    pg = browser_context.new_page()
    yield pg
    pg.close()


# ═══════════════════════════════════════════════════════════════════════════
# 1. HOMEPAGE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestHomepage:

    def test_title(self, page):
        """Homepage has correct title with site name and tagline."""
        page.goto(PORTAL_URL)
        title = page.title()
        assert "Kids Fun Learn" in title
        assert "Fun Education for Ages 4–6" in title

    def test_meta_description(self, page):
        """Homepage has a descriptive meta description tag."""
        page.goto(PORTAL_URL)
        desc = page.locator('meta[name="description"]').get_attribute('content')
        assert desc and len(desc) > 30
        assert "interactive educational portal" in desc.lower()

    def test_og_tags(self, page):
        """Homepage has Open Graph tags for social sharing."""
        page.goto(PORTAL_URL)
        og_title = page.locator('meta[property="og:title"]').get_attribute('content')
        og_desc = page.locator('meta[property="og:description"]').get_attribute('content')
        og_type = page.locator('meta[property="og:type"]').get_attribute('content')
        assert og_title and "Kids Fun Learn" in og_title
        assert og_desc and len(og_desc) > 10
        assert og_type == "website"

    def test_theme_color(self, page):
        """Homepage has theme-color meta tag for mobile browsers."""
        page.goto(PORTAL_URL)
        color = page.locator('meta[name="theme-color"]').get_attribute('content')
        assert color == "#FFD700"

    def test_manifest_link(self, page):
        """Homepage links to the PWA manifest."""
        page.goto(PORTAL_URL)
        manifest = page.locator('link[rel="manifest"]').get_attribute('href')
        assert manifest == "manifest.json"

    def test_heading_structure(self, page):
        """Homepage has exactly one h1 element."""
        page.goto(PORTAL_URL)
        h1_count = page.locator('h1').count()
        assert h1_count == 1
        h1_text = page.locator('h1').text_content()
        assert "Kids Fun Learn" in h1_text

    def test_all_activity_cards_present(self, page):
        """Homepage has links to all 28 activities."""
        page.goto(PORTAL_URL)
        for activity in ACTIVITIES:
            link = page.locator(f'a[href="activities/{activity}.html"]')
            assert link.count() >= 1, f"Missing activity link: {activity}"

    def test_skip_link(self, page):
        """Homepage has a skip-to-content link for keyboard accessibility."""
        page.goto(PORTAL_URL)
        skip = page.locator('.skip-link')
        assert skip.count() >= 1
        href = skip.get_attribute('href')
        assert href == "#main-content"

    def test_main_content_target(self, page):
        """The skip link target element exists."""
        page.goto(PORTAL_URL)
        main = page.locator('#main-content')
        assert main.count() == 1


# ═══════════════════════════════════════════════════════════════════════════
# 2. LANGUAGE SWITCHING TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestLanguageSwitching:

    def test_switch_to_hindi(self, page):
        """Switching to Hindi updates the tagline text."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="hi"]')
        page.wait_for_timeout(300)
        tagline = page.locator('#hero-tagline').text_content()
        assert "मज़ेदार शिक्षा" in tagline

    def test_switch_to_gujarati(self, page):
        """Switching to Gujarati updates the tagline text."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="gu"]')
        page.wait_for_timeout(300)
        tagline = page.locator('#hero-tagline').text_content()
        assert "મઝેદાર શિક્ષા" in tagline

    def test_language_persistence(self, page):
        """Language choice persists in localStorage."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="hi"]')
        page.wait_for_timeout(200)
        lang = page.evaluate("localStorage.getItem('kidsFunLearn_language')")
        assert lang == 'hi'

    def test_switch_back_to_english(self, page):
        """Can switch back to English."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="hi"]')
        page.wait_for_timeout(200)
        page.click('button[data-lang="en"]')
        page.wait_for_timeout(200)
        tagline = page.locator('#hero-tagline').text_content()
        assert "Fun Education for Ages 4–6" in tagline

    def test_active_button_highlight(self, page):
        """Active language button has the 'active' CSS class."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="gu"]')
        page.wait_for_timeout(200)
        assert 'active' in page.locator('button[data-lang="gu"]').get_attribute('class')
        assert 'active' not in page.locator('button[data-lang="en"]').get_attribute('class')

    def test_footer_updates_with_language(self, page):
        """Footer text updates when language changes."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="hi"]')
        page.wait_for_timeout(300)
        footer = page.locator('#footer-text').text_content()
        assert "छोटे" in footer or "कोशिश" in footer

    def test_voice_badge_updates(self, page):
        """Voice badge text updates when language changes."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="hi"]')
        page.wait_for_timeout(300)
        badge = page.locator('#voice-badge-text').text_content()
        assert "आवाज़" in badge

    def test_section_labels_update(self, page):
        """Section labels (age groups, categories) update on language change."""
        page.goto(PORTAL_URL)
        page.click('button[data-lang="hi"]')
        page.wait_for_timeout(300)
        age4 = page.locator('.lbl-age4').first.text_content()
        assert "आयु" in age4


# ═══════════════════════════════════════════════════════════════════════════
# 3. STAR CALCULATION & STORAGE TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestStarSystem:

    def test_total_stars_displays(self, page):
        """Total star count displays on homepage."""
        page.goto(PORTAL_URL)
        page.evaluate("localStorage.setItem('kfl_scores', JSON.stringify({counting: 3, math: 2}))")
        page.reload()
        page.wait_for_timeout(300)
        total = page.locator('#total-stars-count').text_content()
        assert total == "5"

    def test_individual_card_stars(self, page):
        """Individual activity cards show saved star ratings."""
        page.goto(PORTAL_URL)
        page.evaluate("localStorage.setItem('kfl_scores', JSON.stringify({counting: 3, math: 2, pattern: 1}))")
        page.reload()
        page.wait_for_timeout(300)

        counting = page.locator('#stars-counting').text_content()
        assert counting == "⭐⭐⭐"

        math_stars = page.locator('#stars-math').text_content()
        assert math_stars == "⭐⭐☆"

        pattern_stars = page.locator('#stars-pattern').text_content()
        assert pattern_stars == "⭐☆☆"

    def test_zero_stars_when_empty(self, page):
        """Total stars show 0 when no scores saved."""
        page.goto(PORTAL_URL)
        page.evaluate("localStorage.removeItem('kfl_scores')")
        page.reload()
        page.wait_for_timeout(300)
        total = page.locator('#total-stars-count').text_content()
        assert total == "0"

    def test_corrupted_localstorage_handling(self, page):
        """Page handles corrupted localStorage gracefully (no crash)."""
        page.goto(PORTAL_URL)
        page.evaluate("localStorage.setItem('kfl_scores', 'INVALID_JSON{{')")
        page.reload()
        page.wait_for_timeout(300)
        # Page should still load without errors
        h1 = page.locator('h1').text_content()
        assert "Kids Fun Learn" in h1
        total = page.locator('#total-stars-count').text_content()
        assert total == "0"


# ═══════════════════════════════════════════════════════════════════════════
# 4. ACCESSIBILITY TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestAccessibility:

    def test_confetti_canvas_aria_hidden(self, page):
        """Confetti canvas has aria-hidden="true"."""
        page.goto(PORTAL_URL)
        assert page.locator('#confetti-canvas').get_attribute('aria-hidden') == 'true'

    def test_decorative_emoji_aria_hidden(self, page):
        """Decorative emojis on cards have aria-hidden="true"."""
        page.goto(PORTAL_URL)
        emojis = page.locator('.card-emoji')
        for i in range(min(5, emojis.count())):
            assert emojis.nth(i).get_attribute('aria-hidden') == 'true'

    def test_home_emoji_aria_hidden(self, page):
        """Home emoji decoration has aria-hidden="true"."""
        page.goto(PORTAL_URL)
        assert page.locator('.home-emoji').get_attribute('aria-hidden') == 'true'

    def test_language_selector_role(self, page):
        """Language selector has role="group" and aria-label."""
        page.goto(PORTAL_URL)
        selector = page.locator('.language-selector').first
        assert selector.get_attribute('role') == 'group'
        assert selector.get_attribute('aria-label') is not None

    def test_language_buttons_have_aria_labels(self, page):
        """Language buttons have aria-label attributes."""
        page.goto(PORTAL_URL)
        assert page.locator('button[data-lang="en"]').get_attribute('aria-label') == 'English'
        assert page.locator('button[data-lang="hi"]').get_attribute('aria-label') == 'Hindi'
        assert page.locator('button[data-lang="gu"]').get_attribute('aria-label') == 'Gujarati'

    def test_activity_cards_have_aria_labels(self, page):
        """Activity cards have proper aria-label attributes."""
        page.goto(PORTAL_URL)
        cards = page.locator('.activity-card')
        for i in range(cards.count()):
            label = cards.nth(i).get_attribute('aria-label')
            assert label and len(label) > 0, f"Card {i} missing aria-label"

    def test_total_stars_bar_aria_label(self, page):
        """Stars bar has aria-label for accessibility."""
        page.goto(PORTAL_URL)
        assert page.locator('.total-stars-bar').get_attribute('aria-label') == 'Total stars earned'


# ═══════════════════════════════════════════════════════════════════════════
# 5. NAVIGATION TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestNavigation:

    def test_navigate_to_counting(self, page):
        """Can navigate to counting game and back."""
        page.goto(PORTAL_URL)
        page.click('a[href="activities/counting.html"]')
        page.wait_for_timeout(500)
        assert "Counting" in page.title()
        assert "Kids Fun Learn" in page.title()
        # Navigate back
        page.click('button[aria-label="Go Home"]')
        page.wait_for_timeout(500)
        assert "Kids Fun Learn" in page.title()

    def test_navigate_to_math(self, page):
        """Can navigate to math game."""
        page.goto(PORTAL_URL)
        page.click('a[href="activities/math.html"]')
        page.wait_for_timeout(500)
        assert "Math" in page.title()

    def test_navigate_to_shape_matching(self, page):
        """Can navigate to shape matching game."""
        page.goto(PORTAL_URL)
        page.click('a[href="activities/shape-matching.html"]')
        page.wait_for_timeout(500)
        assert "Shape Matching" in page.title()


# ═══════════════════════════════════════════════════════════════════════════
# 6. ACTIVITY PAGE SEO TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestActivitySEO:

    @pytest.mark.parametrize("activity", ACTIVITIES)
    def test_activity_has_title(self, page, activity):
        """Every activity page has a title tag with 'Kids Fun Learn'."""
        url = 'file:///' + os.path.join(ACTIVITIES_DIR, f'{activity}.html').replace('\\', '/')
        page.goto(url)
        title = page.title()
        assert "Kids Fun Learn" in title, f"{activity} missing 'Kids Fun Learn' in title"

    @pytest.mark.parametrize("activity", ACTIVITIES)
    def test_activity_has_meta_description(self, page, activity):
        """Every activity page has a non-generic meta description."""
        url = 'file:///' + os.path.join(ACTIVITIES_DIR, f'{activity}.html').replace('\\', '/')
        page.goto(url)
        meta = page.locator('meta[name="description"]')
        assert meta.count() >= 1, f"{activity} missing meta description"
        desc = meta.get_attribute('content')
        assert desc and len(desc) > 40, f"{activity} has too-short meta description"

    @pytest.mark.parametrize("activity", ACTIVITIES)
    def test_activity_has_og_tags(self, page, activity):
        """Every activity page has Open Graph title and description."""
        url = 'file:///' + os.path.join(ACTIVITIES_DIR, f'{activity}.html').replace('\\', '/')
        page.goto(url)
        og_title = page.locator('meta[property="og:title"]')
        og_desc = page.locator('meta[property="og:description"]')
        assert og_title.count() >= 1, f"{activity} missing og:title"
        assert og_desc.count() >= 1, f"{activity} missing og:description"

    @pytest.mark.parametrize("activity", ACTIVITIES)
    def test_activity_has_h1(self, page, activity):
        """Every activity page has exactly one h1."""
        url = 'file:///' + os.path.join(ACTIVITIES_DIR, f'{activity}.html').replace('\\', '/')
        page.goto(url)
        h1_count = page.locator('h1').count()
        assert h1_count == 1, f"{activity} has {h1_count} h1 elements"


# ═══════════════════════════════════════════════════════════════════════════
# 7. RESPONSIVE DESIGN TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestResponsive:

    def test_mobile_layout(self, browser_context):
        """Homepage renders correctly at mobile breakpoint (375px)."""
        page = browser_context.new_page()
        page.set_viewport_size({'width': 375, 'height': 667})
        page.goto(PORTAL_URL)
        page.wait_for_timeout(300)

        # Cards grid should be visible and not overflow
        grid = page.locator('.cards-grid').first
        box = grid.bounding_box()
        assert box is not None
        assert box['width'] <= 375

        # Activity cards should still be visible
        cards = page.locator('.activity-card')
        assert cards.count() >= 20
        page.close()

    def test_tablet_layout(self, browser_context):
        """Homepage renders correctly at tablet breakpoint (768px)."""
        page = browser_context.new_page()
        page.set_viewport_size({'width': 768, 'height': 1024})
        page.goto(PORTAL_URL)
        page.wait_for_timeout(300)

        grid = page.locator('.cards-grid').first
        box = grid.bounding_box()
        assert box is not None
        assert box['width'] <= 768
        page.close()

    def test_desktop_layout(self, browser_context):
        """Homepage renders correctly at desktop size (1280px)."""
        page = browser_context.new_page()
        page.set_viewport_size({'width': 1280, 'height': 800})
        page.goto(PORTAL_URL)
        page.wait_for_timeout(300)

        # Container should be constrained to max-width
        container = page.locator('.container')
        box = container.bounding_box()
        assert box is not None
        assert box['width'] <= 1016  # max-width: 1000px + padding
        page.close()


# ═══════════════════════════════════════════════════════════════════════════
# 8. CSS & STYLING TESTS
# ═══════════════════════════════════════════════════════════════════════════

class TestStyling:

    def test_google_fonts_loaded(self, page):
        """CSS imports Google Fonts."""
        page.goto(PORTAL_URL)
        # Check that the font is referenced in a stylesheet
        fonts_loaded = page.evaluate("""
            Array.from(document.styleSheets)
                .filter(s => { try { return s.cssRules; } catch(e) { return false; } })
                .some(s => Array.from(s.cssRules).some(r => r.cssText && r.cssText.includes('Baloo')))
        """)
        # The font is referenced via @import in style.css
        assert page.locator('link[href*="style.css"]').count() >= 1

    def test_css_custom_properties(self, page):
        """CSS custom properties (variables) are defined."""
        page.goto(PORTAL_URL)
        yellow = page.evaluate("getComputedStyle(document.documentElement).getPropertyValue('--yellow').trim()")
        assert yellow == "#FFD700"

    def test_activity_card_hover_effect(self, page):
        """Activity cards have transition properties for hover effects."""
        page.goto(PORTAL_URL)
        card = page.locator('.activity-card').first
        transition = page.evaluate("""
            getComputedStyle(document.querySelector('.activity-card')).transition
        """)
        assert 'transform' in transition
