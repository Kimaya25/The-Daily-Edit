import os
import json
import re
import html
import requests
import feedparser
import streamlit as st
from bs4 import BeautifulSoup
from groq import Groq

st.set_page_config(
    page_title="The Daily Edit",
    page_icon="☕",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Playfair+Display:wght@600;700;800&display=swap');

.stApp {
    background: #1F171D;
    color: #F2EDE3;
    font-family: 'Inter', sans-serif;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #D6B36A;
}

[data-testid="stSidebar"] {
    background: #4A2433;
    border-right: 1px solid #D6B36A;
}

[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #FFF8EC !important;
}

input {
    color: #2F1B23 !important;
    background: #FFF8EC !important;
    font-weight: 800 !important;
}

div[data-baseweb="select"] > div {
    background-color: #FFF8EC !important;
    color: #2F1B23 !important;
    font-weight: 900 !important;
    border: 2px solid #D6B36A !important;
}

div[data-baseweb="select"] span {
    color: #2F1B23 !important;
    font-weight: 900 !important;
}

div[data-baseweb="select"] svg {
    fill: #2F1B23 !important;
}

div[role="listbox"] {
    background-color: #FFF8EC !important;
}

div[role="option"] {
    background-color: #FFF8EC !important;
    color: #2F1B23 !important;
    font-weight: 800 !important;
}

div[role="option"]:hover {
    background-color: #D9DDC7 !important;
}

span[data-baseweb="tag"] {
    background-color: #6B2737 !important;
    color: #FFF8EC !important;
    font-weight: 800 !important;
    border-radius: 12px !important;
}

span[data-baseweb="tag"] span {
    color: #FFF8EC !important;
}

span[data-baseweb="tag"] svg {
    fill: #FFF8EC !important;
}

.main-card {
    background: #2C2029;
    border: 1.5px solid #D6B36A;
    border-radius: 30px;
    padding: 44px;
    margin-bottom: 28px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.35);
}

.brand-kicker {
    color: #D6B36A;
    text-transform: uppercase;
    letter-spacing: 2px;
    font-weight: 800;
    font-size: 13px;
    margin-bottom: 12px;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 84px;
    line-height: 1.02;
    font-weight: 800;
    color: #D6B36A;
    margin-bottom: 18px;
}

.hero-subtitle {
    font-size: 21px;
    line-height: 1.65;
    color: #F2EDE3;
    max-width: 900px;
}

.pill {
    display: inline-block;
    background: #5F7355;
    color: #FFF8EC;
    padding: 9px 17px;
    border-radius: 999px;
    margin-right: 8px;
    margin-top: 14px;
    font-weight: 800;
    font-size: 14px;
}

.gold-pill {
    background: #D6B36A;
    color: #1F171D;
}

.info-card {
    background: #2C2029;
    border: 1.3px solid #5F7355;
    border-radius: 24px;
    padding: 30px;
    margin-top: 24px;
    box-shadow: 0 14px 36px rgba(0,0,0,0.25);
}

.profile-card {
    background: #352631;
    border: 1.3px solid #D6B36A;
    border-radius: 22px;
    padding: 22px;
    margin-top: 18px;
}

.profile-label {
    color: #D6B36A;
    font-weight: 800;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.profile-value {
    color: #F2EDE3;
    font-size: 17px;
    margin-bottom: 12px;
}

.news-card {
    background: #F7F1E7;
    color: #2F1B23 !important;
    border-radius: 28px;
    padding: 36px;
    margin-top: 30px;
    box-shadow: 0 14px 34px rgba(0,0,0,0.32);
    border: 1.5px solid #D6B36A;
}

.news-card * {
    color: #2F1B23 !important;
}

.topic-label {
    display: inline-block;
    background: #5F7355;
    color: #FFF8EC !important;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-right: 8px;
    margin-bottom: 14px;
}

.score-label {
    display: inline-block;
    background: #6B2737;
    color: #FFF8EC !important;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-bottom: 14px;
}

.news-title {
    font-family: 'Playfair Display', serif;
    color: #6B2737 !important;
    font-size: 34px;
    font-weight: 800;
    margin-bottom: 18px;
    line-height: 1.1;
}

.section-heading {
    display: inline-block;
    background: #6B2737;
    color: #FFF8EC !important;
    padding: 6px 14px;
    border-radius: 999px;
    font-size: 13px;
    font-weight: 800;
    margin-top: 16px;
    margin-bottom: 8px;
    letter-spacing: 0.4px;
}

.news-body {
    color: #2F1B23 !important;
    line-height: 1.75;
    font-size: 16.5px;
    margin-bottom: 8px;
}

.action-box {
    background: #D9DDC7;
    border-left: 5px solid #5F7355;
    padding: 16px;
    border-radius: 14px;
    margin-top: 18px;
    font-weight: 700;
}

.small-note {
    color: #D8DCC4;
    font-size: 16px;
    line-height: 1.7;
}

.stButton button {
    background: #5F7355;
    color: #FFF8EC;
    border-radius: 999px;
    padding: 12px 24px;
    font-weight: 800;
    border: 1px solid #D6B36A;
}

.stButton button:hover {
    background: #6B2737;
    color: #FFF8EC;
}

a {
    color: #D6B36A !important;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
NEWS_API_KEY = os.environ.get("NEWS_API_KEY")

RSS_FEEDS = {
    "AI": ["https://techcrunch.com/category/artificial-intelligence/feed/"],
    "Tech": ["https://techcrunch.com/feed/"],
    "Sports": ["https://www.espn.com/espn/rss/news"],
    "Fashion": ["https://www.businessoffashion.com/feed/"],
    "Music": ["https://www.billboard.com/feed/"],
    "Finance": ["https://www.cnbc.com/id/100003114/device/rss/rss.html"],
    "Pop Culture": ["https://www.elle.com/rss/all.xml/"],
    "Literature": ["https://lithub.com/feed/"],
    "Science": ["https://www.sciencedaily.com/rss/top/science.xml"],
    "Geopolitics": ["https://www.aljazeera.com/xml/rss/all.xml"],
    "World Affairs": ["https://feeds.bbci.co.uk/news/world/rss.xml"],
    "Startups": ["https://techcrunch.com/category/startups/feed/"],
    "Marketing": ["https://www.marketingdive.com/feeds/news/"],
    "FinTech": ["https://www.finextra.com/rss/headlines.aspx"]
}

NEWSAPI_QUERIES = {
    "AI": "artificial intelligence OR OpenAI OR AI",
    "Tech": "technology OR software OR big tech",
    "Sports": "sports OR tennis OR formula 1",
    "Fashion": "fashion industry OR luxury fashion OR retail",
    "Music": "music industry OR artists OR streaming",
    "Finance": "finance OR stock market OR economy",
    "Pop Culture": "celebrity OR entertainment OR pop culture",
    "Literature": "books OR publishing OR literature",
    "Science": "science OR discovery OR research",
    "Geopolitics": "geopolitics OR diplomacy OR conflict",
    "World Affairs": "world news OR international relations",
    "Startups": "startups OR venture capital OR funding",
    "Marketing": "marketing OR advertising OR brands",
    "FinTech": "fintech OR digital payments OR banking technology"
}

def safe_text(value):
    if value is None:
        return ""
    value = str(value)
    value = re.sub(r"```.*?```", "", value, flags=re.DOTALL)
    value = re.sub(r"<[^>]+>", "", value)
    value = value.replace("{", "").replace("}", "")
    return html.escape(value.strip())

def extract_article_text(url, max_chars=900):
    try:
        response = requests.get(
            url,
            timeout=8,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        soup = BeautifulSoup(response.text, "html.parser")

        for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
            tag.decompose()

        paragraphs = soup.find_all("p")
        article_text = " ".join(p.get_text(" ", strip=True) for p in paragraphs)
        article_text = re.sub(r"\s+", " ", article_text).strip()

        return article_text[:max_chars]

    except Exception:
        return ""

def fetch_newsapi_articles(topic):
    articles = []

    if not NEWS_API_KEY:
        return articles

    query = NEWSAPI_QUERIES.get(topic, topic)

    try:
        url = "https://newsapi.org/v2/everything"

        params = {
            "q": query,
            "language": "en",
            "sortBy": "publishedAt",
            "pageSize": 3,
            "apiKey": NEWS_API_KEY
        }

        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        for article in data.get("articles", [])[:3]:
            link = article.get("url", "")
            article_text = extract_article_text(link, max_chars=900)

            articles.append({
                "topic": topic,
                "title": article.get("title", ""),
                "summary": article.get("description", ""),
                "article_text": article_text,
                "link": link
            })

    except Exception:
        pass

    return articles

def fetch_rss_articles(topic):
    articles = []
    feeds = RSS_FEEDS.get(topic, [])

    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)

            for entry in feed.entries[:3]:
                link = entry.get("link", "")
                article_text = extract_article_text(link, max_chars=900)

                articles.append({
                    "topic": topic,
                    "title": entry.get("title", ""),
                    "summary": entry.get("summary", ""),
                    "article_text": article_text,
                    "link": link
                })

        except Exception:
            pass

    return articles[:3]

def fetch_headlines_by_topic(selected_topics):
    topic_headlines = {}

    for topic in selected_topics:
        newsapi_articles = fetch_newsapi_articles(topic)

        if newsapi_articles:
            topic_headlines[topic] = newsapi_articles
        else:
            topic_headlines[topic] = fetch_rss_articles(topic)

    return topic_headlines

def clean_json_response(content):
    cleaned = content.strip()
    cleaned = re.sub(r"```json", "", cleaned)
    cleaned = re.sub(r"```", "", cleaned)
    cleaned = cleaned.strip()

    start = cleaned.find("{")
    end = cleaned.rfind("}") + 1

    if start != -1 and end != -1:
        cleaned = cleaned[start:end]

    return json.loads(cleaned)

def generate_newsletter(name, degree, career_goal, interests, reading_time, briefing_style, topic_headlines):
    client = Groq(api_key=GROQ_API_KEY)

    headline_text = ""

    for topic, headlines in topic_headlines.items():
        headline_text += f"\n\nTOPIC: {topic}\n"

        for item in headlines:
            headline_text += f"""
- Title: {item['title']}
  Summary: {item['summary'][:300]}
  Article extract: {item.get('article_text', '')[:700]}
"""

    prompt = f"""
Create a personalised daily intelligence briefing for a college student.

Product name: The Daily Edit
Tagline: Your world, edited for you.

Student name: {name}
Degree: {degree}
Career goal: {career_goal}
Selected interests: {", ".join(interests)}
Reading time: {reading_time}
Briefing style: {briefing_style}

Use ONLY these selected interests and live article extracts:
{headline_text}

Return ONLY valid JSON.
Do NOT include HTML.
Do NOT include markdown code blocks.
Do NOT include CSS.

Your job is not just to summarise news.
Your job is to explain why each story matters specifically to this student.

The "what_happened" section must be informative:
- use 3 to 5 sentences,
- include key actors,
- include numbers, locations, companies, dates, or policy details if available,
- explain immediate context,
- do not overclaim beyond the article extract.

The "degree_connection" must be deeply personalised:
- connect to coursework, skills, internships, interviews, projects, or academic concepts,
- avoid generic phrases.

The "career_impact" must be practical:
- mention roles, industries, hiring signals, interview talking points, or emerging opportunities.

The "money_or_future_impact" must be specific:
- mention sectors, companies, consumer behaviour, investment themes, or market signals.

The "personal_impact" must explain how this could affect the student's life in the next 6 to 24 months.

The "personal_impact_score" must be honest.
Score from 1 to 10 based on selected interests, degree, career goal, and usefulness within 6 to 24 months.

Adapt the briefing based on selected briefing style:
- Academic: focus on concepts, coursework, theory, and deeper understanding.
- Career-focused: focus on internships, roles, hiring trends, skills, and career opportunities.
- Investment-focused: focus on markets, sectors, companies, money flows, and investment implications.
- Interview prep: focus on smart talking points, case interview relevance, and discussion-ready insights.
- Casual catch-up: make it easier, lighter, and conversational while still useful.

Return JSON in this exact structure:

{{
  "opening": "short 3 sentence editorial opening in The Daily Edit voice",
  "stories": [
    {{
      "topic": "selected interest name",
      "headline": "specific story headline",
      "relevance_score": "score out of 10",
      "personal_impact_score": "score out of 10",
      "what_happened": "3 to 5 sentence specific article-based explanation",
      "why_it_matters": "specific explanation",
      "degree_connection": "specific deep link to the student's degree",
      "career_impact": "specific link to the career goal",
      "money_or_future_impact": "specific market, money, sector, or future impact",
      "personal_impact": "how this could affect the student personally",
      "smart_takeaway": "memorable takeaway",
      "what_should_i_do": "one practical action the student can take"
    }}
  ],
  "concept_of_the_day": {{
    "concept": "concept name",
    "explanation": "simple explanation",
    "why_student_should_care": "why it matters to this student"
  }},
  "unexpected_connection": {{
    "connection": "connection title",
    "explanation": "explain link between two selected interests"
  }},
  "conversation_starter": "one smart natural line"
}}

Rules:
Create one story per selected interest.
Keep it useful, specific, and student-friendly.
Tone: dark academia, intelligent, polished, practical.
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Return valid JSON only. Never return markdown. Never return HTML."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.35,
        max_tokens=2500
    )

    content = response.choices[0].message.content

    try:
        return clean_json_response(content)
    except Exception:
        st.warning("The AI returned messy formatting. Try Create Today's Edit again.")
        return {
            "opening": "The briefing generated, but the formatting was messy. Try again.",
            "stories": [],
            "concept_of_the_day": {
                "concept": "Formatting issue",
                "explanation": "The AI returned text instead of clean structured cards.",
                "why_student_should_care": "This is a formatting issue, not a product logic issue."
            },
            "unexpected_connection": {
                "connection": "Almost there",
                "explanation": "Click Create Today's Edit again."
            },
            "conversation_starter": "The app is working, but the card format needs one more generation."
        }

def render_story_card(story):
    card_html = f"""
<div class="news-card">
<span class="topic-label">{safe_text(story.get("topic", "Story"))}</span>
<span class="score-label">Relevance: {safe_text(story.get("relevance_score", "N/A"))}</span>
<span class="score-label">Personal Impact: {safe_text(story.get("personal_impact_score", "N/A"))}</span>

<div class="news-title">{safe_text(story.get("headline", "Untitled story"))}</div>

<div class="section-heading">WHAT HAPPENED</div>
<div class="news-body">{safe_text(story.get("what_happened", ""))}</div>

<div class="section-heading">WHY IT MATTERS</div>
<div class="news-body">{safe_text(story.get("why_it_matters", ""))}</div>

<div class="section-heading">WHY THIS MATTERS FOR YOUR DEGREE</div>
<div class="news-body">{safe_text(story.get("degree_connection", ""))}</div>

<div class="section-heading">CAREER IMPACT</div>
<div class="news-body">{safe_text(story.get("career_impact", ""))}</div>

<div class="section-heading">MONEY / MARKETS / FUTURE IMPACT</div>
<div class="news-body">{safe_text(story.get("money_or_future_impact", ""))}</div>

<div class="section-heading">PERSONAL IMPACT</div>
<div class="news-body">{safe_text(story.get("personal_impact", ""))}</div>

<div class="section-heading">SMART TAKEAWAY</div>
<div class="news-body">{safe_text(story.get("smart_takeaway", ""))}</div>

<div class="action-box">
🎯 What should I actually do? {safe_text(story.get("what_should_i_do", ""))}
</div>
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)

def render_support_card(label, title, body, extra_label=None, extra_body=None):
    extra_html = ""

    if extra_label and extra_body:
        extra_html = f"""
<div class="section-heading">{safe_text(extra_label)}</div>
<div class="news-body">{safe_text(extra_body)}</div>
"""

    card_html = f"""
<div class="news-card">
<span class="topic-label">{safe_text(label)}</span>
<div class="news-title">{safe_text(title)}</div>
<div class="news-body">{safe_text(body)}</div>
{extra_html}
</div>
"""
    st.markdown(card_html, unsafe_allow_html=True)

with st.sidebar:
    st.header("The Daily Edit")
    st.caption("Tell us who you are. We'll edit the world for you.")

    name = st.text_input("Your name", "Kimaya")

    degree = st.selectbox(
        "Your degree",
        [
            "Computer Science",
            "Electrical Engineering",
            "Mechanical Engineering",
            "Physics",
            "Marketing",
            "Economics",
            "Finance",
            "FinTech",
            "Design",
            "Law",
            "Medicine",
            "Political Science"
        ]
    )

    career_goal = st.selectbox(
        "Career goal",
        [
            "Product roles",
            "Tech",
            "AI",
            "Software roles",
            "Management roles",
            "Entrepreneurship",
            "Consulting",
            "Finance roles",
            "Marketing roles",
            "Policy roles",
            "Research",
            "Not sure yet"
        ]
    )

    interests = st.multiselect(
        "Choose your interests",
        [
            "AI",
            "Tech",
            "Sports",
            "Fashion",
            "Music",
            "Finance",
            "Pop Culture",
            "Literature",
            "Science",
            "Geopolitics",
            "World Affairs",
            "Startups",
            "Marketing",
            "FinTech"
        ],
        default=["AI", "Tech", "Finance", "World Affairs"]
    )

    reading_time = st.selectbox(
        "Reading time",
        ["5 minutes", "10 minutes", "15 minutes", "20 minutes"]
    )

    briefing_style = st.selectbox(
        "Briefing style",
        [
            "Academic",
            "Career-focused",
            "Investment-focused",
            "Interview prep",
            "Casual catch-up"
        ]
    )

    generate = st.button("Create Today's Edit")

st.markdown("""
<div class="main-card">
    <div class="brand-kicker">PERSONALISED STUDENT INTELLIGENCE</div>
    <div class="hero-title">The Daily Edit</div>
    <div class="hero-subtitle">
        Your personalised intelligence briefing that transforms global headlines into insights
        for your degree, career ambitions, financial future, and everyday life.
    </div>
    <br>
    <span class="pill">degree-aware</span>
    <span class="pill">career-linked</span>
    <span class="pill gold-pill">personal impact scored</span>
    <span class="pill">quick to read</span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
<h3>Your world, edited for you.</h3>
<p class="small-note">
Choose your interests, degree, career goal, and briefing style. The Daily Edit turns live news into card-based insights based on what actually matters to you.
</p>
</div>
""", unsafe_allow_html=True)

if generate:
    if not GROQ_API_KEY:
        st.error("Groq API key missing.")
    elif not interests:
        st.error("Please choose at least one interest.")
    else:
        st.markdown(f"""
<div class="profile-card">
<div class="profile-label">Today's profile</div>
<div class="profile-value"><b>Name:</b> {safe_text(name)}</div>
<div class="profile-value"><b>Degree:</b> {safe_text(degree)}</div>
<div class="profile-value"><b>Career goal:</b> {safe_text(career_goal)}</div>
<div class="profile-value"><b>Briefing style:</b> {safe_text(briefing_style)}</div>
</div>
""", unsafe_allow_html=True)

        with st.spinner("Fetching real articles and building your Daily Edit..."):
            topic_headlines = fetch_headlines_by_topic(interests)

            briefing = generate_newsletter(
                name,
                degree,
                career_goal,
                interests,
                reading_time,
                briefing_style,
                topic_headlines
            )

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.success("Your Daily Edit is ready.")
        st.markdown(f"### Good morning, {safe_text(name)}")
        st.write(briefing.get("opening", ""))
        st.markdown('</div>', unsafe_allow_html=True)

        for story in briefing.get("stories", []):
            render_story_card(story)

        concept = briefing.get("concept_of_the_day", {})
        render_support_card(
            "Concept of the Day",
            concept.get("concept", "Concept"),
            concept.get("explanation", ""),
            "WHY YOU SHOULD CARE",
            concept.get("why_student_should_care", "")
        )

        connection = briefing.get("unexpected_connection", {})
        render_support_card(
            "Unexpected Connection",
            connection.get("connection", "Connection"),
            connection.get("explanation", "")
        )

        render_support_card(
            "Conversation Starter",
            "Say this today",
            briefing.get("conversation_starter", "")
        )

        st.markdown('<div class="info-card">', unsafe_allow_html=True)
        st.subheader("Sources by interest")

        for topic, headlines in topic_headlines.items():
            st.markdown(f"### {topic}")
            for item in headlines[:3]:
                st.markdown(f"- [{item['title']}]({item['link']})")

        st.markdown('</div>', unsafe_allow_html=True)