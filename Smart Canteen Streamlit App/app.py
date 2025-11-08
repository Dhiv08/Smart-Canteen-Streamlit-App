import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import os
from datetime import datetime

# ----------------------------------------
# PAGE CONFIG
# ----------------------------------------
st.set_page_config(page_title="Smart Canteen 🍴", page_icon="🍱", layout="wide")

# ----------------------------------------
# DATA SETUP
# ----------------------------------------
os.makedirs("data", exist_ok=True)
menu_path = "data/menu.csv"

menu_data = [
    # ---------------- VEG MAIN COURSES ----------------
    {"name": "Paneer Butter Masala", "category": "Veg", "calories": 450, "price": 100, "diet": "Vegetarian"},
    {"name": "Veg Biryani", "category": "Veg", "calories": 520, "price": 90, "diet": "Vegetarian"},
    {"name": "Dal Tadka & Rice", "category": "Veg", "calories": 400, "price": 80, "diet": "Vegetarian"},
    {"name": "Aloo Gobi", "category": "Veg", "calories": 350, "price": 70, "diet": "Vegetarian"},
    {"name": "Mixed Veg Curry", "category": "Veg", "calories": 380, "price": 85, "diet": "Vegetarian"},
    {"name": "Chole Bhature", "category": "Veg", "calories": 550, "price": 110, "diet": "Vegetarian"},
    {"name": "Palak Paneer", "category": "Veg", "calories": 420, "price": 95, "diet": "Vegetarian"},
    {"name": "Vegetable Korma", "category": "Veg", "calories": 390, "price": 85, "diet": "Vegetarian"},
    {"name": "Masala Dosa", "category": "Veg", "calories": 430, "price": 70, "diet": "Vegetarian"},
    {"name": "Idli & Sambar", "category": "Veg", "calories": 300, "price": 50, "diet": "Vegetarian"},
    {"name": "Paneer Tikka", "category": "Veg", "calories": 410, "price": 100, "diet": "Vegetarian"},
    {"name": "Veg Pulao", "category": "Veg", "calories": 390, "price": 85, "diet": "Vegetarian"},
    {"name": "Rajma Chawal", "category": "Veg", "calories": 450, "price": 80, "diet": "Vegetarian"},
    {"name": "Stuffed Paratha", "category": "Veg", "calories": 380, "price": 65, "diet": "Vegetarian"},
    {"name": "Kadai Paneer", "category": "Veg", "calories": 460, "price": 105, "diet": "Vegetarian"},

    # ---------------- NON-VEG MAIN COURSES ----------------
    {"name": "Butter Chicken", "category": "Non-Veg", "calories": 580, "price": 130, "diet": "Non-Vegetarian"},
    {"name": "Chicken Biryani", "category": "Non-Veg", "calories": 640, "price": 120, "diet": "Non-Vegetarian"},
    {"name": "Fish Curry with Rice", "category": "Non-Veg", "calories": 560, "price": 140, "diet": "Non-Vegetarian"},
    {"name": "Egg Fried Rice", "category": "Non-Veg", "calories": 480, "price": 100, "diet": "Non-Vegetarian"},
    {"name": "Grilled Chicken Breast", "category": "Non-Veg", "calories": 460, "price": 150, "diet": "Non-Vegetarian"},
    {"name": "Mutton Curry", "category": "Non-Veg", "calories": 610, "price": 160, "diet": "Non-Vegetarian"},
    {"name": "Prawn Masala", "category": "Non-Veg", "calories": 520, "price": 155, "diet": "Non-Vegetarian"},
    {"name": "Chicken Tikka Masala", "category": "Non-Veg", "calories": 570, "price": 135, "diet": "Non-Vegetarian"},
    {"name": "Egg Curry & Rice", "category": "Non-Veg", "calories": 450, "price": 95, "diet": "Non-Vegetarian"},
    {"name": "Fish Fry Thali", "category": "Non-Veg", "calories": 540, "price": 150, "diet": "Non-Vegetarian"},
    {"name": "Chicken Shawarma", "category": "Non-Veg", "calories": 430, "price": 100, "diet": "Non-Vegetarian"},
    {"name": "Grilled Fish Steak", "category": "Non-Veg", "calories": 500, "price": 180, "diet": "Non-Vegetarian"},
    {"name": "Mutton Biryani", "category": "Non-Veg", "calories": 680, "price": 160, "diet": "Non-Vegetarian"},
    {"name": "Chicken Noodles", "category": "Non-Veg", "calories": 520, "price": 120, "diet": "Non-Vegetarian"},

    # ---------------- VEGAN MAIN COURSES ----------------
    {"name": "Tofu Stir Fry", "category": "Vegan", "calories": 350, "price": 100, "diet": "Vegan"},
    {"name": "Vegan Wrap", "category": "Vegan", "calories": 320, "price": 90, "diet": "Vegan"},
    {"name": "Quinoa Salad", "category": "Vegan", "calories": 280, "price": 80, "diet": "Vegan"},
    {"name": "Grilled Veg Sandwich", "category": "Vegan", "calories": 300, "price": 75, "diet": "Vegan"},
    {"name": "Vegan Rice Bowl", "category": "Vegan", "calories": 400, "price": 95, "diet": "Vegan"},
    {"name": "Oatmeal Bowl", "category": "Vegan", "calories": 260, "price": 70, "diet": "Vegan"},
    {"name": "Chickpea Curry", "category": "Vegan", "calories": 370, "price": 90, "diet": "Vegan"},
    {"name": "Veggie Burger (Vegan Patty)", "category": "Vegan", "calories": 420, "price": 110, "diet": "Vegan"},
    {"name": "Vegan Fried Rice", "category": "Vegan", "calories": 330, "price": 85, "diet": "Vegan"},
    {"name": "Tofu Curry & Brown Rice", "category": "Vegan", "calories": 390, "price": 95, "diet": "Vegan"},

    # ---------------- BEVERAGES ----------------
    {"name": "Fresh Lime Juice", "category": "Beverage", "calories": 90, "price": 40, "diet": "All"},
    {"name": "Cold Coffee", "category": "Beverage", "calories": 180, "price": 60, "diet": "All"},
    {"name": "Masala Chai", "category": "Beverage", "calories": 100, "price": 30, "diet": "All"},
    {"name": "Protein Shake", "category": "Beverage", "calories": 220, "price": 80, "diet": "All"},
    {"name": "Filter Coffee", "category": "Beverage", "calories": 120, "price": 35, "diet": "All"},
    {"name": "Buttermilk", "category": "Beverage", "calories": 70, "price": 25, "diet": "All"},
    {"name": "Green Tea", "category": "Beverage", "calories": 10, "price": 30, "diet": "All"},
    {"name": "Fruit Smoothie", "category": "Beverage", "calories": 150, "price": 60, "diet": "All"},
    {"name": "Iced Latte", "category": "Beverage", "calories": 160, "price": 70, "diet": "All"},
    {"name": "Lassi (Sweet/Salted)", "category": "Beverage", "calories": 190, "price": 50, "diet": "All"},

    # ---------------- DESSERTS ----------------
    {"name": "Gulab Jamun", "category": "Dessert", "calories": 200, "price": 50, "diet": "Vegetarian"},
    {"name": "Chocolate Brownie", "category": "Dessert", "calories": 250, "price": 70, "diet": "Vegetarian"},
    {"name": "Vegan Cupcake", "category": "Dessert", "calories": 220, "price": 80, "diet": "Vegan"},
    {"name": "Fruit Bowl", "category": "Dessert", "calories": 180, "price": 60, "diet": "All"},
    {"name": "Rasgulla", "category": "Dessert", "calories": 170, "price": 45, "diet": "Vegetarian"},
    {"name": "Mysore Pak", "category": "Dessert", "calories": 210, "price": 55, "diet": "Vegetarian"},
    {"name": "Ice Cream Cup", "category": "Dessert", "calories": 190, "price": 70, "diet": "Vegetarian"},
    {"name": "Vegan Pudding", "category": "Dessert", "calories": 200, "price": 85, "diet": "Vegan"},
    {"name": "Kheer", "category": "Dessert", "calories": 230, "price": 60, "diet": "Vegetarian"},
    {"name": "Brownie Sundae", "category": "Dessert", "calories": 280, "price": 90, "diet": "Vegetarian"},
]

menu = pd.DataFrame(menu_data)
menu.to_csv(menu_path, index=False)

# ----------------------------------------
# SESSION DEFAULTS
# ----------------------------------------
for key, val in {"user": None, "page": "Home", "tray": [], "logged_in": False, "diet": "Select", "gender": "Select"}.items():
    if key not in st.session_state:
        st.session_state[key] = val

# ----------------------------------------
# LOGIN PAGE (Side-by-Side Labels + Centered)
# ----------------------------------------
if not st.session_state.logged_in:
    # 🍴 Title and tagline
    st.markdown(
        """
        <h1 style='text-align:center; color:black; margin-top:10px; font-size:48px; font-family:Poppins, sans-serif;'>
            🍴 Smart Canteen
        </h1>
        <h4 style='text-align:center; color:#333333; font-size:22px; font-family:Poppins, sans-serif; margin-bottom:30px;'>
            Your personalized dining experience 🌿
        </h4>
        """,
        unsafe_allow_html=True
    )

    # 🖼️ Food banner image
    st.markdown(
        """
        <div style='text-align:center;'>
            <img src='https://img.freepik.com/free-photo/various-indian-dishes-top-view_23-2148747719.jpg'
                 width='450' style='border-radius:20px; box-shadow:0 6px 20px rgba(0,0,0,0.3); margin-top:10px;'>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 🧍‍♀️ Subheader
    st.markdown(
        "<h3 style='text-align:center; color:#2E8B57;'>👩‍💻 Create your profile to continue</h3>",
        unsafe_allow_html=True
    )

    # 💅 Inline label-input styling
    st.markdown(
        """
        <style>
        .form-box {
            max-width: 500px;
            margin: 0 auto;
            background: rgba(255,255,255,0.85);
            padding: 25px 40px;
            border-radius: 15px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }

        .field {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin: 10px 0;
        }

        .field label {
            font-weight: 600;
            color: #333;
            width: 40%;
            text-align: right;
            margin-right: 10px;
        }

        .field input, .field select {
            width: 60%;
            padding: 8px;
            border-radius: 8px;
            border: 1px solid #ccc;
            box-shadow: 0 1px 5px rgba(0,0,0,0.1);
        }

        .center {
            text-align: center;
            margin-top: 15px;
        }

        .stButton > button {
            width: 50%;
            margin: 0 auto;
            display: block;
            background: linear-gradient(90deg, #0b8a42, #4caf50);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 10px 25px;
            font-size: 18px;
            font-weight: bold;
            box-shadow: 0 3px 10px rgba(0,0,0,0.2);
            transition: 0.3s;
        }

        .stButton > button:hover {
            transform: scale(1.05);
            box-shadow: 0 5px 15px rgba(11,138,66,0.4);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 🧾 Custom HTML form layout
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    gender = st.selectbox("Gender", ["Select", "Male", "Female", "Other"])
    diet = st.selectbox("Dietary Preference", ["Select", "Vegetarian", "Non-Vegetarian", "Vegan"])
    terms = st.checkbox("✅ I accept the Terms & Conditions")

    # 🚀 Start button
    if st.button("Start Now 🚀"):
        if not all([name.strip(), email.strip()]) or gender == "Select" or diet == "Select" or not terms:
            st.warning("⚠️ Please fill all required fields.")
        else:
            st.session_state.user = name.strip().title()
            st.session_state.email = email
            st.session_state.gender = gender
            st.session_state.diet = diet
            st.session_state.logged_in = True
            st.success(f"Welcome, {st.session_state.user}! Let’s start your Smart Dining Journey 😋")
            st.balloons()
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


# ----------------------------------------
# SIDEBAR
# ----------------------------------------
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/857/857681.png", width=70)
st.sidebar.markdown(f"### 👤 Hello, {st.session_state.user}!")
st.sidebar.markdown(f"**Gender:** {st.session_state.gender}")
st.sidebar.markdown(f"**Diet:** {st.session_state.diet}")
st.sidebar.markdown("---")

pages = ["Home", "Menu", "Cart", "Dashboard", "Feedback"]
labels = ["🏠 Home", "🍱 Menu", "🛒 Cart", "📊 Dashboard", "💬 Feedback"]
index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
choice = st.sidebar.radio("Navigate", labels, index=index)
st.session_state.page = pages[labels.index(choice)]

if st.sidebar.button("🚪 Logout"):
    for k in list(st.session_state.keys()):
        del st.session_state[k]
    st.rerun()

## ----------------------------------------
# HOME PAGE
# ----------------------------------------
if st.session_state.page == "Home":

        # Welcome text
    st.markdown(f"<h1 style='text-align:center;'>👋 Hi, {st.session_state.user}!</h1>", unsafe_allow_html=True)
    st.markdown(
        "<p style='text-align:center;'>Welcome to <b>Smart Canteen</b> — where taste meets technology 🍴</p>",
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # 🖼️ Smaller centered image (not full width)
    st.markdown(
        """
        <div style='text-align:center;'>
            <img src='https://img.freepik.com/free-photo/indian-food-thali-top-view-assorted-traditional-dishes_123827-20789.jpg'
                 width='600' style='border-radius:15px; box-shadow:0 4px 15px rgba(0,0,0,0.2);'>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<br><br>", unsafe_allow_html=True)



    # Navigation buttons in 3 columns
    c1, c2, c3 = st.columns(3)

    nav_target = None  # Temporary variable to handle navigation safely

    with c1:
        if st.button("🍽️ Smart Menu", use_container_width=True):
            nav_target = "Menu"

    with c2:
        if st.button("🛒 Order Now", use_container_width=True):
            nav_target = "Cart"

    with c3:
        if st.button("📊 My Dashboard", use_container_width=True):
            nav_target = "Dashboard"

    # ✅ Safe rerun trigger
    if nav_target:
        st.session_state.page = nav_target
        st.rerun()

# ----------------------------------------
# MENU PAGE
# ----------------------------------------
elif st.session_state.page == "Menu":
    st.header("🍱 Smart Menu — Personalized for You")
    diet = st.session_state.diet
    df = menu.copy()
    if diet == "Vegetarian":
        df = df[df["diet"].isin(["Vegetarian", "Vegan", "All"])]
    elif diet == "Non-Vegetarian":
        df = df[df["diet"].isin(["Non-Vegetarian", "All"])]
    elif diet == "Vegan":
        df = df[df["diet"].isin(["Vegan", "All"])]
    cat = st.selectbox("Filter by Category", ["All"] + sorted(df["category"].unique()))
    if cat != "All":
        df = df[df["category"] == cat]
    for _, r in df.iterrows():
        st.markdown(f"### {r['name']} — ₹{r['price']}")
        st.caption(f"{r['category']} | {r['calories']} kcal | {r['diet']}")
        q = st.number_input(f"Quantity for {r['name']}", 1, 10, 1, key=f"qty_{r['name']}")
        if st.button(f"Add {r['name']} to Cart", key=f"add_{r['name']}"):
            i = r.to_dict(); i["quantity"] = q
            st.session_state.tray.append(i)
            st.success(f"✅ Added {q} × {r['name']} to cart!")

# ----------------------------------------
# CART PAGE
# ----------------------------------------
elif st.session_state.page == "Cart":
    st.header("🛒 Your Cart")
    if not st.session_state.tray:
        st.warning("Cart is empty — add items from Menu.")
    else:
        df = pd.DataFrame(st.session_state.tray)
        df["Total"] = df["price"] * df["quantity"]
        st.dataframe(df[["name", "price", "quantity", "Total"]], use_container_width=True)
        total = df["Total"].sum()
        st.subheader(f"💰 Total: ₹{total}")
        if st.button("Proceed to Pay 💳"):
            st.success(f"Payment Successful — Enjoy your meal, {st.session_state.user}! 😋")
            df["user"] = st.session_state.user
            df["date"] = datetime.now()
            hist = "data/history.csv"
            if os.path.exists(hist):
                old = pd.read_csv(hist)
                df = pd.concat([old, df])
            df.to_csv(hist, index=False)
            st.session_state.tray = []
            st.balloons()

# ----------------------------------------
# DASHBOARD PAGE
# ----------------------------------------
elif st.session_state.page == "Dashboard":
    st.header("📊 Your Calorie Dashboard")
    hist = "data/history.csv"
    if not os.path.exists(hist):
        st.info("No order history yet.")
    else:
        data = pd.read_csv(hist)
        u = data[data["user"] == st.session_state.user]
        if u.empty:
            st.info("No orders found.")
        else:
            u["date"] = pd.to_datetime(u["date"])
            u["day"] = u["date"].dt.date
            chart = u.groupby("day")["calories"].sum().reset_index()
            st.plotly_chart(px.bar(chart, x="day", y="calories",
                                   color="calories", color_continuous_scale="greens"),
                            use_container_width=True)

# ----------------------------------------
# FEEDBACK PAGE
# ----------------------------------------
elif st.session_state.page == "Feedback":
    st.markdown("<h2 style='text-align:center;'>💬 Feedback & Suggestions</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;'>We value your feedback to improve Smart Canteen 🌱</p>", unsafe_allow_html=True)
    st.write("")

    # Two-column layout
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("⭐ Rate your experience")
        rating = st.slider("Select Rating (1 = Poor, 5 = Excellent)", 1, 5, 4)
        comment = st.text_area("📝 Write your feedback below:")

        if st.button("Submit Feedback 💚"):
            if not comment.strip():
                st.warning("⚠️ Please write your feedback before submitting.")
            else:
                sentiment_score = TextBlob(comment).sentiment.polarity
                if sentiment_score > 0:
                    sentiment_text = "Positive 😊"
                elif sentiment_score < 0:
                    sentiment_text = "Negative 😞"
                else:
                    sentiment_text = "Neutral 😐"

                st.success(f"Thanks, {st.session_state.user}! Your feedback sentiment is **{sentiment_text}**.")
                st.snow()

                # Optional: save feedback to a CSV file
                feedback_path = "data/feedback.csv"
                new_entry = pd.DataFrame([{
                    "user": st.session_state.user,
                    "rating": rating,
                    "feedback": comment,
                    "sentiment": sentiment_text,
                    "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }])
                if os.path.exists(feedback_path):
                    old = pd.read_csv(feedback_path)
                    new_entry = pd.concat([old, new_entry], ignore_index=True)
                new_entry.to_csv(feedback_path, index=False)

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1048/1048949.png", width=250)
        st.info("✨ Your feedback helps us grow smarter & tastier!")
