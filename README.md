# flask_udemy_comments

<h4>Final section of https://www.udemy.com/python-flask-course/ by Jorge </h4>

Added comment functionality.

Step 1: Update register view and set new user is_author to false

```
@app.route('/register', methods=('GET', 'POST'))
def register():
    form=RegisterForm()
    if form.validate_on_submit():
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(form.password.data, salt)
        author=Author(
            form.fullname.data,
            form.email.data,
            form.username.data,
            hashed_password,
            False
            )
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('success'))
    return render_template('author/register.html', form=form)

```

Step 2: New Model for Commment
```
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    publish_date = db.Column(db.DateTime)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    
    def __init__(self, body, post, publish_date=None):
        self.body = body
        self.post_id = post
        if publish_date is None:
            self.publish_date = datetime.utcnow()
        else:
            self.publish_date = publish_date

    def __repr__(self):
        return self.body
```

Step 3. New views code for def article to pick up comments

```
@app.route('/article/<slug>', methods=('POST', 'GET'))
def article(slug):
    form = CommentForm()
    post = Post.query.filter_by(slug=slug).first_or_404()
    comments = Comment.query.filter_by(post_id=post.id)
    if form.validate_on_submit():
        body = form.comment.data
        post_id = post.id
        comment = Comment(body, post_id)
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article', slug=slug))
    return render_template('blog/article.html', post=post, form=form, comments=comments, slug=slug)
```

Step 4. New Article HTML to show existing comments, and form to submit new comments

```
  <h4>Want to join the conversation? Login</h4>

        {% for comment in comments %}
        
        <div style="background-color:rgba(250,250,250,0.8); padding-bottom: 25px">
        
        {{ comment.body }}
        
        </div>
         <div style="background-color:white; padding-bottom: 15px"></div>
         
        {% endfor %}
        
        {% if 'username' in session %}
        
            {% from "_formhelpers.html" import render_field %}
             <form method="POST" action="{{ url_for('article', slug=slug) }}" role="form">
            {{ form.hidden_tag() }}
                
            {{ render_field(form.comment, class='form-control') }}
            
            <button type="submit" class="btn btn-default">Comment</button>
        {% endif %}
```
