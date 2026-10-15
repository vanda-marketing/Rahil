#!/usr/bin/env python3
"""Builds the Rahil Patel site: shared header/footer, one HTML file per tab."""
import json, html, pathlib

OUT = pathlib.Path(__file__).parent
U = "https://rahilpatel.org/wp-content/uploads/"
SITE = "https://rahilpatel.org"
EMAIL = "rahilfoundbylove@gmail.com"
SUBSTACK = "https://substack.com/@rahilpatelwrites"
X_URL = "https://x.com/rahil3272"
PORTRAIT = U + "2025/10/About-RAhil-Right-Image.png"

NAV = [
    ("story", "Rahil’s Story", "rahils-story.html", "/rahils-story/"),
    ("writing", "Writings", "writing.html", "/writing/"),
    ("books", "Books", "books.html", "/books/"),
    ("video", "Video", "video.html", "/video/"),
    ("courses", "Courses", "courses.html", "/courses/"),
    ("speaking", "Speaking", "speaking.html", "/speaking/"),
    ("partnerships", "Partnerships", "partnerships.html", "/partnerships/"),
]
e = html.escape

ARROW = ('<span class="arrow" aria-hidden="true"><svg width="10" height="10" viewBox="0 0 10 10" fill="none">'
         '<path d="M1.5 8.5L8.5 1.5M8.5 1.5H3M8.5 1.5V7" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round"/></svg></span>')
PLAY = ('<span class="play" aria-hidden="true"><svg width="20" height="22" viewBox="0 0 20 22">'
        '<path d="M19 11L1 21V1z" fill="#000"/></svg></span>')


def btn(label, href, cls="", external=False):
    ext = ' target="_blank" rel="noopener"' if external else ""
    return f'<a class="round-btn {cls}" href="{e(href)}"{ext}>{e(label)}{ARROW}</a>'


def icon_link(icon, text, href, external=False, alt=""):
    ext = ' target="_blank" rel="noopener"' if external else ""
    return (f'<a class="icon-link" href="{e(href)}"{ext}><span class="ring"><img src="{icon}" alt="{e(alt)}" width="16" height="16"></span>'
            f'<span>{e(text)}</span></a>')


def yt(vid, title, thumb=None, start=None):
    thumb = thumb or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"
    s = f' data-start="{start}"' if start else ""
    return (f'<button class="yt" type="button" data-id="{vid}"{s} aria-label="Play video: {e(title)}">'
            f'<img src="{e(thumb)}" alt="" loading="lazy" width="640" height="360">{PLAY}</button>'
            f'<noscript><a href="https://www.youtube.com/watch?v={vid}">Watch “{e(title)}” on YouTube</a></noscript>')


def person_ref():
    return {"@id": SITE + "/#person"}


PERSON = {
    "@type": "Person", "@id": SITE + "/#person", "name": "Rahil Patel", "url": SITE + "/",
    "image": PORTRAIT,
    "jobTitle": "Speaker, writer and teacher in Christian apologetics",
    "description": "Former Hindu monk of twenty years who became a Christian. Speaks, writes and teaches on Hindu thought, Indian culture and India’s growing global influence.",
    "email": "mailto:" + EMAIL,
    "homeLocation": {"@type": "Place", "name": "Oxfordshire, United Kingdom"},
    "knowsAbout": ["Hinduism", "Hindu philosophy", "Christian apologetics", "Indian culture", "Interfaith dialogue", "India and global affairs"],
    "sameAs": [X_URL, SUBSTACK, "https://theocca.org/author/rahil-patel/", "https://www.ctcollege.org/guest-lecturers/rahil-patel/"],
}
WEBSITE = {"@type": "WebSite", "@id": SITE + "/#website", "url": SITE + "/", "name": "Rahil Patel",
           "inLanguage": "en-GB", "publisher": person_ref()}


def crumbs(name, path):
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
        {"@type": "ListItem", "position": 2, "name": name, "item": SITE + path}]}


def video_obj(vid, name, desc, thumb=None):
    # uploadDate: add each video's YouTube publish date (YYYY-MM-DD) for Google video rich results
    return {"@type": "VideoObject", "name": name, "description": desc,
            "thumbnailUrl": [thumb or f"https://i.ytimg.com/vi/{vid}/hqdefault.jpg"],
            "contentUrl": f"https://www.youtube.com/watch?v={vid}",
            "embedUrl": f"https://www.youtube.com/embed/{vid}",
            "uploadDate": "ADD-YOUTUBE-PUBLISH-DATE",
            "actor": person_ref()}


def page(key, title, desc, body, schema_nodes, canonical_path, og_image=PORTRAIT, header_cls="inner"):
    nav_items = "".join(
        f'<li><a href="{f}"{" aria-current=\"page\"" if k == key else ""}>{e(lbl)}</a></li>' for k, lbl, f, _ in NAV)
    graph = {"@context": "https://schema.org", "@graph": [WEBSITE, PERSON] + schema_nodes}
    full_title = title if key == "home" else f"{title} | Rahil Patel"
    footer_links_1 = "".join(f'<li><a href="{f}">{e(l)}</a></li>' for _, l, f, _ in NAV[:4])
    footer_links_2 = "".join(f'<li><a href="{f}">{e(l)}</a></li>' for _, l, f, _ in NAV[4:])
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(full_title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{canonical_path}">
<meta name="robots" content="index, follow, max-image-preview:large">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Rahil Patel">
<meta property="og:title" content="{e(full_title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{canonical_path}">
<meta property="og:image" content="{og_image}">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@rahil3272">
<link rel="icon" href="{U}2025/11/cropped-favicon-32x32.png" sizes="32x32">
<link rel="icon" href="{U}2025/11/cropped-favicon-192x192.png" sizes="192x192">
<link rel="apple-touch-icon" href="{U}2025/11/cropped-favicon-180x180.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=El+Messiri:wght@400..700&family=Geist:wght@300..600&display=swap">
<link rel="stylesheet" href="assets/styles.css">
<script type="application/ld+json">
{json.dumps(graph, ensure_ascii=False, indent=1)}
</script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header {header_cls}">
  <div class="container">
    <div class="header-top">
      <a class="logo" href="index.html" aria-label="Rahil Patel, home"><img src="{U}2025/11/logo.png" alt="Rahil Patel. Author, Speaker, Tutor" width="210" height="62"></a>
      <div class="header-actions">
        {btn("Subscribe", SUBSTACK, "gold small", True)}
        <button class="menu-toggle" type="button" aria-label="Open menu" aria-controls="mobile-menu" aria-expanded="false"><span></span><span></span><span></span></button>
      </div>
    </div>
    <nav class="desktop-nav" aria-label="Main"><ul>{nav_items}</ul></nav>
  </div>
  <div class="mobile-menu" id="mobile-menu" hidden>
    <button class="close-btn" type="button" aria-label="Close menu">&times;</button>
    <ul>{nav_items}</ul>
    {btn("Subscribe on Substack", SUBSTACK, "gold", True)}
    <div class="contact">{icon_link(U + "2025/10/mail.svg", EMAIL, "mailto:" + EMAIL, alt="Email")}</div>
  </div>
</header>

<main id="main">
{body}

<section class="subscribe" aria-labelledby="subscribe-title">
  <div class="container inner">
    <div>
      <span class="eyebrow">Stay in touch</span>
      <h2 id="subscribe-title" class="h-section">Get Rahil’s writing in your inbox</h2>
      <p>Essays on faith, culture and civilisation, published on Substack. Free to subscribe.</p>
    </div>
    {btn("Subscribe", SUBSTACK, "gold", True)}
  </div>
</section>
</main>

<footer class="site-footer">
  <div class="container">
    <div class="footer-top">
      <div>
        <a class="footer-logo" href="index.html" aria-label="Rahil Patel, home"><img src="{U}2025/11/footernew.svg" alt="Rahil Patel" width="170" height="50"></a>
        <p class="footer-tag">Speaker, writer and teacher on Hindu thought, Indian culture and Christian apologetics.</p>
      </div>
      <ul class="footer-links">{footer_links_1}</ul>
      <ul class="footer-links">{footer_links_2}</ul>
      <div class="footer-right">
        {icon_link(U + "2025/10/mail.svg", EMAIL, "mailto:" + EMAIL, alt="Email")}
        {icon_link(U + "2026/10/substack.svg", "Substack", SUBSTACK, True, alt="Substack")}
        {icon_link(U + "2025/10/form-twitter-icon.svg", "@rahil3272", X_URL, True, alt="X")}
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 Rahil Patel. All rights reserved.</span>
      <span>Website by <a href="https://www.globalmediainsight.com/" target="_blank" rel="noopener">Global Media Insight</a></span>
    </div>
  </div>
</footer>
<script src="assets/site.js" defer></script>
</body>
</html>
"""


def hero(eyebrow, title_html, lede, sub=None):
    subnav = ""
    if sub:
        subnav = '<nav class="subnav" aria-label="On this page">' + "".join(
            f'<a class="pill" href="#{a}">{e(l)}</a>' for a, l in sub) + "</nav>"
    return f"""<section class="page-hero">
  <div class="container reveal">
    <span class="eyebrow">{e(eyebrow)}</span>
    <h1 class="h-display">{title_html}</h1>
    <p class="lede">{e(lede)}</p>
    {subnav}
  </div>
</section>"""


# ---------------- Data ----------------
INTERVIEWS = [
    ("lbI4Ul0WEuk", "Rahil Patel with Above The Bar Church", "Above The Bar Church", U + "2025/10/church.jpg", None),
    ("4MVpvCd5nYY", "Rahil Patel with David Deane", "David Deane", U + "2025/10/video-interview-image-3.png", 196),
    ("eNny3And2SE", "Rahil Patel with Cheryl Pinto", "Cheryl Pinto", U + "2025/10/video-interview-image-2.png", 64),
    ("P6khABuP-kg", "Rahil Patel with Lisa Fields", "Lisa Fields", U + "2025/10/video-interview-image-1.png", None),
]
FILMS = [
    ("09n8WRCcb78", "A Short Documentary", "When Christ Fulfills",
     "This short film, produced by the Billy Graham Evangelistic Association, shares Rahil’s journey of faith and transformation.",
     U + "2025/10/A-Short-Documentary_1.png", "Short film"),
    ("8aEHUJN8WyA", "The Witness Conference", "Beyond Religion: A Relationship with God",
     "Filmed at a conference in India, this 30-minute video captures Rahil sharing his story of transformation and hope.",
     U + "2025/10/The-Witness-Conference.png", "30 minutes"),
    ("yz3kLwUNZrY", "A New Beginning", "How Christ Shapes the Heart and Mind",
     "Filmed for national television in Suriname, this 1 hour 40 minute interview offers an in-depth look at Rahil’s journey of faith and transformation.",
     U + "2025/10/a-new-beginning.jpg", "1 hour 40 minutes"),
]
PODCASTS = [
    ("Undeceptions with John Dickson", "https://podcasts.apple.com/gb/podcast/hindu-priest/id1478239058?i=1000471271495", U + "2025/10/underceptions.png", "Apple Podcasts"),
    ("Dancing with Wisdom", "https://drsunil.com/leadership/harry-potter-and-the-hindu-priest/", U + "2025/10/prodcast-image-2.png", "Dr Sunil"),
    ("Inspired with Simon Guillebaud", "https://podcasts.apple.com/gb/podcast/from-hindu-priest-to-follower-of-jesus-rahil-patel/id1564089451?i=1000723846245", U + "2025/10/podcast.png", "Apple Podcasts"),
    ("Evidence and Answers with Patrick Zukeran: Episode 848", "https://www.listennotes.com/podcasts/evidence-answers/episode-848-hinduism-to-b-ly8Pk0rQq/", U + "2025/10/Rectangle-45.png", "Listen Notes"),
    ("Evidence and Answers with Patrick Zukeran: Episode 171", "https://www.listennotes.com/podcasts/evidence-answers/episode-171-sharing-christ-bv4Zk3TqGf-/", U + "2025/10/Rectangle-45.png", "Listen Notes"),
]
PRESS = [
    ("Christianity Today", "USA", "https://www.christianitytoday.com/2024/03/rahil-patel-testimony-hindu-priest/"),
    ("Premier Christianity", "UK", "https://www.premierchristianity.com/home/rahil-patel-from-hindu-priest-to-peace-filled-christian/1383.article"),
    ("God Reports", "USA", "https://www.godreports.com/2020/06/after-20-years-as-a-swami-hindu-was-touched-by-childrens-bible/"),
    ("Church Times", "UK", "https://www.churchtimes.co.uk/articles/2016/23-september/features/interviews/interview-rahil-patel-author"),
    ("IFES", "Netherlands", "https://ifesworld.org/en/journal/why-inter-religious-dialogue-needs-apologetics-benno-van-den-toren/"),
    ("Baptists Union", "UK", "https://www.baptist.org.uk/Articles/469385/Found_by_love.aspx"),
    ("Eternity News", "Australia", "https://www.eternitynews.com.au/australia/what-is-lacking-in-christianity-by-a-hindu-who-turned-to-jesus/amp/"),
    ("Teach to Reach", "UK", "https://www.twonineteen.org.uk/2019/hospitality-and-the-gospel-part-2-by-david/"),
]
OCCA = [
    ("Searching for Inner Peace", "occa-article/why-good-wishes-resonate-occa-article-text3/", "What does real peace look like and where does it come from? From prostrate pilgrims in India to billionaires with heavy minds, the search is universal."),
    ("What Civilisations Choose to Remember", "occa-article/why-good-wishes-resonate-occa-article-text2/", "Why do old artefacts matter? Rahil examines the recent return of Chola artefacts to India, and what museums and memory say about identity."),
    ("Untouchable in the Land of Equality", "occa-article/why-good-wishes-resonate-occa-article-text1/", "Caste is not exclusive to India. It is showing up in Silicon Valley boardrooms too, and the Christian story offers good news."),
    ("Swearing on the Gita", "occa-article/swearing-on-the-gita/", "Is swearing on the Bhagavad Gita the same as swearing on a Bible? Rahil reflects on truth and the intentions behind the gesture."),
    ("How Christian Marriage Reshaped Indian Law", "occa-article/how-christian-marriage-reshaped-indian-law/", "How did ‘one husband and one wife’ enter law in a land shaped by epics where plural marriage was the norm?"),
    ("Love and Truth", "occa-article/love-and-truth/", "Every January, warm New Year wishes arrive from traditions that never quite framed the world that way."),
    ("Work, Conscience and the Architecture of Trust", "occa-article/work-conscience-and-the-architecture-of-trust/", "Why does ‘Made in Germany’ carry such weight? A line from a Mercedes factory floor back to Martin Luther."),
    ("Engaging with Truth in the Context of Indic Faiths", "occa-article/engaging-with-truth-in-the-context-of-indic-faiths/", "Talk with someone from a Hindu, Jain, Sikh or Buddhist background and you may notice truth works differently."),
]
SEEN = [
    ("Why good wishes resonate across cultures", "seen-unseen-article/why-good-wishes-resonate-across-cultures-11/"),
    ("There’s fear or fascination as cultures confront death", "seen-unseen-article/why-good-wishes-resonate-across-cultures-10/"),
    ("The tale of two Hindu Prime Ministers", "seen-unseen-article/why-good-wishes-resonate-across-cultures-9/"),
    ("The Merc, the monks, and the pursuit of excellence", "seen-unseen-article/why-good-wishes-resonate-across-cultures-8/"),
    ("Rishi Sunak’s wealth and why he doesn’t apologise for it", "seen-unseen-article/why-good-wishes-resonate-across-cultures-7/"),
    ("Untouchable: experiencing discrimination around the world", "seen-unseen-article/why-good-wishes-resonate-across-cultures-6/"),
    ("Re-defining marriage: how India slowly changed its mind", "seen-unseen-article/why-good-wishes-resonate-across-cultures-5/"),
]
ESSAYS = [
    ("Fighting for India’s soul: hope, hate and the Citizenship (Amendment) Act 2019", "essay/fighting-for-indias-soul-hope-hate-and-the-citizenship-amendment-act-2019-caa-2/", "An introduction to and critical evaluation of the Indian government’s Citizenship (Amendment) Act 2019 and its economic and diplomatic implications."),
    ("Religious relations: Modi, the Hindu Rashtra and India’s new internationalism", "essay/fighting-for-indias-soul-hope-hate-and-the-citizenship-amendment-act-2019-caa-3/", "How Prime Minister Narendra Modi’s Hindu faith shapes India’s domestic affairs and international relations."),
]
BLOGS = [
    ("The Leader and Perfectionist Conundrum: there’s no such thing as tractors!", "blog/the-leader-and-perfectionist-conundrum-theres-no-such-thing-as-tractors-4/"),
    ("When Leaders Sit with Clouds", "blog/when-leaders-sit-with-clouds/"),
    ("Are We Present?", "blog/are-we-present/"),
    ("How Much Do We Know?", "blog/how-much-do-we-know/"),
    ("Crushed but Not Broken", "blog/crushed-but-not-broken/"),
]
TRANSLATIONS = [
    ("Swedish", "sv", U + "2025/10/swedish-version.png", "https://www.nyamusik.se/bocker/biografier-livsberattelser/karleken-fann-mig--en-hinduprasts-mote-med-jesus-402637"),
    ("Danish", "da", U + "2025/11/Danish.png", "https://prorex.dk/shop/1694-biografier/18331---hindupraest-moeder-jesus/"),
    ("Polish", "pl", U + "2025/11/Polish.png", "https://clc.org.pl/produkt/podroz-do-milosci/"),
    ("Dutch", "nl", U + "2025/11/Dutch.png", "https://www.amazon.co.uk/Gevonden-door-liefde-hindoepriester-Christus/dp/9043528927"),
    ("Traditional Chinese", "zh-Hant", U + "2025/11/Traditional-Chinese.png", "https://www.elimbookstore.com.tw/shop.php?searchmode=&Fkeyword=%E8%A2%AB%E6%84%9B%E5%B0%8B%E8%A6%8B&html=list_goods"),
    ("Estonian", "et", U + "2025/11/Estonian.png", "https://iamcentre.ee/shop/sarjad/rahvaste-lood/armastus-leidis-minu-hindu-preestri-rannak-toeni/"),
]
AMAZON = "https://www.amazon.co.uk/Found-Love-Priest-Encounters-Christ/dp/190972842X"
BIOLA = "https://learn.biola.edu/bundles/christian-apologetics-certificate"
CTC = "https://www.ctcollege.org/guest-lecturers/rahil-patel/"
OCCA_URL = "https://theocca.org/author/rahil-patel/"

pages = {}

# ---------------- Home ----------------
cards = [
    ("Video", "video.html", "Interviews, films and podcasts"),
    ("Books", "books.html", "Found by Love and more"),
    ("Courses", "courses.html", "Study apologetics with Rahil"),
    ("Speaking", "speaking.html", "Invite Rahil to your event"),
    ("Writings", "writing.html", "Articles, essays and blogs"),
    ("Partnerships", "partnerships.html", "Organisations Rahil works with"),
]
card_html = "".join(
    f'<a class="leaf-card" href="{h}"><span class="round-btn">{e(t)}{ARROW}</span><span class="desc">{e(d)}</span></a>'
    for t, h, d in cards)
latest = "".join(
    f'<article class="media-card"><span class="meta">OCCA article</span><h3><a href="{SITE}/{p}">{e(t)}</a></h3><p>{e(x)}</p></article>'
    for t, p, x in OCCA[:3])
featured_video = INTERVIEWS[0]
home_body = f"""
<section class="home-hero">
  <div class="container reveal">
    <h1 class="h-display">When <span class="highlight">Civilizations</span> Meet</h1>
    <p class="lede">Speaker, writer and teacher on Hindu thought, Indian culture and Christian apologetics.</p>
    <a class="scroll-down" href="#about-rahil" aria-label="Scroll to About Rahil"><svg width="20" height="22" viewBox="0 0 20 22" fill="none" aria-hidden="true"><path d="M10 1v19M10 20l8-8M10 20l-8-8" stroke="#B1926D" stroke-width="1.4" stroke-linecap="round" stroke-linejoin="round"/></svg></a>
  </div>
</section>

<section class="section about" id="about-rahil" aria-labelledby="about-title">
  <div class="container about-grid">
    <div>
      <span class="eyebrow">About Rahil</span>
      <h2 id="about-title" class="h-section">From Hindu monk to Christ</h2>
      <div class="prose" style="margin-top:26px">
        <p>Rahil Patel is a speaker, writer and teacher in Christian apologetics, specialising in Hindu thought, Indian culture and India’s growing global influence. Before becoming a Christian, he spent twenty years as a Hindu monk, living, teaching and travelling within Hindu communities across the world.</p>
        <p>Drawing on this unusual journey, Rahil now helps churches, leaders, students and wider audiences understand Hinduism and engage thoughtfully with people from Hindu backgrounds. His work combines theology, culture, history and lived experience, building bridges between different worlds with clarity, respect and depth.</p>
        <p>Rahil is the author of <i>Found by Love</i>, which has been translated into nine languages, and <i>Bridging Worlds of Hinduism &amp; Christianity: Understanding Hindu Thought &amp; Practice</i>. His first novel, <i>A Search for Bread</i>, will be published by Pippa Rann Books in November 2026. He lives with his wife and daughter in Oxfordshire, United Kingdom.</p>
      </div>
      <ul class="facts">
        <li><strong>20</strong><span>years as a Hindu monk</span></li>
        <li><strong>9</strong><span>languages <i>Found by Love</i> is published in</span></li>
        <li><strong>3</strong><span>books, including a novel due November 2026</span></li>
      </ul>
    </div>
    <div class="about-image"><img src="{PORTRAIT}" alt="Rahil Patel" width="440" height="560"></div>
  </div>
</section>

<section class="section" aria-labelledby="story-banner-title">
  <div class="container">
    <div class="story-unfold">
      <div>
        <h2 id="story-banner-title">From Hindu Monk to Christ</h2>
        <p>See the Story Unfold</p>
        {btn("Watch Rahil’s story", "rahils-story.html")}
      </div>
    </div>
  </div>
</section>

<section class="section cream" aria-labelledby="explore-title">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Speaking, Teaching, Writing</span>
      <h2 id="explore-title" class="h-section">Shaping Conversations on Faith, Culture and Civilisation</h2>
    </div>
    <div class="card-grid">{card_html}</div>
  </div>
</section>

<section class="section" aria-labelledby="home-video-title">
  <div class="container media-grid two" style="align-items:center">
    <div>{yt(featured_video[0], featured_video[1], featured_video[3], featured_video[4])}</div>
    <div>
      <span class="eyebrow">Video</span>
      <h2 id="home-video-title" class="h-section">Watch Rahil in conversation</h2>
      <p style="margin-top:16px;color:var(--text-soft)">Interviews with churches, theologians and apologists, plus films telling Rahil’s story.</p>
      <div class="section-foot">{btn("See all video", "video.html")}</div>
    </div>
  </div>
</section>

<section class="section warm" aria-labelledby="home-writing-title">
  <div class="container">
    <div class="section-head">
      <span class="eyebrow">Latest writing</span>
      <h2 id="home-writing-title" class="h-section">Recent articles</h2>
    </div>
    <div class="media-grid">{latest}</div>
    <div class="section-foot">{btn("Read all writings", "writing.html")}</div>
  </div>
</section>
"""
pages["index.html"] = page(
    "home", "Rahil Patel | Speaker, Author and Teacher on Hinduism and Christianity",
    "Rahil Patel spent twenty years as a Hindu monk before becoming a Christian. He speaks, writes and teaches on Hindu thought, Indian culture and Christian apologetics.",
    home_body,
    [{"@type": "ProfilePage", "@id": SITE + "/#webpage", "url": SITE + "/", "name": "Rahil Patel",
      "isPartOf": {"@id": SITE + "/#website"}, "mainEntity": person_ref(), "primaryImageOfPage": PORTRAIT}],
    "/", header_cls="")

# ---------------- Story ----------------
films_html = "".join(f"""
<article class="film">
  <div class="film-media">{yt(v, h2, th)}</div>
  <div>
    <span class="eyebrow">{e(eb)}</span>
    <h2 class="h-section">{e(h2)}</h2>
    <p style="margin-top:18px">{e(d)}</p>
    <span class="duration">{e(dur)}</span>
  </div>
</article>""" for v, eb, h2, d, th, dur in FILMS)
story_body = hero("Rahil’s Story", 'From Hindu Monk <span class="highlight">to Christ</span>',
                  "Twenty years as a Hindu monk, then an encounter that changed everything. Three films tell the story.") + f"""
<section class="section" aria-label="Films">
  <div class="container">{films_html}</div>
</section>"""
pages["rahils-story.html"] = page(
    "story", "Rahil’s Story", "Watch three films about Rahil Patel’s journey from twenty years as a Hindu monk to faith in Christ.",
    story_body,
    [crumbs("Rahil’s Story", "/rahils-story/")] + [video_obj(v, h2, d, th) for v, eb, h2, d, th, dur in FILMS],
    "/rahils-story/")

# ---------------- Video ----------------
interview_html = "".join(f"""
<article class="media-card">
  {yt(v, t, th, st)}
  <span class="meta">Interview</span>
  <h3>{e(t)}</h3>
</article>""" for v, t, host, th, st in INTERVIEWS)
film_cards = "".join(f"""
<article class="media-card">
  {yt(v, h2, th)}
  <span class="meta">{e(eb)} · {e(dur)}</span>
  <h3>{e(h2)}</h3>
</article>""" for v, eb, h2, d, th, dur in FILMS)
pod_html = "".join(
    f'<a class="podcast" href="{e(u)}" target="_blank" rel="noopener"><img src="{im}" alt="" loading="lazy" width="96" height="96"><div><h3>{e(t)}</h3><span>Listen on {e(src)}</span></div></a>'
    for t, u, im, src in PODCASTS)
press_html = "".join(
    f'<li><div><h3><a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a></h3></div><span class="source">{e(c)}</span></li>'
    for n, c, u in PRESS)
video_body = hero("Video", 'Watch and <span class="highlight">Listen</span>',
                  "Interviews, films, podcasts and press features with Rahil Patel.",
                  [("interviews", "Video interviews"), ("films", "Story films"), ("podcasts", "Podcasts"), ("press", "In the press")]) + f"""
<section class="section" id="interviews" aria-labelledby="int-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Video interviews</span><h2 id="int-title" class="h-section">Conversations with Rahil</h2></div>
    <div class="media-grid two">{interview_html}</div>
  </div>
</section>
<section class="section cream" id="films" aria-labelledby="films-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Story films</span><h2 id="films-title" class="h-section">Rahil’s journey on film</h2></div>
    <div class="media-grid">{film_cards}</div>
  </div>
</section>
<section class="section" id="podcasts" aria-labelledby="pod-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Podcasts</span><h2 id="pod-title" class="h-section">Listen to Rahil</h2></div>
    <div class="media-grid two">{pod_html}</div>
  </div>
</section>
<section class="section warm" id="press" aria-labelledby="press-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">In the press</span><h2 id="press-title" class="h-section">Magazine and news features</h2></div>
    <ul class="list">{press_html}</ul>
  </div>
</section>"""
video_schema = [crumbs("Video", "/video/")]
video_schema += [video_obj(v, t, f"Rahil Patel, former Hindu monk, in conversation with {host}.", th) for v, t, host, th, st in INTERVIEWS]
video_schema += [video_obj(v, h2, d, th) for v, eb, h2, d, th, dur in FILMS]
video_schema += [{"@type": "PodcastEpisode", "name": t, "url": u, "image": im, "actor": person_ref()} for t, u, im, src in PODCASTS]
video_schema += [{"@type": "ItemList", "name": "Press features about Rahil Patel", "itemListElement": [
    {"@type": "ListItem", "position": i + 1, "url": u, "name": f"{n} ({c})"} for i, (n, c, u) in enumerate(PRESS)]}]
pages["video.html"] = page("video", "Video", "Watch interviews and films with Rahil Patel, listen to his podcast appearances, and read press features.",
                           video_body, video_schema, "/video/")

# ---------------- Books ----------------
trans_html = "".join(
    f'<a class="translation" href="{e(u)}" target="_blank" rel="noopener" hreflang="{lc}"><img src="{im}" alt="Found by Love, {e(n)} edition" loading="lazy" width="150" height="225"><span>{e(n)}</span><small>Buy</small></a>'
    for n, lc, im, u in TRANSLATIONS)
books_body = hero("Books", 'Books by <span class="highlight">Rahil Patel</span>',
                  "A memoir published in nine languages, a guide to Hindu thought for Christians, and a first novel.",
                  [("found-by-love", "Found by Love"), ("translations", "Translations"), ("more-books", "More books")]) + f"""
<section class="section" id="found-by-love" aria-labelledby="fbl-title">
  <div class="container book-feature">
    <img src="{U}2025/12/found-by-love-img.png" alt="Cover of Found by Love by Rahil Patel" width="300" height="450">
    <div>
      <span class="eyebrow">Memoir</span>
      <h2 id="fbl-title" class="h-section">Found by Love</h2>
      <p style="margin-top:18px;max-width:560px">A journey of transformation and the search for meaning that touches us all. The story of a Hindu priest who encountered Christ.</p>
      {btn("Buy on Amazon UK", AMAZON, "", True)}
    </div>
  </div>
</section>
<section class="section cream" id="translations" aria-labelledby="tr-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Available translations</span><h2 id="tr-title" class="h-section">Read Found by Love in your language</h2>
      <p>For other translations, contact the publisher at <a class="text-link" href="mailto:info@instantapostle.com">info@instantapostle.com</a>.</p></div>
    <div class="translations">{trans_html}</div>
  </div>
</section>
<section class="section" id="more-books" aria-labelledby="more-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">More books</span><h2 id="more-title" class="h-section">Also by Rahil</h2></div>
    <div class="book-row">
      <article class="book-card">
        <div class="book-cover" aria-hidden="true"><small>Rahil Patel</small>Bridging Worlds of Hinduism &amp; Christianity</div>
        <div>
          <h3 class="h-card">Bridging Worlds of Hinduism &amp; Christianity</h3>
          <p>Understanding Hindu Thought &amp; Practice. A guide for Christians who want to understand Hindu belief and engage their Hindu neighbours well.</p>
        </div>
      </article>
      <article class="book-card">
        <div class="book-cover" aria-hidden="true"><small>A novel</small>A Search for Bread</div>
        <div>
          <h3 class="h-card">A Search for Bread</h3>
          <p>Rahil’s first novel, published by Pippa Rann Books.</p>
          <span class="badge">Coming November 2026</span>
        </div>
      </article>
    </div>
  </div>
</section>"""
books_schema = [crumbs("Books", "/books/"),
    {"@type": "Book", "@id": SITE + "/books/#found-by-love", "name": "Found by Love", "author": person_ref(),
     "image": U + "2025/12/found-by-love-img.png", "isbn": "190972842X", "inLanguage": "en", "url": SITE + "/books/",
     "description": "Rahil Patel’s memoir of twenty years as a Hindu priest and his encounter with Christ.",
     "offers": {"@type": "Offer", "url": AMAZON, "availability": "https://schema.org/InStock"},
     "workExample": [{"@type": "Book", "name": f"Found by Love ({n} edition)", "inLanguage": lc, "image": im, "url": u,
                      "author": person_ref()} for n, lc, im, u in TRANSLATIONS]},
    {"@type": "Book", "@id": SITE + "/books/#bridging-worlds", "name": "Bridging Worlds of Hinduism & Christianity: Understanding Hindu Thought & Practice",
     "author": person_ref(), "url": SITE + "/books/"},
    {"@type": "Book", "@id": SITE + "/books/#a-search-for-bread", "name": "A Search for Bread", "genre": "Novel", "bookFormat": "https://schema.org/Paperback",
     "author": person_ref(), "publisher": {"@type": "Organization", "name": "Pippa Rann Books"}, "datePublished": "2026-11", "url": SITE + "/books/"}]
pages["books.html"] = page("books", "Books", "Books by Rahil Patel: Found by Love (in nine languages), Bridging Worlds of Hinduism & Christianity, and the novel A Search for Bread.",
                           books_body, books_schema, "/books/", og_image=U + "2025/12/found-by-love-img.png")

# ---------------- Courses ----------------
courses_body = hero("Courses", 'Learn with <span class="highlight">Rahil</span>',
                    "Study Christian apologetics and Hindu thought with Rahil through accredited programmes and guest lectures.") + f"""
<section class="section" aria-label="Courses">
  <div class="container">
    <article class="course">
      <div class="course-logo"><img src="{U}2026/04/Biola-Learn-Logo_half-e1775556543502.jpg" alt="Biola Learn" loading="lazy"></div>
      <div>
        <span class="eyebrow">Online certificate · Biola Learn</span>
        <h2 class="h-section">Christian Apologetics Certificate</h2>
        <p style="margin-top:14px">An online certificate from Biola University’s learning platform, with teaching from Rahil on Hinduism and how to engage people from Hindu backgrounds.</p>
        {btn("View the course", BIOLA, "", True)}
      </div>
    </article>
    <article class="course">
      <div class="course-logo"><img src="{U}2025/10/partnership-col-logo-rt.png" alt="Christ Theological College" loading="lazy"></div>
      <div>
        <span class="eyebrow">Guest lectures · Christ Theological College</span>
        <h2 class="h-section">Guest lecturer</h2>
        <p style="margin-top:14px">Rahil teaches as a guest lecturer, bringing first-hand knowledge of Hindu practice to students preparing for ministry.</p>
        {btn("See Rahil’s lecturer profile", CTC, "", True)}
      </div>
    </article>
    <article class="course">
      <div class="course-logo"><img src="{U}2025/12/found-by-love-img.png" alt="" loading="lazy" style="max-height:130px"></div>
      <div>
        <span class="eyebrow">For churches and groups</span>
        <h2 class="h-section">Teaching for your church</h2>
        <p style="margin-top:14px">Seminars and short courses for churches, small groups and mission teams, including:</p>
        <ul>
          <li>Understanding Hindu thought and practice</li>
          <li>Sharing faith with Hindu friends and neighbours</li>
          <li>India’s growing global influence and the church</li>
        </ul>
        {btn("Enquire about teaching", "speaking.html#booking")}
      </div>
    </article>
  </div>
</section>"""
courses_schema = [crumbs("Courses", "/courses/"),
    {"@type": "Course", "name": "Christian Apologetics Certificate", "url": BIOLA,
     "description": "Online Christian apologetics certificate from Biola Learn, including teaching from Rahil Patel on Hinduism.",
     "provider": {"@type": "CollegeOrUniversity", "name": "Biola University", "sameAs": "https://www.biola.edu/"},
     "instructor": person_ref(),
     "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "Online", "instructor": person_ref()}}]
pages["courses.html"] = page("courses", "Courses", "Study Christian apologetics and Hindu thought with Rahil Patel: the Biola Learn Christian Apologetics Certificate, guest lectures and church teaching.",
                             courses_body, courses_schema, "/courses/")

# ---------------- Speaking ----------------
topics = [
    ("From Hindu Monk to Christ", "Rahil’s personal story of twenty years as a monk and his encounter with Jesus."),
    ("Understanding Hinduism", "Hindu thought, practice and culture explained for Christian audiences."),
    ("When Civilizations Meet", "India’s growing global influence and what it means for the church."),
    ("Apologetics in a Hindu Context", "Answering the questions Hindu friends actually ask about Jesus and truth."),
]
topics_html = "".join(f'<li><h3>{e(t)}</h3><p>{e(d)}</p></li>' for t, d in topics)
speaking_body = hero("Speaking", 'Invite Rahil <span class="highlight">to Speak</span>',
                     "Talks, sermons, seminars and Q&A for churches, conferences, universities and leadership teams around the world.",
                     [("topics", "Topics"), ("booking", "Booking")]) + f"""
<section class="section" id="topics" aria-labelledby="topics-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Topics</span><h2 id="topics-title" class="h-section">What Rahil speaks about</h2></div>
    <ul class="topics">{topics_html}</ul>
  </div>
</section>
<section class="section cream" id="booking" aria-labelledby="booking-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Booking</span><h2 id="booking-title" class="h-section">Send a speaking request</h2>
      <p>Tell us about your event and Rahil will be in touch.</p></div>
    <div class="booking">
      <form class="form" id="booking-form" action="#" method="post" novalidate>
        <div class="field"><label for="f-name">Full name *</label><input id="f-name" name="name" type="text" autocomplete="name" required></div>
        <div class="field"><label for="f-email">Email address *</label><input id="f-email" name="email" type="email" autocomplete="email" required></div>
        <div class="field full"><label for="f-org">Organisation</label><input id="f-org" name="organisation" type="text" autocomplete="organization"></div>
        <fieldset>
          <legend>Event details</legend>
          <div class="field"><label for="f-event">Event name</label><input id="f-event" name="event" type="text"></div>
          <div class="field"><label for="f-loc">Event location</label><input id="f-loc" name="location" type="text"></div>
          <div class="field"><label for="f-date">Event date</label><input id="f-date" name="date" type="date"></div>
          <div class="field"><label for="f-aud">Audience size</label><input id="f-aud" name="audience" type="text" inputmode="numeric"></div>
          <div class="field full"><label for="f-msg">Message</label><textarea id="f-msg" name="message"></textarea></div>
        </fieldset>
        <div class="actions"><button class="round-btn gold" type="submit">Send request{ARROW}</button></div>
        <p class="form-note" id="form-status" role="status"></p>
      </form>
      <aside class="contact-card" aria-label="Contact details">
        <h3>Prefer email?</h3>
        {icon_link(U + "2025/10/mail.svg", EMAIL, "mailto:" + EMAIL, alt="Email")}
        {icon_link(U + "2025/10/form-twitter-icon.svg", "@rahil3272", X_URL, True, alt="X")}
        {icon_link(U + "2026/10/substack.svg", "Substack", SUBSTACK, True, alt="Substack")}
      </aside>
    </div>
  </div>
</section>"""
speaking_schema = [crumbs("Speaking", "/speaking/"),
    {"@type": "Service", "name": "Speaking engagements with Rahil Patel", "serviceType": "Public speaking", "provider": person_ref(),
     "areaServed": "Worldwide", "url": SITE + "/speaking/",
     "audience": {"@type": "Audience", "audienceType": "Churches, conferences, universities, leaders and students"},
     "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Speaking topics", "itemListElement": [
         {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for t, d in topics]}},
    {"@type": "ContactPage", "url": SITE + "/speaking/", "name": "Book Rahil Patel to speak", "about": person_ref()}]
pages["speaking.html"] = page("speaking", "Speaking", "Invite Rahil Patel to speak at your church, conference or university on Hinduism, Christian apologetics and his journey from Hindu monk to Christ.",
                              speaking_body, speaking_schema, "/speaking/")

# ---------------- Writing ----------------
def article_list(items, source):
    out = ""
    for it in items:
        t, p = it[0], it[1]
        x = f"<p>{e(it[2])}</p>" if len(it) > 2 else ""
        out += f'<li><div><h3><a href="{SITE}/{p}">{e(t)}</a></h3>{x}</div><span class="source">{e(source)}</span></li>'
    return f'<ul class="list">{out}</ul>'

writing_body = hero("Writings", 'Faith, Culture and <span class="highlight">Civilisation</span>',
                    "Articles, columns, academic essays and reflections from Rahil Patel.",
                    [("occa", "OCCA articles"), ("seen-unseen", "Seen & Unseen"), ("essays", "Essays"), ("blog", "Blog")]) + f"""
<section class="section" id="occa" aria-labelledby="occa-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">OCCA articles</span><h2 id="occa-title" class="h-section">Writing for the Oxford Centre for Christian Apologetics</h2></div>
    {article_list(OCCA, "OCCA")}
  </div>
</section>
<section class="section cream" id="seen-unseen" aria-labelledby="su-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Seen &amp; Unseen</span><h2 id="su-title" class="h-section">Columns on culture and current affairs</h2></div>
    {article_list(SEEN, "Seen & Unseen")}
  </div>
</section>
<section class="section" id="essays" aria-labelledby="essays-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Essays</span><h2 id="essays-title" class="h-section">Academic essays on India</h2></div>
    {article_list(ESSAYS, "Essay")}
  </div>
</section>
<section class="section warm" id="blog" aria-labelledby="blog-title">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Blog</span><h2 id="blog-title" class="h-section">Reflections on leadership and life</h2></div>
    {article_list(BLOGS, "Blog")}
  </div>
</section>"""
all_articles = [(t, p, "Oxford Centre for Christian Apologetics") for t, p, _ in OCCA] + \
               [(t, p, "Seen & Unseen") for t, p in SEEN] + [(t, p, "Essay") for t, p, _ in ESSAYS] + [(t, p, "Blog") for t, p in BLOGS]
writing_schema = [crumbs("Writings", "/writing/"),
    {"@type": "CollectionPage", "url": SITE + "/writing/", "name": "Writings by Rahil Patel", "author": person_ref(),
     "mainEntity": {"@type": "ItemList", "itemListElement": [
         {"@type": "ListItem", "position": i + 1, "item": {"@type": "Article", "headline": t, "url": f"{SITE}/{p}",
                                                           "author": person_ref(), "publisher": {"@type": "Organization", "name": pub}}}
         for i, (t, p, pub) in enumerate(all_articles)]}}]
pages["writing.html"] = page("writing", "Writings", "Articles, columns, essays and blog posts by Rahil Patel on Hinduism, Christianity, India and culture.",
                             writing_body, writing_schema, "/writing/")

# ---------------- Partnerships ----------------
partners = [
    ("Oxford Centre for Christian Apologetics", "Rahil writes articles on faith, culture and Indic religions for OCCA.", OCCA_URL, U + "2025/10/partnership-col-logo-lt.png"),
    ("Christ Theological College", "Rahil is a guest lecturer, teaching students preparing for ministry and mission.", CTC, U + "2025/10/partnership-col-logo-rt.png"),
    ("Biola Learn", "Rahil teaches on the Christian Apologetics Certificate.", BIOLA, U + "2026/04/Biola-Learn-Logo_half-e1775556543502.jpg"),
]
partners_html = "".join(
    f'<a class="partner" href="{e(u)}" target="_blank" rel="noopener"><div class="logo-box"><img src="{im}" alt="{e(n)} logo" loading="lazy"></div><h3>{e(n)}</h3><p>{e(d)}</p><span class="text-link">Visit site</span></a>'
    for n, d, u, im in partners)
partners_body = hero("Partnerships", 'Working <span class="highlight">Together</span>',
                     "Organisations Rahil teaches, writes and partners with.") + f"""
<section class="section" aria-label="Partners">
  <div class="container"><div class="partners">{partners_html}</div>
    <div class="section-foot" style="text-align:center">{btn("Partner with Rahil", "speaking.html#booking")}</div>
  </div>
</section>"""
partners_schema = [crumbs("Partnerships", "/partnerships/"),
                   {"@type": "Organization", "name": "Oxford Centre for Christian Apologetics", "url": "https://theocca.org/"},
                   {"@type": "EducationalOrganization", "name": "Christ Theological College", "url": "https://www.ctcollege.org/"},
                   {"@type": "EducationalOrganization", "name": "Biola Learn", "url": "https://learn.biola.edu/"}]
pages["partnerships.html"] = page("partnerships", "Partnerships", "Organisations Rahil Patel works with, including the Oxford Centre for Christian Apologetics, Christ Theological College and Biola Learn.",
                                  partners_body, partners_schema, "/partnerships/")

for name, content in pages.items():
    (OUT / name).write_text(content, encoding="utf-8")
print("built", len(pages), "pages")
