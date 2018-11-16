# Here go your api methods.


@auth.requires_signature()
def add_post():
    post_id = db.post.insert(
        post_title=request.vars.post_title,
        post_content=request.vars.post_content,
    )
    # We return the id of the new post, so we can insert it along all the others.
    return response.json(dict(post_id=post_id))


def get_post_list():
    results = []
    if auth.user is None:
        # Not logged in.
        rows = db().select(db.post.ALL, orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.id,
                post_title=row.post_title,
                post_content=row.post_content,
                post_author=row.post_author,
                thumb = None,
                #thumb_count = row.post.thumb_count,
            ))
    else:
        # Logged in.
        rows = db().select(db.post.ALL, db.thumb.ALL,
                            left=[
                                db.thumb.on((db.thumb.post_id == db.post.id) & (db.thumb.user_email == auth.user.email)),
                            ],
                            orderby=~db.post.post_time)
        for row in rows:
            results.append(dict(
                id=row.post.id,
                post_title=row.post.post_title,
                post_content=row.post.post_content,
                post_author=row.post.post_author,
                thumb = None if row.thumb.id is None else row.thumb.thumb_state,
                thumb_count=row.post.thumb_count,
            ))
    # For homogeneity, we always return a dictionary.
    return response.json(dict(post_list=results))
    
@auth.requires_signature()
def set_thumb():
    post_id = int(request.vars.post_id)
    thumb_state = request.vars.thumb
    if thumb_state != None:
        db.thumb.update_or_insert(
            (db.thumb.post_id == post_id) & (db.thumb.user_email == auth.user.email),
            post_id = post_id,
            user_email = auth.user.email,
            thumb_state = thumb_state
        )
    else:
        db((db.thumb.post_id == post_id) & (db.thumb.user_email == auth.user.email)).delete()
    return "ok" # Might be useful in debugging.

@auth.requires_signature()
def update_count():
    post_id = int(request.vars.post_id)
    thumb_count = int(request.vars.thumb_count)
    #amount = int(request.vars.amount)
    db.post.update_or_insert((db.post.id == post_id),
        post_id = post_id,
        thumb_count = thumb_count,
    )
    return response.json(dict(post_id=post_id))
    #count = 0
    #rows = db().select(db.post.ALL, db.thumb.ALL, orderby=~db.post.post_time)
    #for row in rows:
    #    if row.thumb.post_id == post_id:
    #        if row.thumb.thumb_state == None:
    #            continue
    #        if row.thumb.thumb_state == 'u':
    #            count += 1
    #        if row.thumb.thumb_state == 'd':
    #            count -= 1
        
    #db.post.update_or_insert((db.post.id == post_id),
    #    post_id = post_id,
    #    thumb_count = count,
    #)
    #return response.json(dict(post_id=post_id))
        


