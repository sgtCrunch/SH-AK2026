import os
from flask import Flask, render_template, request, jsonify, redirect
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix


app = Flask(__name__)

#app.config['PREFERRED_URL_SCHEME'] = 'https'
# Fix proxy headers when behind Nginx
#app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)


# ── Config ────────────────────────────────────────────────
UPLOAD_FOLDER   = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
CLUE_FOLDER   = os.path.join(os.path.dirname(__file__), 'static', 'clue-imgs')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ── Sample data — replace with your own source ────────────
Clues = {
    "weird-clue":'''Its fun to remember times when 
                    we were weirder with tons of whimsy. 
                    To be fair you still have plent of both.
                    For this challenge, buy a bouquet of flowers 
                    and pose with the "Lady With Flowers". 
                    In the photo you must imitate Anushe's 
                    favorite Mario character,
                    Waluigi! You know the pose I'm talking about! Make sure
                    you upload the photo on the next page!''',
    "end-clue":'''Happy Birthday Anushe!''',
    "eyebrow-clue":'''Huh, you looking at me? Remember, its a momentous occasion, 
                      don't forget why we are here. You know even Caesar would agree. You haven't 
                      met him? Ask your namesake, he defintely knows him. For this challenge,
                      decypher this: "ilqg brxu idyrulwh errn dqg wdnh d skrwr dv d jurxs."
                      Don't be afraid to use techology!''',
    "avo-clue": '''Phew that was fun! Being 
                    one with nature is important.
                    I mean look at Anushe in this photo! There's
                    something calming about rituals. For this challenge,
                    walk through the labyrinth and find your inner peace.
                    Take a photo of you in the labyrinth and upload it on the next page!
                    ''',
    "peace-clue":'''Peace out hombre! I hope you enjoyed the journey. I know I have.
                    For the last challenge, someone for goodness sake take an action shot of
                    of Anushe on the race track! Make sure to upload it on the next page!''',
    "paint-clue":'''Pretty cool huh? It challenges our perception of reality
                    and makes us pay attention. For this challenge, you will solve the
                    Anushe themed crossword! Once done take a picture and submit it on the next page.''',
    "baby-clue":'''I hope you enjoyed your mosaic class! 
                We know how much you like making things 
                and we all thought this was perfect.
                For each blue letter clue, you'll 
                find a task to complete and a picture 
                to take and upload. For this one, we would 
                love a group photo of all of you 
                holding up your completed mosaics!
                Go to the last page to upload your photo.
                Make sure to take it first with your phone and
                then click upload to choose it from your library.''',
    "puzzclue":'''Whoa! Not gonna lie I thought you weren't 
                    gonna find it. You are really good at puzzles! 
                    For this challenge, just pose with your finished puzzle, 
                    make sure you are smoking your invisible cigar! 
                    Upload the photo on the next page!'''
}

travel_clues = {
    "weird-clue":'''Beautiful poses! Truly breathtaking! 
                    To find your next location, must with all your 
                    Senses seek the Labyrinth. Don't be a fool start 
                    from the top and then go down. If you don't know where 
                    to start, then seek the Scottish soldier 
                    hes always on the Lookout.''',
    "eyebrow-clue":'''Dang I should really read more books. 
                      For your next location, we will explore space
                      and light. It is important to examine what is
                      Within and what we are Without. When you do this 
                      and dare to go into the pyramid, you will find your next clue.''',
    "avo-clue":'''I feel zen don't you? For your next location,
                  is about finding peace with people around the world 
                  and espeically your sister! Did you know that there's a bird
                  that migrates from Japan every year to Canberra? Incredible. One
                  more thing, check tables when you get there...''',
    "peace-clue":'''Are you hungry? I know I am. For your next location, its dinner time!
                    We have reservation at KOTO Japanese Restaurant for 6:15pm! Don't be late!
                    MMM I love sushi.''',    
    "paint-clue":'''Dang I wish I was that fast. Anushe always beats me badly at those.
                    Anyway, you know whats fun? Tiny little cars made for children going 
                    at unatural speeds. For your next location, find your nearest go-kart race track!''',
    "baby-clue":'''Great job on the mosaics! To find your next location you must
                   find the whimsical and naive Lady With Flowers. She is patiently waiting for her tram
                   to arrive. Go say hi and ask for your next clue!
                ''',
    "puzzclue":'''Dang really speeding through this. 
                  For your next location, you need to seek the stacks.
                  They say knowledge is power so go find YY 358.24 K12, I guess its 
                  in your namesake? Also don't go too far, this is almost over.'''
}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clean_text(text):
    """Remove newlines and tabs from text, preserving single spaces."""
    return ' '.join(text.split())


# ── Routes ────────────────────────────────────────────────
# This route handles the root URL, e.g., "/"
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def letter(path):
    print(f"Received request for path: {path}")
    
    # Check if path exists in Clues to prevent KeyError from malicious requests
    if path not in Clues:
        from flask import abort
        abort(404)
    
    clue_img_url = f'/static/clue-imgs/{path}.jpg'
    cleaned_text = clean_text(Clues[path])
    pages = [[clue_img_url, cleaned_text]]

    return render_template('blue-letter.html', 
                           pages=pages,
                           background_url=f'/static/backgrounds/{path}.png', 
                           redirect_url=f'/{path}/completed')

@app.route('/<path:path>/completed')
def note(path):
    # Check if path exists in travel_clues to prevent KeyError
    if path not in travel_clues:
        from flask import abort
        abort(404)
    
    travel_clue = travel_clues[path]

    return render_template('travel-clue.html',
                           background_url=f'/static/backgrounds/travel-clue.gif', 
                           clue=clean_text(travel_clue))


@app.route('/robots.txt')
def robots():
    return app.send_static_file('robots.txt')


@app.route('/upload-photo', methods=['POST'])
def upload_photo():
    if 'photo' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['photo']

    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        # Get the endpoint that sent the request from the referrer
        from urllib.parse import urlparse
        base, ext = os.path.splitext(file.filename)
        
        if request.referrer:
            parsed_url = urlparse(request.referrer)
            origin_endpoint = parsed_url.path.strip('/') or 'index'
        else:
            origin_endpoint = 'upload'
        
        filename  = f'{origin_endpoint}{ext}'
        save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        file.save(save_path)
        url = f'/static/uploads/{filename}'
        return jsonify({'url': url, 'filename': filename})

    return jsonify({'error': 'File type not allowed'}), 400


if __name__ == '__main__':
    app.run(debug=True)
