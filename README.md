# flask_udemy_comments

Final section of https://www.udemy.com/python-flask-course/ by Jorge 

Added comment functionality.

Step 1: New Model for Commment

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

Step 2. New views code for def article

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

Step 3. New Article HTML to show existing comments, and form to submit new comments

   <h4>Want to join the conversation?</h4>

        {% for comment in comments %}
        
        <div style="background-color:rgba(250,250,250,0.8); padding-bottom: 25px">
        
        {{ comment.body }}
        
        </div>
         <div style="background-color:white; padding-bottom: 15px"></div>
         
        {% endfor %}
        
       
        
        {% from "_formhelpers.html" import render_field %}
         <form method="POST" action="{{ url_for('article', slug=slug) }}" role="form">
        {{ form.hidden_tag() }}
            
        {{ render_field(form.comment, class='form-control') }}
        
        <button type="submit" class="btn btn-default">Comment</button>

