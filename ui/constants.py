MAX_HISTORY = 3

# ── Suggested questions (plain strings) ───────────────────────────────────────
# Used in sidebar.py: `for q in SUGGESTED`
SUGGESTED = [
    "What B.Tech programs does SMIT offer?",
    "What is the fee structure?",
    "How do I apply for admission?",
    "What is the placement record?",
    "Does SMIT provide hostel facilities?",
]

# ── Topic chips (icon, label) ──────────────────────────────────────────────────
# Used in chips.py: `for icon, label in CHIPS`
CHIPS = [
    ("🎓", "Admissions"),
    ("💰", "Fee Structure"),
    ("🏢", "Placements"),
    ("🏠", "Hostel"),
    ("🎁", "Scholarships"),
    ("📅", "Academic Calendar"),
]

# ── Announcements (icon, text, when) ──────────────────────────────────────────
# Used in sidebar.py: `for icon, text, when in ANNOUNCEMENTS`
ANNOUNCEMENTS = [
    ("📢", "Admissions Open 2026", "Apply before Aug 31"),
    ("🏢", "Campus Placement Drive Ongoing", "Top companies visiting"),
    ("🎓", "Scholarship Applications Available", "Deadline: Sep 15"),
]

# ── Upcoming events (month, day, title, sub) ───────────────────────────────────
# Used in sidebar.py: `for month, day, title, sub in EVENTS`
EVENTS = [
    ("AUG", "10", "Orientation Program", "Welcome to SMIT 2026 batch"),
    ("SEP", "05", "Tech Fest", "Annual technology festival"),
    ("OCT", "12", "Hackathon", "24-hour coding challenge"),
    ("NOV", "20", "Cultural Fest", "Music, dance & drama"),
]

# ── Empty-state cards (icon, label, subtitle) ──────────────────────────────────
# Used in empty_state.py: `for icon, label, sub in EMPTY_PROMPTS`
EMPTY_PROMPTS = [
    ("🎓", "Admissions", "Eligibility, dates & process"),
    ("💰", "Fee Structure", "Tuition, hostel & scholarships"),
    ("🏢", "Placements", "Companies, packages & stats"),
    ("🏠", "Hostel Facilities", "Rooms, mess & amenities"),
    ("📅", "Academic Calendar", "Semester dates & holidays"),
    ("🔬", "Programs Offered", "B.Tech, M.Tech & more"),
]