from flask import flash, redirect, render_template, request, session, url_for, jsonify
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy import or_
from sqlalchemy.orm import aliased
from app import app, db
from app.models import Users, Users_information, Users_role, Messages
from app.helpers import apology, login_required, admin_required, validate_required, role, validate, check_inform

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.context_processor
def inject_user_role_and_unread_messages_counter():
    user_role = role(session['user_id']) if 'user_id' in session else None
    unread_messages_count = Messages.query.filter_by(recipient_id=session['user_id'], is_read=False).count() if 'user_id' in session else 0
    return dict(user_role=user_role, unread_messages_count=unread_messages_count)

# Login/out routes, framework provided by cs50 staff, I add new logic and a new sql library
@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Querying the database to find dose username exist
        user = Users.query.filter_by(username=request.form.get("username")).first()
        if user is None or not user.username:
            return apology("invalid username and/or password", 403)

        # Ensure username exists and password is correct
        if not check_password_hash(
            user.hash, request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = user.id

        # Ask user to fill information for admin to validate
        if validate(user.id) == 1 and check_inform(user.id) is None:
            return redirect("/edit")
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    
    session.clear()
    
    return redirect("/")

# Users routes
@app.route("/")
@login_required
@validate_required
def index():

    # Present all users' information 
    users = Users_information.query.with_entities(
        Users_information.realname,
        Users_information.nickname,
        Users_information.is_club_member,
        Users_information.contact
        ).join(Users_role, Users_role.user_id == Users_information.user_id).filter(
        Users_information.realname.isnot(None),
        Users_information.nickname.isnot(None),
        Users_information.is_club_member.isnot(None),
        Users_information.contact.isnot(None),
        Users_role.is_hidden == 0
        ).all()
       
    return render_template("index.html", users=users)

@app.route("/profile")
@login_required
def profile():
    
    user_id = session["user_id"]
    
    user = db.session.query(Users, Users_information, Users_role) \
        .join(Users_information, Users.id == Users_information.user_id) \
        .join(Users_role, Users.id == Users_role.user_id) \
        .filter(Users.id == user_id) \
        .first()
        
    user1 = user[0]
    print(user1.username)
    return render_template("profile.html", user=user)

@app.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    
    if request.method == "POST":

        user_id = session["user_id"]

        realname = request.form.get("realname")
        if not realname:
            realname = ""

        nickname = request.form.get("nickname")
        if not nickname:
            nickname = ""

        is_club_member = request.form.get("is_club_member")
        if not is_club_member:
            is_club_member = ""

        contact = request.form.get("contact")
        if not contact:
            contact = ""

        # Update user information to database
        new_info = Users_information.query.filter_by(user_id=user_id).first()

        new_info.realname = realname
        new_info.nickname = nickname
        new_info.is_club_member = is_club_member
        new_info.contact = contact
        db.session.commit()

        flash('Information Confirmed!')

        return redirect("/")

    else:
        return render_template("edit.html")

@app.route("/search", methods=["GET", "POST"])
@login_required
@validate_required
def search():
    
    q = request.args.get("q")
    
    if q:
        role_alias = aliased(Users_role)
        users = db.session.query(Users_information).join(role_alias, Users_information.user_id == role_alias.user_id).filter(
            or_(
                Users_information.realname.like(f"%{q}%"),
                Users_information.nickname.like(f"%{q}%"),
                Users_information.is_club_member.like(f"%{q}%"),
                Users_information.contact.like(f"%{q}%")
            )
        ).filter(role_alias.is_hidden == 0).limit(50).all()

        users_j = []
        for user in users:
            user_d = user.to_dict(include_user_id=False)
            users_j.append(user_d)

        return jsonify(users_j)
    
    return render_template("search.html")

@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    
    user_id = session.get("user_id")
    
    if request.method == "POST":
        
        password_c = request.form.get("current_password")
        password_n = request.form.get("new_password")
        check = request.form.get("check")

        # Check user input
        if not password_c or not password_n or check != password_n:
            return apology("Check your input and try again!")

        # Make sure user provid correct password
        user = Users.query.filter_by(id=user_id).first()
        if not check_password_hash(
            user.hash, password_c
        ):
            return apology("invalid password")

        user.hash = generate_password_hash(password_n)
        db.session.commit()
        
        flash('Password Changed!')
        
        return redirect("/")
    
    return render_template("change.html")

# Admin and register routes
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        # Get username, password from html
        name = request.form.get("username")
        password = request.form.get("password")
        check = request.form.get("confirmation")

        if not name or not password or check != password:
            return apology("Check your input and try again!")

        # generate the hashed password
        hashed_password = generate_password_hash(password)
        
        existed_user = Users.query.filter_by(username=name).first()

        if existed_user:
            return apology("Username exists!")
       
        new_user = Users(username=name, hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        new_info = Users_information(user_id=new_user.id)
        new_role = Users_role(user_id=new_user.id)
        db.session.add(new_info)
        db.session.add(new_role)
        db.session.commit()

        return redirect("/login")
    
    return render_template("register.html")

@app.route("/admin", methods=["GET", "POST"])
@login_required
@admin_required
def admin():
    
    if request.method == "POST":
        
        # This two section allow you to validate user and delete user who is unvalidate 
        # It makes sure every users must be validate by admin
        if "validate" in request.form:
            user_id = request.form.get("user_id")
            user = Users_role.query.filter_by(user_id=user_id).first()
            user.is_hidden = 0
            db.session.commit()

        elif "delete" in request.form:
            user_id = request.form.get("user_id")
            Users_information.query.filter_by(user_id=user_id).delete()
            Users_role.query.filter_by(user_id=user_id).delete()
            Users.query.filter_by(id=user_id).delete()
            db.session.commit()
            
        elif "unvalidate" in request.form:
            user_id = request.form.get("user_id")
            user = Users_role.query.filter_by(user_id=user_id).first()
            user.is_hidden = 1
            db.session.commit()

        return redirect(url_for("admin"))

    else:

        # Present all users are not validated
        users = db.session.query(Users, Users_information, Users_role) \
            .join(Users_information, Users.id == Users_information.user_id) \
            .join(Users_role, Users.id == Users_role.user_id) \
            .filter(Users_role.is_hidden == 1) \
            .all()
            
        # Present all users are validated
        users1 = db.session.query(Users, Users_information, Users_role) \
            .join(Users_information, Users.id == Users_information.user_id) \
            .join(Users_role, Users.id == Users_role.user_id) \
            .filter(Users_role.is_hidden == 0) \
            .filter(Users_role.role != 'admin') \
            .all()

        return render_template("admin.html", users=users, users1=users1)

# Site message route    
@app.route("/send_message", methods=["GET", "POST"])
@login_required
@admin_required
def send_message():
    
    if request.method == "POST":
        recipient_name = request.form.get("recipient_name")
        title = request.form.get("title")
        content = request.form.get("content")
        
        if not recipient_name or not title or not content:
            apology("Rcipient name/Title/Message content is required")
            
        sender_id = session["user_id"]
        
        if recipient_name == 'all':
            users = db.session.query(Users_information) \
            .join(Users_role, Users_information.user_id == Users_role.user_id) \
            .filter(Users_role.is_hidden == 0) \
            .filter(Users_role.role != 'admin') \
            .all()
            for user in users:
                message = Messages(sender_id=sender_id, recipient_id=user.user_id, title=title, content=content)
                db.session.add(message)
        
        else:
            recipient = Users_information.query.filter_by(realname=recipient_name).first()
            message = Messages(sender_id=sender_id, recipient_id=recipient.user_id, title=title, content=content)
            db.session.add(message)
        
        db.session.commit()
        flash("Message sent successfully!")
        
        return redirect (url_for("send_message"))
    
    else:
        users_list = ['all']
        users = db.session.query(Users_information) \
            .join(Users_role, Users_information.user_id == Users_role.user_id) \
            .filter(Users_role.is_hidden == 0) \
            .filter(Users_role.role != 'admin') \
            .all()
        for user in users:
            users_list.append(user.realname)
        
        return render_template("send_message.html", users=[user for user in users_list])
    
@app.route("/mailbox", methods=["GET"])
@login_required
@validate_required
def mailbox():
    
    if role(session["user_id"]) == 'reader':
        user_id = session["user_id"]

        messages = Messages.query.filter_by(recipient_id=user_id).all()
        
        unread_messages = Messages.query.filter_by(recipient_id=user_id, is_read=False).all()
        for message in unread_messages:
            message.is_read = True
            db.session.commit()

        return render_template("mailbox.html", messages=messages)
    
    elif role(session["user_id"]) == 'admin':
        user_id = session["user_id"]
        
       # messages = Messages.query.filter_by(sender_id=user_id).all()
        
        messages =  db.session.query(Messages, Users_information) \
            .join(Users_information, Messages.recipient_id == Users_information.user_id) \
            .all()
        
        return render_template("mailbox.html", messages=messages)
        